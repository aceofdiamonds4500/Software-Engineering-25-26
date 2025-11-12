"""
Inference script for making predictions with trained model
"""
import torch
from transformers import AutoTokenizer
import os
import json
from models.medical_bert import get_model
from config.config import InferenceConfig, TrainingConfig


def load_trained_model(model_path, device='cuda'):
    """Load a trained model."""
    # Load checkpoint
    checkpoint = torch.load(
        f"{model_path}/pytorch_model.bin",
        map_location=device
    )
    
    # Load label mapping and derive num_labels
    with open(f"{model_path}/label_mapping.json", 'r') as f:
        label_dict = json.load(f)
    num_labels = len(label_dict)
    
    # Prefer loading encoder directly from saved directory (local path)
    if os.path.isdir(f"{model_path}/encoder_base"):
        model_dir = f"{model_path}/encoder_base"
    elif os.path.isdir(f"{model_path}/bert_base"):
        model_dir = f"{model_path}/bert_base"
    else:
        model_dir = None

    # Default model name to local dir or a safe fallback
    model_name = model_dir if model_dir else 'bert-base-uncased'

    # If the saved encoder config indicates RoBERTa, prefer the training-time RoBERTa name
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
    
    # Create model with proper parameters
    model_type = checkpoint['model_config'].get('model_type', 'MedicalBertClassifierAdvanced')
    if 'Advanced' in model_type:
        model = get_model('advanced', num_labels=num_labels, model_name=model_name)
    else:
        model = get_model('simple', num_labels=num_labels, model_name=model_name)
    
    # Allow extra buffers like class_weights and ensure compatibility
    model.load_state_dict(checkpoint['model_state_dict'], strict=False)
    model.to(device)
    model.eval()
    
    # Reverse mapping (id -> label)
    id_to_label = {v: k for k, v in label_dict.items()}
    
    return model, id_to_label


def predict(text, model, id_to_label, tokenizer, device='cuda', max_length=512):
    """
    Make a prediction for a single text.
    
    Args:
        text: Input text string
        model: Trained model
        tokenizer: BERT tokenizer
        id_to_label: Dictionary mapping IDs to label names
        device: Device to run on
        max_length: Maximum sequence length
    
    Returns:
        predicted_label, confidence_score
    """
    # Tokenize
    encoded = tokenizer.encode_plus(
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
    
    # Predict
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
    
    # Get prediction
    probs = torch.softmax(logits, dim=1)
    confidence, predicted_id = torch.max(probs, dim=1)

    predicted_label = id_to_label[predicted_id.item()]
    confidence_score = confidence.item()

    # Top-k for diagnostics
    k = min(5, probs.size(1))
    top_probs, top_ids = torch.topk(probs, k=k, dim=1)
    topk = [(id_to_label[top_ids[0, i].item()], top_probs[0, i].item()) for i in range(k)]

    return predicted_label, confidence_score, topk


def main():
    """Example usage."""
    config = InferenceConfig()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load model
    print("Loading model...")
    model, id_to_label = load_trained_model(config.MODEL_PATH, device)
    # Load tokenizer to match the encoder architecture
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
        # Try to infer tokenizer from the saved encoder config
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
        # First preference: inferred name_or_path from encoder config
        if inferred_name:
            try:
                tokenizer = AutoTokenizer.from_pretrained(inferred_name, use_fast=True)
            except Exception:
                tokenizer = None

        # Second preference: choose a default based on model_type
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

        # Final fallback: use configured MODEL_NAME, else BERT base
        if tokenizer is None:
            try:
                tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME, use_fast=True)
            except Exception:
                tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=True)
    
    # Example prediction
    sample_text = """
Description: Obesity hypoventilation syndrome. A 61-year-old woman with a history of polyarteritis nodosa, mononeuritis multiplex involving the lower extremities, and severe sleep apnea returns in followup following an overnight sleep study.
(Medical Transcription Sample Report)
HISTORY OF PRESENT ILLNESS: This is a 61-year-old woman with a history of polyarteritis nodosa, mononeuritis multiplex involving the lower extremities, and severe sleep apnea returns in followup following an overnight sleep study, on CPAP and oxygen to evaluate her for difficulty in initiating and maintaining sleep. She returns today to review results of an inpatient study performed approximately two weeks ago.

In the meantime, the patient reports she continues on substantial doses of opiate medication to control leg pain from mononeuritis multiplex.

She also takes Lasix for lower extremity edema.

The patient reports that she generally initiates sleep on CPAP, but rips her mask off, tosses and turns throughout the night and has "terrible quality sleep."

MEDICATIONS: Current medications are as previously noted. Changes include reduction in prednisone from 9 to 6 mg by mouth every morning. She continues to take Ativan 1 mg every six hours as needed. She takes imipramine 425 mg at bedtime.

Her MS Contin dose is 150 mg every 8 to 12 hours and an immediate release morphine preparation, 45 to 75 mg by mouth every 8 hours as needed.

FINDINGS: Vital signs: Blood pressure 153/81, pulse 90, respiratory rate 20, weight 311.8 pounds (up 10 pounds from earlier this month), height 5 feet 6 inches, temperature 98.4 degrees, SaO2 is 88% on room air at rest. Chest is clear. Extremities show lower extremity pretibial edema with erythema.

LABORATORIES: An arterial blood gas on room air showed a pH of 7.38, PCO2 of 52, and PO2 of 57.

CPAP compliance monitoring over the past two to three weeks showed average use of 3 hours 26 minutes on nights used. She used it for greater than 4 hours per night on 67% of night surveyed. Her estimated apnea/hypopnea index was 3 per hour. Her average leak flow was 67 liters per minute.

The patient's overnight sleep study was performed as an inpatient sleep study during a routine hospitalization for intravenous gamma globulin therapy. She slept for a total sleep time of 257 minutes out of 272 minutes in bed (sleep efficiency approximately 90%). Sleep stage distribution was relatively normal with 2% stage I, 72% stage II, 24% stage III, IV, and 2% stage REM sleep.

There were no periodic limb movements during sleep.

There was evidence of a severe predominantly central sleep apnea during non-REM sleep at 173 episodes per hour and during REM sleep at 77 episodes per hour. Oxyhemoglobin saturations during non-REM sleep fluctuated from the baseline of 92% to an average low of 82%. During REM sleep, the baseline oxyhemoglobin saturation was 87% , decreased to 81% with sleep-disordered breathing episodes.

Of note, the sleep study was performed on CPAP at 10.5 cm of H2O with oxygen at 8 liters per minute.

ASSESSMENT:
1. Obesity hypoventilation syndrome. The patient has evidence of a well-compensated respiratory acidosis, which is probably primarily related to severe obesity. In addition, there may be contribution from large doses of opiates and standing doses of gabapentin.
2. Severe central sleep apnea, on CPAP at 10 cmH2O and supplemental oxygen at 8 liters per minute. The breathing pattern is that of cluster or Biot's breathing throughout sleep. The primary etiology is probably opiate use, with contribution with further exacerbation by severe obesity which acts to lower the baseline oxyhemoglobin saturation, and worsen desaturations during apneic episodes.
3. Mononeuritis multiplex with pain requiring significant substantial doses of analgesia.
4. Hypoxemia primarily due to obesity, hypoventilation, and presumably basilar atelectasis and a combination of V/Q mismatch and shunt on that basis.

PLANS: My overall impression is that we should treat this patient's sleep disruption with measures to decrease central sleep apnea during sleep. These will include, (1). Decrease in evening doses of MS Contin, (2). Modest weight loss of approximately 10 to 20 pounds, and (3). Instituting Automated Servo Ventilation via nasal mask. With regard to latter, the patient will be returning for a trial of ASV to examine its effect on sleep-disordered breathing patterns.

In addition, the patient will benefit from modest diuresis, with improvement of oxygenation, as well as nocturnal desaturation and oxygen requirements. I have encouraged the patient to increase her dose of Lasix from 100 to 120 mg by mouth every morning as previously prescribed. I have also asked her to add Lasix in additional late afternoon to evening dose of Lasix at 40 mg by mouth at that time. She was instructed to take between one and two K-Tab with her evening dose of Lasix (10 to 20 mEq).

In addition, we will obtain a complete set of pulmonary function studies to evaluate this patient for underlying causes of parenchymal lung disease that may interfere with oxygenation. Further workup for hypoxemia may include high-resolution CT scanning if evidence for significant pulmonary restriction and/or reductions in diffusion capacity is evident on pulmonary function testing.
    """
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