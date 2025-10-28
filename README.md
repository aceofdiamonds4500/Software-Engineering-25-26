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

- `config/`: Training and inference configuration.
- `data/`: Reading, preprocessing, tokenization, and labeling.
- `models/`: Classifiers and utilities for saving/loading.
- `training/`: Training loop.
- `inference.py`: Loads a trained checkpoint and makes predictions.
- `diagnose.py`: Optional helpers/debugging.

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

Key options in `config/config.py`.

- `TrainingConfig`
  - `MODEL_NAME`: Encoder to use (e.g., `allenai/biomed_roberta_base`).
  - `MAX_LENGTH`: Tokenizer sequence length (e.g., 512).
  - `EPOCHS`: Training epochs.
  - `MODEL_TYPE`: `simple` or `advanced`.
  - `NUM_LABELS`: Number of specialties (set at runtime using dataset mapping).
  - `DROPOUT_RATE`, `LABEL_SMOOTHING`, and other training hyperparameters.
  - `FREEZE_LAYERS` (advanced model): Number of early encoder layers to freeze.

- `InferenceConfig`
  - `MODEL_PATH`: Directory containing a trained checkpoint (e.g., `checkpoints/best`).
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
python training/train.py
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
python inference.py
```

How it works:
- Loads the checkpoint from `InferenceConfig.MODEL_PATH`.
- Builds the model with the correct `num_labels` and encoder `name_or_path`.
- Loads the tokenizer from `encoder_base` (fallback: `bert_base`, then default).
- Tokenizes the input, runs the model, and returns the predicted specialty with confidence.

Programmatic usage:

```python
from inference import load_trained_model, predict
from transformers import AutoTokenizer
import torch

model_path = "checkpoints/best"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model, id_to_label = load_trained_model(model_path, device)
tokenizer = AutoTokenizer.from_pretrained(f"{model_path}/encoder_base")

text = "Patient presents with shortness of breath and wheezing."
label, conf = predict(text, model, tokenizer, id_to_label, device)
print(label, conf)
```

## Reproducibility

- Label mapping is deterministic by sorting specialties.
- Checkpoints include encoder files to ensure consistent tokenization.
- For exact repeatability, fix random seeds and environment settings.

## Troubleshooting

- "Tokenizer not found": ensure `encoder_base/` exists under your checkpoint; otherwise the script falls back to `bert_base/` or a default model.
- CUDA OOM: lower `MAX_LENGTH` or batch size; consider gradient accumulation.
- Poor F1: try a domain-specific encoder (e.g., biomedical models), tune `gamma`, or increase `EPOCHS`.

## Notes

- Current default encoder in `config/config.py` is `allenai/biomed_roberta_base`.
- The training loop removes `token_type_ids` to support models that do not use them.