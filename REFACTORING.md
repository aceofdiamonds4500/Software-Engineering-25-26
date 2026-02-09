# Medical Transcription Classification System - Refactored

## Project Organization

This project has been reorganized for clarity, maintainability, and best practices.

### Final Directory Structure

```
.
├── backend/                          # Backend services and AI
│   ├── ai/                          # AI/ML components
│   │   ├── data/                    # Data loading and preprocessing
│   │   │   ├── data_loader.py      # Dataset preparation, tokenization
│   │   │   ├── file_reader.py      # File I/O utilities
│   │   │   ├── preprocessing.py    # Text cleaning and preprocessing
│   │   │   └── __init__.py
│   │   ├── models/                  # Model definitions
│   │   │   ├── medical_bert.py     # BERT architectures (Simple, Advanced)
│   │   │   ├── model_utils.py      # Model utilities (save, load, summary)
│   │   │   └── __init__.py
│   │   ├── training/                # Training logic
│   │   │   ├── train.py            # Main training entry point
│   │   │   ├── trainer.py          # Training loop (train_epoch, validate)
│   │   │   └── __init__.py
│   │   ├── inference/               # Inference and predictions
│   │   │   ├── inference.py        # Prediction functions
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── database/                    # Database operations
│   │   ├── db_manager.py           # SQLite manager with C bindings
│   │   └── __init__.py
│   ├── server.py                    # Backend server (socket-based inference)
│   └── __init__.py
├── desktop/                         # Desktop app (C# WinForms)
│   └── *.cs, *.csproj
├── mobile/                          # Mobile app (Android)
│   └── app/
├── config/                          # Configuration
│   ├── config.py                   # TrainingConfig, InferenceConfig
│   └── __init__.py
├── scripts/                         # Utility scripts
│   ├── diagnose.py                 # System diagnostics
│   └── __init__.py
└── README.md, REFACTORING.md       # Documentation
```

## Key Changes

### 1. ✅ **Data Module Created** → `backend/ai/data/`
Previously scattered across `backend/ai/training/`, now properly organized:
- `data_loader.py` - Tokenization and DataLoader creation
- `file_reader.py` - CSV and file I/O
- `preprocessing.py` - Text cleaning

### 2. ✅ **Inference Renamed** → `backend/ai/inference/inference.py`
- Was: `backend/ai/inference/predictor.py`
- Now: `backend/ai/inference/inference.py`

### 3. ✅ **Scripts Isolated** → `scripts/`
- Was: `diagnose.py` (root level)
- Now: `scripts/diagnose.py`

### 4. ✅ **Training Streamlined** → `backend/ai/training/`
Now contains only training logic:
- `train.py` - Main entry point
- `trainer.py` - Training loop functions
- Data operations moved to `backend/ai/data/`


## New Import Paths

### Old → New Imports

```python
# Data
from data import load_medical_data                    
→ from backend.ai.data import load_medical_data

from data.data_loader import prepare_data             
→ from backend.ai.data import prepare_data

from data.preprocessing import preprocess_dataframe   
→ from backend.ai.data import preprocess_dataframe

# Models
from models import get_model                          
→ from backend.ai.models import get_model

# Training
from training.trainer import train_epoch              
→ from backend.ai.training import train_epoch

# Inference
from inference import predict                         
→ from backend.ai.inference import predict

# Configuration
from config import TrainingConfig                     
→ from config import TrainingConfig
```

## Module Organization Philosophy

### `backend/ai/data/` - Data Layer
- Loads and prepares data
- No ML logic, pure data operations
- Exports: `load_medical_data`, `prepare_data`, `preprocess_dataframe`

### `backend/ai/models/` - Model Layer
- Model architectures and utilities
- No training or inference logic
- Exports: `get_model`, `save_model`, `load_model`, `print_model_summary`

### `backend/ai/training/` - Training Layer
- Training orchestration and loops
- Uses data and models
- Exports: `train_epoch`, `validate`, `format_time`
- Entry point: `train.py`

### `backend/ai/inference/` - Inference Layer
- Prediction and inference
- Uses models
- Exports: `load_trained_model`, `predict`

### `backend/database/` - Database Layer
- Database operations
- C library bindings
- Exports: `DatabaseManager`

### `config/` - Configuration
- All configuration in one place
- Exports: `TrainingConfig`, `InferenceConfig`

### `scripts/` - Utilities
- Diagnostic tools
- Helper scripts
- Not part of main package

## Usage Examples

### Training
```bash
python -m backend.ai.training.train
```

```python
from backend.ai.data import load_medical_data, prepare_data
from backend.ai.training import train_epoch, validate
from backend.ai.models import get_model

# Load and prepare data
df = load_medical_data('mtsamples.csv')
train_loader, val_loader, tokenizer, labels = prepare_data(df)

# Create model
model = get_model('advanced')

# Train
train_loss, time = train_epoch(model, train_loader, ...)
val_acc, val_loss, _, _, _ = validate(model, val_loader, ...)
```

### Inference
```python
from backend.ai.inference import load_trained_model, predict

model, id_to_label = load_trained_model('./model_path')
label, confidence, topk = predict(text, model, tokenizer, id_to_label)
```

### Database
```python
from backend.database import DatabaseManager

db = DatabaseManager('./sqlite/data_control.so')
db.init()
db.insert_transcript(desc, specialty, name, transcription, keywords)
result = db.select_transcript(id)
db.close()
```

### Diagnostics
```bash
python scripts/diagnose.py
```

### Server
```bash
python backend/server.py
```

## Configuration

All configuration is centralized in `config/config.py`:

```python
from config import TrainingConfig, InferenceConfig

# Training parameters
config = TrainingConfig()
config.EPOCHS = 5
config.BATCH_SIZE = 32
config.MODEL_NAME = 'bert-base-uncased'

# Inference parameters  
infer_config = InferenceConfig()
infer_config.DEVICE = 'cuda'
```

## Migration Notes

- Old files in root (`models/`, `data/`, `training/`, etc.) have been moved
- Old `diagnose.py` → `scripts/diagnose.py`
- Old `inference.py` has been removed (use `backend/ai/inference/inference.py`)
- All imports updated to new paths
- C# and Android projects moved to `desktop/` and `mobile/`

## Next Steps

If you encounter import errors:
1. Ensure you're running from project root
2. Check module names in `backend/ai/*//__init__.py`
3. Verify dependencies: `torch`, `transformers`, `pandas`, `sklearn`
4. Use relative imports within packages: `from .module import func`
5. Use absolute imports from package root: `from backend.ai.data import func`

