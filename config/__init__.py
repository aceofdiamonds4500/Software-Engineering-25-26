"""
Configuration package.

This package contains configuration classes for training and inference.
Modify these to change hyperparameters, paths, and other settings.
"""

from .config import (
    TrainingConfig,
    InferenceConfig
)

__version__ = '1.0.0'

__all__ = [
    'TrainingConfig',
    'InferenceConfig'
]