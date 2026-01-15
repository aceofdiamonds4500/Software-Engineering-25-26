"""
Training utilities package.

This package contains all training-related functions including:
- Training loop for single epoch
- Validation/evaluation
- Accuracy calculation
- Time formatting utilities
"""

from .trainer import (
    train_epoch,
    validate,
    flat_accuracy,
    format_time
)

__version__ = '1.0.0'

__all__ = [
    'train_epoch',
    'validate',
    'flat_accuracy',
    'format_time'
]