"""
Data loading and preprocessing
"""
import torch
from torch.utils.data import TensorDataset, random_split, DataLoader, RandomSampler, SequentialSampler, WeightedRandomSampler
from transformers import AutoTokenizer
import json
import os
import numpy as np
from config.config import TrainingConfig


def serialize_specialty(df, save_dir='./medical_classification_model'):
    """
    Convert medical specialty names to numerical IDs.
    
    Args:
        df: DataFrame with 'medical_specialty' column
        save_dir: Directory to save label mapping
    
    Returns:
        label_dict: Dictionary mapping specialty names to IDs
    """
    possible_labels = df.medical_specialty.unique()
    label_dict = {}                  
    
    print("\nMapping medical specialties to IDs:")
    for i, possible_label in enumerate(possible_labels):
        print(f"  {i:2d}: {possible_label}")
        label_dict[possible_label] = i
    
    df['specialty_id'] = df.medical_specialty.replace(label_dict)
    
    # Save label mapping
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'label_mapping.json'), 'w') as f:
        json.dump(label_dict, f, indent=2)
    
    print(f"Saved label mapping to {save_dir}/label_mapping.json")
    
    return label_dict


def tokenize_dataset(sentences, labels, tokenizer, max_length=512):
    """
    Tokenize dataset for BERT.
    
    Args:
        sentences: List of text strings
        labels: List of label IDs
        tokenizer: BERT tokenizer
        max_length: Maximum sequence length
    
    Returns:
        input_ids, attention_masks, labels as tensors
    """
    print(f"\nTokenizing {len(sentences)} samples...")
    
    input_ids = []
    attention_masks = []
    
    for i, text in enumerate(sentences):
        if i % 500 == 0 and i > 0:
            print(f"  Tokenized {i}/{len(sentences)} samples...")
            
        encode_dict = tokenizer.encode_plus(
            text, 
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encode_dict['input_ids'])
        attention_masks.append(encode_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels = torch.tensor(labels, dtype=torch.long)

    print(f"\nTokenization complete!")
    print(f"Example sentence: {sentences[1][:100]}...")
    print(f"Token IDs shape: {input_ids[1].shape}")
    
    return input_ids, attention_masks, labels


def create_data_loaders(input_ids, attention_masks, labels, batch_size=16, train_split=0.8):
    """
    Create training and validation data loaders.
    
    Args:
        input_ids: Tokenized input IDs
        attention_masks: Attention masks
        labels: Labels
        batch_size: Batch size for training
        train_split: Proportion of data for training
    
    Returns:
        train_dataloader, validation_dataloader
    """
    dataset = TensorDataset(input_ids, attention_masks, labels)

    train_size = int(train_split * len(dataset))
    validation_size = len(dataset) - train_size

    train_dataset, validation_dataset = random_split(
        dataset, 
        [train_size, validation_size]
    )
    
    print(f'\n{train_size:>5,} training samples')
    print(f'{validation_size:>5,} validation samples')

    # Create weighted sampler for balanced training batches
    train_labels = [labels[i] for i in train_dataset.indices]
    class_counts = np.bincount(train_labels)
    class_weights = 1.0 / class_counts
    sample_weights = [class_weights[label] for label in train_labels]
    
    print(f"Class distribution in training set:")
    for i, count in enumerate(class_counts):
        print(f"  Class {i}: {count} samples (weight: {class_weights[i]:.4f})")
    
    weighted_sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True
    )

    # Windows shared-memory can be unstable with >0 workers; use 0 for stability
    num_workers = 0
    pin_memory = torch.cuda.is_available()
    train_dataloader = DataLoader(
        train_dataset,
        sampler=weighted_sampler,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory
    )

    validation_dataloader = DataLoader(
        validation_dataset,
        sampler=SequentialSampler(validation_dataset),
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory
    )
    
    return train_dataloader, validation_dataloader


def prepare_data(df, text_column='clean_transcription', batch_size=16, max_length=512):
    """
    Complete data preparation pipeline.
    
    Args:
        df: DataFrame with text and labels
        text_column: Name of column containing text
        batch_size: Batch size for data loaders
        max_length: Maximum sequence length for tokenization
    
    Returns:
        train_dataloader, validation_dataloader, tokenizer, label_dict
    """
    print("\n" + "="*80)
    print("DATA PREPARATION PIPELINE")
    print("="*80)
    
    # Serialize labels
    label_dict = serialize_specialty(df)
    
    # Get data
    sentences = df[text_column].values
    labels = df.specialty_id.values
    
    # Tokenize
    print("\nLoading tokenizer...")
    cfg = TrainingConfig()
    tokenizer = AutoTokenizer.from_pretrained(cfg.MODEL_NAME)
    input_ids, attention_masks, labels = tokenize_dataset(
        sentences, labels, tokenizer, max_length
    )
    
    # Create data loaders
    print("\nCreating data loaders...")
    train_dataloader, validation_dataloader = create_data_loaders(
        input_ids, attention_masks, labels, batch_size
    )
    
    print("="*80 + "\n")
    
    return train_dataloader, validation_dataloader, tokenizer, label_dict