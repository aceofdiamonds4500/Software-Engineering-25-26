"""Inference module for making predictions with trained models."""
import torch
from transformers import AutoTokenizer
import os
import json
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from backend.ai.models import get_model

try:
    from config.config import InferenceConfig, TrainingConfig
except ImportError:
    class InferenceConfig:
        MODEL_PATH = "./medical_classification_model"
        MODEL_NAME = "bert-base-uncased"
    class TrainingConfig:
        MODEL_NAME = "bert-base-uncased"
        MAX_LENGTH = 512


def load_trained_model(model_path, device='cuda'):
    """Load a trained model."""
    checkpoint = torch.load(
        f"{model_path}/pytorch_model.bin",
        map_location=device
    )
    
    with open(f"{model_path}/label_mapping.json", 'r') as f:
        label_dict = json.load(f)
    num_labels = len(label_dict)
    
    if os.path.isdir(f"{model_path}/encoder_base"):
        model_dir = f"{model_path}/encoder_base"
    elif os.path.isdir(f"{model_path}/bert_base"):
        model_dir = f"{model_path}/bert_base"
    else:
        model_dir = None

    model_name = model_dir if model_dir else 'bert-base-uncased'

    try:
        cfg_path = os.path.join(model_dir, 'config.json') if model_dir else None
        if cfg_path and os.path.isfile(cfg_path):
            with open(cfg_path, 'r', encoding='utf-8') as f:
                enc_cfg = json.load(f)
            model_type = enc_cfg.get('model_type')
            architectures = enc_cfg.get('architectures', [])
            if (model_type and 'roberta' in model_type.lower()) or any('Roberta' in a for a in architectures):
                if 'roberta' in TrainingConfig.MODEL_NAME.lower():
                    model_name = TrainingConfig.MODEL_NAME
    except Exception:
        pass
    
    model_type = checkpoint['model_config'].get('model_type', 'MedicalBertClassifierAdvanced')
    if 'Advanced' in model_type:
        model = get_model('advanced', num_labels=num_labels, model_name=model_name)
    else:
        model = get_model('simple', num_labels=num_labels, model_name=model_name)
    
    model.load_state_dict(checkpoint['model_state_dict'], strict=False)
    model.to(device)
    model.eval()
    
    id_to_label = {v: k for k, v in label_dict.items()}
    
    return model, id_to_label


def predict(text, model, tokenizer, id_to_label, device='cuda', max_length=512):
    """Make a prediction for a single text."""
    encoded = tokenizer(
        text,
        add_special_tokens=True,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    
    input_ids = encoded['input_ids'].to(device)
    attention_mask = encoded['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
    
    probs = torch.softmax(logits, dim=1)
    confidence, predicted_id = torch.max(probs, dim=1)

    predicted_label = id_to_label[predicted_id.item()]
    confidence_score = confidence.item()

    k = min(5, probs.size(1))
    top_probs, top_ids = torch.topk(probs, k=k, dim=1)
    topk = [(id_to_label[top_ids[0, i].item()], top_probs[0, i].item()) for i in range(k)]

    return predicted_label, confidence_score, topk


def main():
    """Example usage."""
    config = InferenceConfig()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    print("Loading model...")
    model, id_to_label = load_trained_model(config.MODEL_PATH, device)
    
    def _has_tokenizer_files(path: str) -> bool:
        candidates = [
            'tokenizer.json',
            'vocab.json',
            'vocab.txt',
            'merges.txt',
        ]
        return any(os.path.isfile(os.path.join(path, f)) for f in candidates)

    local_tokenizer_dir = None
    if os.path.isdir(f"{config.MODEL_PATH}/encoder_base"):
        local_tokenizer_dir = f"{config.MODEL_PATH}/encoder_base"
    elif os.path.isdir(f"{config.MODEL_PATH}/bert_base"):
        local_tokenizer_dir = f"{config.MODEL_PATH}/bert_base"

    if local_tokenizer_dir and _has_tokenizer_files(local_tokenizer_dir):
        tokenizer = AutoTokenizer.from_pretrained(local_tokenizer_dir, use_fast=True)
    else:
        inferred_name = None
        model_type = None
        cfg_path = os.path.join(local_tokenizer_dir, 'config.json') if local_tokenizer_dir else None
        if cfg_path and os.path.isfile(cfg_path):
            try:
                with open(cfg_path, 'r', encoding='utf-8') as f:
                    enc_cfg = json.load(f)
                inferred_name = enc_cfg.get('name_or_path')
                model_type = enc_cfg.get('model_type')
            except Exception:
                pass

        tokenizer = None
        if inferred_name:
            try:
                tokenizer = AutoTokenizer.from_pretrained(inferred_name, use_fast=True)
            except Exception:
                tokenizer = None

        if tokenizer is None and model_type:
            try:
                if model_type in ('roberta', 'xlm-roberta'):
                    if 'roberta' in getattr(config, 'MODEL_NAME', '').lower():
                        tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME, use_fast=True)
                    else:
                        tokenizer = AutoTokenizer.from_pretrained('roberta-base', use_fast=True)
                elif model_type == 'bert':
                    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=True)
            except Exception:
                tokenizer = None

        if tokenizer is None:
            try:
                tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME, use_fast=True)
            except Exception:
                tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=True)
    
    sample_text = """Description: Medical sample text here."""
    predicted_label, confidence, topk = predict(
        sample_text, model, tokenizer, id_to_label, device, max_length=TrainingConfig.MAX_LENGTH
    )
    
    print(f"\nPredicted Specialty: {predicted_label}")
    print(f"Confidence: {confidence:.2%}")
    print("Top-5 candidates:")
    for lbl, prob in topk:
        print(f"  - {lbl}: {prob:.2%}")


if __name__ == "__main__":
    main()
