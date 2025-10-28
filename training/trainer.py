"""
Training loop and evaluation functions
"""
import torch
import numpy as np
import time
import datetime
import os
import sys
from torch.amp import autocast, GradScaler
from sklearn.metrics import f1_score

# Ensure project root is on sys.path for package imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import TrainingConfig

config = TrainingConfig()


def format_time(elapsed):
    """Convert seconds to hh:mm:ss format."""
    elapsed_rounded = int(round((elapsed)))
    return str(datetime.timedelta(seconds=elapsed_rounded))


def flat_accuracy(preds, labels):
    """Calculate accuracy from predictions and labels."""
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)


def train_epoch(model, train_dataloader, optimizer, device, epoch_i, epochs, scheduler=None, freeze_control=None):
    """
    Train model for one epoch.
    
    Returns:
        avg_train_loss, training_time
    """
    print("")
    print(f'======== Epoch {epoch_i + 1} / {epochs} ========')
    print('Training...')

    t0 = time.time()
    total_train_loss = 0
    use_amp = torch.cuda.is_available() and device.type == 'cuda'
    scaler = GradScaler('cuda', enabled=use_amp)

    model.train()

    half_point = max(1, len(train_dataloader) // 2)
    for step, batch in enumerate(train_dataloader):
        # Restore normal freeze depth halfway through epoch 0
        if freeze_control is not None and epoch_i == 0 and step == half_point:
            try:
                freeze_control('restore')
            except Exception:
                pass
        if step % 16 == 0 and step != 0:
            elapsed = format_time(time.time() - t0)
            print(f'  Batch {step:>5,}  of  {len(train_dataloader):>5,}.    Elapsed: {elapsed}.')

        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        b_labels = batch[2].to(device)

        model.zero_grad()

        with autocast('cuda', enabled=use_amp):
            outputs = model(
                b_input_ids,
                token_type_ids=None,
                attention_mask=b_input_mask,
                labels=b_labels,
                label_smoothing=config.LABEL_SMOOTHING
            )

            loss = outputs.loss
        total_train_loss += loss.item()

        scaler.scale(loss).backward()
        # Unscale before clipping to avoid scaling affecting clipping threshold
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        # Step LR scheduler per batch if provided (supports warmup)
        if scheduler is not None:
            try:
                scheduler.step()
            except Exception:
                pass

    avg_train_loss = total_train_loss / len(train_dataloader)
    training_time = format_time(time.time() - t0)

    print("")
    print(f"  Average training loss: {avg_train_loss:.2f}")
    print(f"  Training epoch took: {training_time}")

    return avg_train_loss, training_time


def validate(model, validation_dataloader, device):
    """
    Validate model.
    
    Returns:
        avg_val_accuracy, avg_val_loss, validation_time
    """
    print("")
    print("Running Validation...")

    t0 = time.time()
    model.eval()

    total_eval_accuracy = 0
    total_eval_loss = 0
    all_preds = []
    all_labels = []

    use_amp = torch.cuda.is_available() and device.type == 'cuda'
    for batch in validation_dataloader:
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        b_labels = batch[2].to(device)

        with torch.no_grad():
            with autocast('cuda', enabled=use_amp):
                outputs = model(
                    b_input_ids,
                    token_type_ids=None,
                    attention_mask=b_input_mask,
                    labels=b_labels
                )

        loss = outputs.loss
        logits = outputs.logits

        total_eval_loss += loss.item()

        logits = logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()
        preds = np.argmax(logits, axis=1).flatten()
        labels_flat = label_ids.flatten()
        total_eval_accuracy += np.sum(preds == labels_flat) / len(labels_flat)
        all_preds.extend(preds.tolist())
        all_labels.extend(labels_flat.tolist())

    avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
    avg_val_loss = total_eval_loss / len(validation_dataloader)
    validation_time = format_time(time.time() - t0)

    # Compute macro and weighted F1 across classes
    try:
        f1_macro = f1_score(all_labels, all_preds, average='macro')
        f1_weighted = f1_score(all_labels, all_preds, average='weighted')
    except Exception:
        f1_macro = 0.0
        f1_weighted = 0.0

    print(f"  Accuracy: {avg_val_accuracy:.2f}")
    print(f"  F1 (macro): {f1_macro:.2f}")
    print(f"  F1 (weighted): {f1_weighted:.2f}")
    print(f"  Validation Loss: {avg_val_loss:.2f}")
    print(f"  Validation took: {validation_time}")

    return avg_val_accuracy, avg_val_loss, validation_time, f1_macro, f1_weighted