# Medical Specialty Classification

Modern, encoder-agnostic text classification for medical transcriptions using Hugging Face Transformers. This project trains a classifier to map each transcription to a medical specialty and provides an inference script for predictions.

## Overview

- `AutoModel`/`AutoTokenizer` (e.g., `allenai/biomed_roberta_base`, ClinicalBERT, BERT).
- Two classifier heads:
  - Advanced: partially fine-tunes last layers and trains a deeper head.
  - Simple: freezes the encoder and trains a lightweight head.
- Pooling: automatically falls back to masked mean when an encoder lacks `pooler_output`.
- Class-imbalance handling using Focal Loss, Class Weights, and Label Smoothing.
- Deterministic label mapping by sorting specialties.

## Project Structure

```
.
├── backend/                          # Backend services and AI
│   ├── ai/                          # AI/ML components
│   │   ├── data/                    # Data loading and preprocessing
│   │   │   ├── data_loader.py
│   │   │   ├── file_reader.py
│   │   │   ├── preprocessing.py
│   │   │   └── __init__.py
│   │   ├── models/                  # Model definitions
│   │   │   ├── medical_bert.py
│   │   │   ├── model_utils.py
│   │   │   └── __init__.py
│   │   ├── training/                # Training logic
│   │   │   ├── train.py
│   │   │   ├── trainer.py
│   │   │   └── __init__.py
│   │   ├── inference/               # Inference and predictions
│   │   │   ├── inference.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── database/                    # Database operations
│   │   ├── 
│   │   └── __init__.py
│   ├── controller.py                # Backend inference server
│   └── __init__.py
├── config/                          # Configuration
│   ├── config.py
│   └── __init__.py
├── scripts/                         # Utility scripts
│   ├── diagnose.py                 # System diagnostics
│   └── __init__.py
├── desktop/                         # Desktop GUI (C# WinForms)
├── mobile/                          # Mobile app (Android)
└── README.md, REFACTORING.md
```

**See [REFACTORING.md](REFACTORING.md) for detailed migration information.**

## Requirements

- Python 3.10+ (tested with 3.11)
- PyTorch (CUDA recommended)
- Transformers
- scikit-learn
- pandas, numpy

Install dependencies:

If a `requirements.txt` is not present, install directly:

```bash
pip install torch transformers scikit-learn pandas numpy
```

## Configuration

All configuration is centralized in `config/config.py`:

```python
from config import TrainingConfig, InferenceConfig
```

- `TrainingConfig`
  - `MODEL_NAME`: Encoder to use (e.g., `bert-base-uncased`, `allenai/biomed_roberta_base`).
  - `MAX_LENGTH`: Tokenizer sequence length (e.g., 512).
  - `EPOCHS`: Training epochs.
  - `MODEL_TYPE`: `simple` or `advanced`.
  - `NUM_LABELS`: Number of specialties (40 by default).
  - `DROPOUT_RATE`, `LABEL_SMOOTHING`, and other training hyperparameters.
  - `FREEZE_LAYERS` (advanced model): Number of early encoder layers to freeze.

- `InferenceConfig`
  - `MODEL_PATH`: Directory containing a trained checkpoint (e.g., `./medical_classification_model`).
  - `MAX_LENGTH`: Inference tokenization length.

## Data Pipeline

- Input CSV: `mtsamples.csv` (or your own, with `text` and `medical_specialty` columns after preprocessing).
- Label mapping:
  - Mapped by sorted unique specialties.
  - Saved to `label_mapping.json` alongside checkpoints.
- Tokenization:
  - `AutoTokenizer.from_pretrained(TrainingConfig.MODEL_NAME)` for training.
  - Encodes text to `input_ids` and `attention_mask` only (no `token_type_ids` needed for RoBERTa).

## Models

- Encoders loaded via `AutoModel.from_pretrained(MODEL_NAME)`.
- Pooling:
  - Uses `outputs.pooler_output` when present.
  - Falls back to masked mean of `last_hidden_state` when not.
- Loss:
  - Focal Loss (`alpha`, `gamma`) with optional class weights and label smoothing.

### Advanced Classifier

- Freezes early encoder layers; fine-tunes the last layers. (Last 3 layers)
- Custom classification head with batch normalization, ReLU, and dropout.

### Simple Classifier

- Freezes the entire encoder; trains a small classification head.

## Training

Run training:

```bash
python -m backend.ai.training.train
```

Or from Python:

```python
from backend.ai.data import load_medical_data, prepare_data
from backend.ai.training import train_epoch, validate
from backend.ai.models import get_model

# Load and prepare data
df = load_medical_data('mtsamples.csv')
train_loader, val_loader, tokenizer, labels = prepare_data(df)

# Create model
model = get_model('advanced', num_labels=40)

# Train
train_loss, time = train_epoch(model, train_loader, ...)
val_acc, val_loss, _, _, _ = validate(model, val_loader, ...)
```

During training:
- Loads `TrainingConfig`, tokenizer, and builds the chosen model.
- Trains for `EPOCHS` with mixed precision on CUDA when available.
- Saves checkpoints to `checkpoints/epoch_X/` and selects `checkpoints/best/`.
- Saves:
  - `pytorch_model.bin`: model weights plus config summary.
  - `encoder_base/`: the encoder (tokenizer and model files) for portable inference.
  - `label_mapping.json`: mapping of specialty name → id.

Tips:
- If GPU memory is limited, reduce `MAX_LENGTH` or batch size.
- For imbalanced classes, tune focal loss `gamma` and use class weights.
- Advanced model: experiment with `FREEZE_LAYERS` to balance speed and quality.

## Evaluation

During training and validation the script reports:
- Accuracy: overall fraction of correct predictions.
- F1 Macro: averaged F1 across classes (treats each class equally).
- F1 Weighted: weighted by support (more influenced by frequent classes).

Key notes for training:
- Prefer F1 Macro when class balance/fairness matters.
- Accuracy can drop while F1 Macro improves if minority classes get better.

## Inference

Make a single prediction:

```bash
python -m backend.ai.inference.inference
```

How it works:
- Loads the checkpoint from `InferenceConfig.MODEL_PATH`.
- Builds the model with the correct `num_labels` and encoder `name_or_path`.
- Loads the tokenizer from `encoder_base` (fallback: `bert_base`, then default).
- Tokenizes the input, runs the model, and returns the predicted specialty with confidence.

Usage:

```python
from backend.ai.inference import load_trained_model, predict
from transformers import AutoTokenizer
import torch

model_path = "checkpoints/best"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model, id_to_label = load_trained_model(model_path, device)
tokenizer = AutoTokenizer.from_pretrained(f"{model_path}/encoder_base")

text = "Patient presents with shortness of breath and wheezing."
label, confidence, topk = predict(text, model, tokenizer, id_to_label, device)
print(f"Predicted: {label}")
print(f"Confidence: {confidence:.2%}")
print("Top-5 candidates:")
for lbl, prob in topk:
    print(f"  - {lbl}: {prob:.2%}")
```

```

## Diagnostics

Run system diagnostics to validate the setup:

```bash
python scripts/diagnose.py
```

This script checks:
- ✅ Data loading and preprocessing
- ✅ Class distribution and imbalance
- ✅ Label encoding
- ✅ Text quality
- ✅ Tokenization
- ✅ Model creation
- ✅ Forward pass
- ✅ Class weights

## Reproducibility

- Label mapping is deterministic by sorting specialties.
- Checkpoints include encoder files to ensure consistent tokenization.
- For exact repeatability, fix random seeds and environment settings.

## Troubleshooting

- **Import errors**: Ensure you're running from the project root. Check [REFACTORING.md](REFACTORING.md) for new import paths.
- **Tokenizer not found**: Ensure `encoder_base/` exists under your checkpoint; otherwise the script falls back to `bert_base/` or a default model.
- **CUDA OOM**: Lower `MAX_LENGTH` or batch size; consider gradient accumulation.
- **Poor F1**: Try a domain-specific encoder (e.g., biomedical models), tune `gamma`, or increase `EPOCHS`.
- **Module not found**: Make sure all packages in `backend/ai/*/` have `__init__.py` files.

## Notes

- Default encoder in `config/config.py` is `bert-base-uncased`.
- The training loop removes `token_type_ids` to support models that do not use them.
- For detailed refactoring information, see [REFACTORING.md](REFACTORING.md).
- Desktop GUI is in `desktop/` (C# WinForms).
- Mobile app is in `mobile/app/` (Android/Gradle).
- All utility scripts are in `scripts/`.