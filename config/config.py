"""
Configuration settings for training
"""


class TrainingConfig:
    """Training hyperparameters and settings."""
    
    # Model settings
    MODEL_TYPE = 'advanced'  # 'simple' or 'advanced'
    # Hugging Face model name; swap to try different encoders
    MODEL_NAME = 'allenai/biomed_roberta_base'
    NUM_LABELS = 40
    DROPOUT_RATE = 0.4
    FREEZE_LAYERS = 9  # For advanced model
    
    # Class weights and label smoothing
    USE_CLASS_WEIGHTS = True
    LABEL_SMOOTHING = 0.05
    
    # Training settings
    BATCH_SIZE = 32
    EPOCHS = 16
    LEARNING_RATE_HEAD = 4e-4
    LEARNING_RATE_BERT = 5e-6
    WEIGHT_DECAY = 0.01
    WARMUP_STEPS = 0
    MAX_GRAD_NORM = 1.0

    # Checkpointing
    SAVE_CHECKPOINTS = True
    CHECKPOINT_DIR = './checkpoints'
    SAVE_BEST = True
    
    # Scheduler settings
    SCHEDULER_STEP_SIZE = 2
    SCHEDULER_GAMMA = 0.8
    
    # Data settings
    MAX_LENGTH = 512
    TRAIN_SPLIT = 0.8
    
    # Paths
    DATA_PATH = 'mtsamples.csv'
    SAVE_DIR = './medical_classification_model'
    
    # Random seed
    SEED = 456
    
    # Device
    USE_CUDA = True


class InferenceConfig:
    """Configuration for inference/prediction."""
    
    MODEL_PATH = './medical_classification_model'
    BATCH_SIZE = 32
    MAX_LENGTH = 256