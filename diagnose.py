"""
Comprehensive diagnostic to find the root cause
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import numpy as np
import pandas as pd
from data import load_medical_data, preprocess_dataframe
from config import TrainingConfig

print("="*80)
print("COMPREHENSIVE DIAGNOSTIC")
print("="*80)

config = TrainingConfig()

# Load data
print("\n1. Loading data...")
df = load_medical_data(config.DATA_PATH)
df = preprocess_dataframe(df, 'transcription', 'clean_transcription')

print(f"\nTotal samples: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Check class distribution
print("\n2. Class Distribution:")
print("="*80)
class_counts = df.medical_specialty.value_counts()
print(class_counts)

print(f"\nMost common: {class_counts.index[0]} ({class_counts.iloc[0]} samples)")
print(f"Least common: {class_counts.index[-1]} ({class_counts.iloc[-1]} samples)")
print(f"Imbalance ratio: {class_counts.iloc[0] / class_counts.iloc[-1]:.1f}:1")

# Check if we have exactly 40 classes
print(f"\n3. Number of unique specialties: {df.medical_specialty.nunique()}")
if df.medical_specialty.nunique() != 40:
    print(f"⚠️  WARNING: Expected 40 classes, found {df.medical_specialty.nunique()}")

# Check label encoding
print("\n4. Checking label encoding...")
from data.data_loader import serialize_specialty
label_dict = serialize_specialty(df)

print(f"\nNumber of labels: {len(label_dict)}")
print(f"Label IDs range: {df.specialty_id.min()} to {df.specialty_id.max()}")
print(f"Expected range: 0 to {len(label_dict)-1}")

if df.specialty_id.max() >= len(label_dict):
    print("⚠️  ERROR: Label IDs exceed number of classes!")

# Check text quality
print("\n5. Text Quality Check:")
print("="*80)
text_lengths = df.clean_transcription.str.len()
print(f"Text length stats:")
print(f"  Min: {text_lengths.min()}")
print(f"  Max: {text_lengths.max()}")
print(f"  Mean: {text_lengths.mean():.0f}")
print(f"  Median: {text_lengths.median():.0f}")

# Check for very short texts
short_texts = (text_lengths < 100).sum()
print(f"\nTexts < 100 chars: {short_texts} ({100*short_texts/len(df):.1f}%)")

# Sample some texts
print("\n6. Sample Texts:")
print("="*80)
for i in [0, 1, 2]:
    print(f"\nSample {i+1}:")
    print(f"  Specialty: {df.iloc[i]['medical_specialty']}")
    print(f"  Label ID: {df.iloc[i]['specialty_id']}")
    print(f"  Length: {len(df.iloc[i]['clean_transcription'])} chars")
    print(f"  Text preview: {df.iloc[i]['clean_transcription'][:200]}...")

# Test tokenization
print("\n7. Testing Tokenization:")
print("="*80)
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

sample_text = df.iloc[0]['clean_transcription']
encoded = tokenizer.encode_plus(
    sample_text,
    add_special_tokens=True,
    max_length=512,
    padding='max_length',
    truncation=True,
    return_attention_mask=True,
    return_tensors='pt'
)

input_ids = encoded['input_ids'][0]
attention_mask = encoded['attention_mask'][0]

non_padding = (input_ids != tokenizer.pad_token_id).sum().item()
print(f"Sample text tokens: {non_padding} / 512")
print(f"First 20 tokens: {input_ids[:20].tolist()}")

# Test model creation
print("\n8. Testing Model Creation:")
print("="*80)
from models import get_model

try:
    model = get_model(
        model_type='simple',
        num_labels=40,
        dropout_rate=0.2,
        class_weights=None
    )
    print("✓ Model created successfully")
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"\nModel parameters:")
    print(f"  Total: {total_params:,}")
    print(f"  Trainable: {trainable_params:,} ({100*trainable_params/total_params:.2f}%)")
    
except Exception as e:
    print(f"✗ Model creation failed: {e}")

# Test forward pass
print("\n9. Testing Forward Pass:")
print("="*80)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()

# Create test batch
test_input = encoded['input_ids'].to(device)
test_mask = encoded['attention_mask'].to(device)
test_label = torch.tensor([df.iloc[0]['specialty_id']]).to(device)

print(f"Test input shape: {test_input.shape}")
print(f"Test label: {test_label.item()}")

with torch.no_grad():
    outputs = model(test_input, attention_mask=test_mask, labels=test_label, label_smoothing=0.1)
    logits = outputs.logits
    loss = outputs.loss
    
    print(f"\nLogits shape: {logits.shape}")
    print(f"Loss: {loss.item():.4f}")
    
    # Check logit statistics
    print(f"\nLogit statistics:")
    print(f"  Min: {logits.min().item():.4f}")
    print(f"  Max: {logits.max().item():.4f}")
    print(f"  Mean: {logits.mean().item():.4f}")
    print(f"  Std: {logits.std().item():.4f}")
    
    # Check prediction
    pred = torch.argmax(logits, dim=1)
    print(f"\nPrediction: {pred.item()}")
    print(f"True label: {test_label.item()}")
    print(f"Match: {pred.item() == test_label.item()}")
    
    # Show top 5 predictions
    probs = torch.softmax(logits, dim=1)[0]
    top5_probs, top5_indices = torch.topk(probs, 5)
    
    print(f"\nTop 5 predictions:")
    for i, (prob, idx) in enumerate(zip(top5_probs, top5_indices)):
        print(f"  {i+1}. Class {idx.item()}: {prob.item():.4f}")

# Check class weights
print("\n10. Testing Class Weights:")
print("="*80)
from sklearn.utils.class_weight import compute_class_weight

labels = df.specialty_id.values
class_weights = compute_class_weight(
    'balanced',
    classes=np.arange(40),
    y=labels
)

# Check for extreme weights
print(f"Class weight statistics:")
print(f"  Min: {class_weights.min():.3f}")
print(f"  Max: {class_weights.max():.3f}")
print(f"  Mean: {class_weights.mean():.3f}")
print(f"  Std: {class_weights.std():.3f}")

if class_weights.max() > 50:
    print(f"⚠️  WARNING: Very high class weights detected (max={class_weights.max():.1f})")
    print("   This can cause training instability")

# Show classes with highest weights
top_weighted = np.argsort(class_weights)[-5:]
print(f"\nTop 5 weighted classes:")
for idx in top_weighted:
    specialty = [k for k, v in label_dict.items() if v == idx][0]
    count = class_counts[specialty]
    print(f"  Class {idx} ({specialty}): weight={class_weights[idx]:.3f}, count={count}")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)