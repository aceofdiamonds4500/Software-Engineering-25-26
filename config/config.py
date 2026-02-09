"""Project configuration module"""


class TrainingConfig:
    """Training configuration parameters."""
    
    # Data paths
    DATA_PATH = 'mtsamples.csv'
    
    # Model configuration
    MODEL_NAME = 'bert-base-uncased'
    MODEL_TYPE = 'advanced'  # 'simple' or 'advanced'
    NUM_LABELS = 40
    MAX_LENGTH = 512
    FREEZE_LAYERS = 9
    
    # Training hyperparameters
    BATCH_SIZE = 16
    EPOCHS = 9
    LEARNING_RATE_HEAD = 1e-3
    LEARNING_RATE_BERT = 1e-5
    WEIGHT_DECAY = 0.01
    LABEL_SMOOTHING = 0.1
    WARMUP_STEPS = None  # Will use 10% of total steps if None
    
    # Model parameters
    DROPOUT_RATE = 0.4
    USE_CLASS_WEIGHTS = True
    
    # Training settings
    USE_CUDA = True
    SEED = 42
    
    # Checkpoint and save settings
    SAVE_DIR = './medical_classification_model'
    CHECKPOINT_DIR = './checkpoints'
    SAVE_CHECKPOINTS = True
    SAVE_BEST = True


class InferenceConfig:
    """Inference configuration parameters."""
    
    MODEL_PATH = "./medical_classification_model"
    MODEL_NAME = "bert-base-uncased"
    MAX_LENGTH = 512
    DEVICE = "cuda"  # or "cpu"
