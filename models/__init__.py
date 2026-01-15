"""
Models package for medical text classification.

This package contains BERT-based neural network models for classifying
medical transcriptions into different medical specialties.
"""

from .medical_bert import (
    MedicalBertClassifierAdvanced,
    SimpleMedicalBert,
    get_model
)
from .model_utils import (
    count_parameters,
    print_model_summary,
    save_model,
    load_model
)

__version__ = '1.0.0'

__all__ = [
    # Model classes
    'MedicalBertClassifierAdvanced',
    'SimpleMedicalBert',
    'get_model',
    
    # Model utilities
    'count_parameters',
    'print_model_summary',
    'save_model',
    'load_model'
]