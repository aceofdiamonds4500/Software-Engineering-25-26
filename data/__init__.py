"""
Data loading and preprocessing package.

This package handles all data-related operations including:
- Loading CSV files
- Text cleaning and preprocessing
- Tokenization for BERT
- Creating PyTorch data loaders
"""

from .file_reader import (
    pd_read,
    load_medical_data
)
from .preprocessing import (
    text_cleaner,
    insert_clean_column,
    clean_medical_text,
    preprocess_dataframe
)
from .data_loader import (
    serialize_specialty,
    tokenize_dataset,
    create_data_loaders,
    prepare_data
)

__version__ = '1.0.0'

__all__ = [
    # File reading
    'pd_read',
    'load_medical_data',
    
    # Text preprocessing
    'text_cleaner',
    'insert_clean_column',
    'clean_medical_text',
    'preprocess_dataframe',
    
    # Data loading and tokenization
    'serialize_specialty',
    'tokenize_dataset',
    'create_data_loaders',
    'prepare_data'
]