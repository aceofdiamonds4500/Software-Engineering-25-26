"""
Main training script
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import random
import numpy as np
import pandas as pd
from torch.optim import AdamW
import time

from models import get_model, print_model_summary, save_model
from data import load_medical_data, preprocess_dataframe, prepare_data
from training.trainer import train_epoch, validate, format_time
from config import TrainingConfig


def set_seed(seed):
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def main():
    """Main training function."""
    
    # Load configuration
    config = TrainingConfig()
    
    # Set device
    print("="*80)
    print("SYSTEM INFORMATION")
    print("="*80)
    print(f"Torch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available() and config.USE_CUDA:
        device = torch.device("cuda")
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
        # Speed optimizations
        torch.backends.cudnn.benchmark = True
        try:
            torch.set_float32_matmul_precision('high')
        except Exception:
            pass
    else:
        device = torch.device("cpu")
    
    print(f"Using device: {device}")
    print("="*80 + "\n")
    
    # Set seed
    set_seed(config.SEED)
    
    # Load and prepare data
    print("="*80)
    print("LOADING DATA")
    print("="*80)
    
    df = load_medical_data(config.DATA_PATH)
    
    # Preprocess text
    df = preprocess_dataframe(df, 'transcription', 'clean_transcription')
    
    # Prepare data loaders
    train_dataloader, validation_dataloader, tokenizer, label_dict = prepare_data(
        df, 
        text_column='clean_transcription',
        batch_size=config.BATCH_SIZE,
        max_length=config.MAX_LENGTH
    )
    
    # Calculate class weights if enabled
    class_weights = None
    if config.USE_CLASS_WEIGHTS:
        print("\nCalculating class weights for imbalanced data...")
        from sklearn.utils.class_weight import compute_class_weight
        import numpy as np
        
        labels = df.specialty_id.values
        class_weights = compute_class_weight(
            'balanced',
            classes=np.arange(config.NUM_LABELS),
            y=labels
        )
        # Convert class_weights to Float tensor to match expected type
        class_weights = torch.tensor(class_weights, dtype=torch.float32)
        print(f"Class weights range: {class_weights.min():.3f} to {class_weights.max():.3f}")
    
    # Create model
    print("="*80)
    print("CREATING MODEL")
    print("="*80)
    
    model = get_model(
        model_type=config.MODEL_TYPE,
        num_labels=config.NUM_LABELS,
        dropout_rate=config.DROPOUT_RATE,
        class_weights=class_weights,
        model_name=config.MODEL_NAME,
        freeze_layers=config.FREEZE_LAYERS
    ).to(device)

    # Initialize final layer bias with log class priors to improve early accuracy
    try:
        labels_np = df.specialty_id.values
        counts = np.bincount(labels_np, minlength=config.NUM_LABELS).astype(np.float32)
        priors = counts / (counts.sum() + 1e-8)
        priors = np.clip(priors, 1e-8, 1.0)
        bias_init = torch.log(torch.tensor(priors, dtype=torch.float32, device=device))
        with torch.no_grad():
            # Assumes the last layer in classifier is the final Linear
            model.classifier[-1].bias.copy_(bias_init)
        print("Initialized classifier bias with log class priors.")
    except Exception as e:
        print(f"Warning: could not initialize bias from priors: {e}")
    
    # Print model summary
    print_model_summary(model)
    
    # Setup optimizer with differential learning rates
    if config.MODEL_TYPE == 'advanced':
        optimizer = AdamW([
            {'params': model.classifier.parameters(), 'lr': config.LEARNING_RATE_HEAD},
            {'params': model.bert.encoder.layer[9].parameters(), 'lr': config.LEARNING_RATE_BERT},
            {'params': model.bert.encoder.layer[10].parameters(), 'lr': config.LEARNING_RATE_BERT},
            {'params': model.bert.encoder.layer[11].parameters(), 'lr': config.LEARNING_RATE_BERT},
            {'params': model.bert.pooler.parameters(), 'lr': config.LEARNING_RATE_BERT}
        ], weight_decay=config.WEIGHT_DECAY)
    else:
        optimizer = AdamW(
            model.parameters(),
            lr=config.LEARNING_RATE_HEAD,
            weight_decay=config.WEIGHT_DECAY
        )
    
    # Setup warmup + linear decay scheduler stepped per batch
    total_steps = len(train_dataloader) * config.EPOCHS
    warmup_steps = config.WARMUP_STEPS if config.WARMUP_STEPS and config.WARMUP_STEPS > 0 else max(1, int(0.1 * total_steps))

    def lr_lambda(current_step: int):
        if current_step < warmup_steps:
            return float(current_step) / float(warmup_steps)
        # Linear decay after warmup
        return max(0.0, float(total_steps - current_step) / float(max(1, total_steps - warmup_steps)))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
    
    # Ensure checkpoint directory exists
    if getattr(config, 'SAVE_CHECKPOINTS', False):
        os.makedirs(config.CHECKPOINT_DIR, exist_ok=True)

    best_val_acc = -1.0
    best_epoch = -1

    # Training loop
    print("="*80)
    print("STARTING TRAINING")
    print("="*80)
    
    training_stats = []
    total_t0 = time.time()
    
    # Helper to set freeze depth on the fly
    def set_freeze_layers(model, freeze_layers):
        try:
            for i, layer in enumerate(model.bert.encoder.layer):
                requires = i >= freeze_layers
                for p in layer.parameters():
                    p.requires_grad = requires
            # keep embeddings frozen per original design
            for p in model.bert.embeddings.parameters():
                p.requires_grad = False
        except Exception:
            pass
    
    # Helper to set freeze depth on the fly
    def set_freeze_layers(model, freeze_layers):
        try:
            for i, layer in enumerate(model.bert.encoder.layer):
                requires = i >= freeze_layers
                for p in layer.parameters():
                    p.requires_grad = requires
            # keep embeddings frozen per original design
            for p in model.bert.embeddings.parameters():
                p.requires_grad = False
        except Exception:
            pass

    for epoch_i in range(config.EPOCHS):
        # Epoch 0: short freeze — freeze 11 layers for first half, then restore to 9
        if epoch_i == 0 and config.MODEL_TYPE == 'advanced':
            try:
                set_freeze_layers(model, 11)
            except Exception:
                pass
        # Epoch 0: freeze one extra BERT layer to stabilize early updates
        if epoch_i == 0 and config.MODEL_TYPE == 'advanced':
            set_freeze_layers(model, max(0, TrainingConfig.FREEZE_LAYERS + 1))
        elif epoch_i == 1 and config.MODEL_TYPE == 'advanced':
            # Restore configured freeze depth thereafter
            set_freeze_layers(model, TrainingConfig.FREEZE_LAYERS)
        # Train
        def freeze_control(action: str):
            if action == 'restore':
                try:
                    set_freeze_layers(model, TrainingConfig.FREEZE_LAYERS)
                except Exception:
                    pass

        avg_train_loss, training_time = train_epoch(
            model, train_dataloader, optimizer, device, epoch_i, config.EPOCHS, scheduler, freeze_control
        )
        
        # Validate
        avg_val_accuracy, avg_val_loss, validation_time, f1_macro, f1_weighted = validate(
            model, validation_dataloader, device
        )
        
        # Note: scheduler stepped per-batch inside train_epoch
        
        # Save checkpoints
        if getattr(config, 'SAVE_CHECKPOINTS', False):
            checkpoint_dir = os.path.join(config.CHECKPOINT_DIR, f"epoch_{epoch_i+1}")
            try:
                save_model(model, checkpoint_dir, label_dict)
            except Exception as e:
                print(f"Warning: could not save epoch checkpoint: {e}")

            if getattr(config, 'SAVE_BEST', False) and avg_val_accuracy > best_val_acc:
                best_val_acc = avg_val_accuracy
                best_epoch = epoch_i + 1
                best_dir = os.path.join(config.CHECKPOINT_DIR, 'best')
                try:
                    save_model(model, best_dir, label_dict)
                    print(f"Saved best checkpoint (epoch {best_epoch}) with acc {best_val_acc:.2%}.")
                except Exception as e:
                    print(f"Warning: could not save best checkpoint: {e}")

        # Record stats
        training_stats.append({
            'epoch': epoch_i + 1,
            'Training Loss': avg_train_loss,
            'Valid. Loss': avg_val_loss,
            'Valid. Accur.': avg_val_accuracy,
            'F1 (macro)': f1_macro,
            'F1 (weighted)': f1_weighted,
            'Training Time': training_time,
            'Validation Time': validation_time
        })
    
    print("")
    print("Training complete!")
    print(f"Total training took {format_time(time.time()-total_t0)} (h:mm:ss)")
    
    # Print final statistics
    print("\n" + "="*80)
    print("TRAINING SUMMARY:")
    print("="*80)
    df_stats = pd.DataFrame(training_stats)
    print(df_stats.to_string(index=False))
    print("="*80 + "\n")
    
    # Save model
    save_model(model, config.SAVE_DIR, label_dict)
    
    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print("="*80)
    print(f"Model saved to: {config.SAVE_DIR}")
    print(f"Final validation accuracy: {training_stats[-1]['Valid. Accur.']:.2%}")
    print(f"Final F1 (macro): {training_stats[-1]['F1 (macro)']:.2f}")
    print(f"Final F1 (weighted): {training_stats[-1]['F1 (weighted)']:.2f}")
    print("="*80)


if __name__ == "__main__":
    main()