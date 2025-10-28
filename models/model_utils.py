"""
Utility functions for model operations
"""
import torch
import json
import os


def count_parameters(model):
    """
    Count trainable and frozen parameters in the model.
    
    Returns:
        dict with trainable_params, frozen_params, total_params, trainable_pct
    """
    trainable_params = 0
    frozen_params = 0
    
    for param in model.parameters():
        if param.requires_grad:
            trainable_params += param.numel()
        else:
            frozen_params += param.numel()
    
    total_params = trainable_params + frozen_params
    trainable_pct = 100 * trainable_params / total_params if total_params > 0 else 0
    
    return {
        'trainable': trainable_params,
        'frozen': frozen_params,
        'total': total_params,
        'trainable_pct': trainable_pct
    }


def print_model_summary(model):
    """Print detailed model parameter summary."""
    stats = count_parameters(model)
    
    print("=" * 80)
    print("MODEL SUMMARY:")
    print("=" * 80)
    print(f"Trainable parameters:  {stats['trainable']:>15,} ({stats['trainable_pct']:.2f}%)")
    print(f"Frozen parameters:     {stats['frozen']:>15,}")
    print(f"Total parameters:      {stats['total']:>15,}")
    print("=" * 80)
    
    print("\nParameter breakdown by layer:")
    for name, param in model.named_parameters():
        status = "✓ TRAINABLE" if param.requires_grad else "❄ FROZEN"
        print(f"{status} | {name:60s} | {param.numel():>12,}")
    print("=" * 80 + "\n")


def save_model(model, save_dir, label_dict=None):
    """
    Save model and configuration.
    
    Args:
        model: The model to save
        save_dir: Directory to save to
        label_dict: Optional label mapping dictionary
    """
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"\nSaving model to {save_dir}...")
    
    # Save model state
    torch.save({
        'model_state_dict': model.state_dict(),
        'model_config': {
            'model_type': model.__class__.__name__,
            'num_labels': 40  # You can make this dynamic
        }
    }, os.path.join(save_dir, "pytorch_model.bin"))
    
    # Save BERT base
    if hasattr(model, 'bert'):
        bert_dir = os.path.join(save_dir, "bert_base")
        model.bert.save_pretrained(bert_dir)
    
    # Save label mapping
    if label_dict:
        with open(os.path.join(save_dir, 'label_mapping.json'), 'w') as f:
            json.dump(label_dict, f, indent=2)
    
    print(f"Model saved successfully!")


def load_model(model_class, load_dir, device='cuda'):
    """
    Load a saved model.
    
    Args:
        model_class: The model class to instantiate
        load_dir: Directory to load from
        device: Device to load model on
    
    Returns:
        Loaded model
    """
    checkpoint = torch.load(
        os.path.join(load_dir, "pytorch_model.bin"),
        map_location=device
    )
    
    model = model_class()
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    print(f"Model loaded from {load_dir}")
    return model