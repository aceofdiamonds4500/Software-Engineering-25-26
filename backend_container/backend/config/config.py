"""Project configuration module"""


class TrainingConfig:
    """Training configuration parameters."""
    
    # Data paths
    DATA_PATH = 'backend/ai/training/train.csv'
    
    # Model configuration
    MODEL_NAME = 'bert-base-uncased'
    MODEL_TYPE = 'advanced'  # 'simple' or 'advanced'
    NUM_LABELS = 40
    MAX_LENGTH = 512
    
    # Layer freezing configuration (applies to both 'simple' and 'advanced' models)
    # FREEZE_LAYERS: Freeze BERT layers below this index (e.g., 7 freezes layers 0-6, unfreezes 7-11)
    # UNFREEZE_LAYERS: Override to unfreeze only specific layers (e.g., [9, 10, 11]). If None, uses FREEZE_LAYERS
    # UNFREEZE_POOLER: Whether to unfreeze the BERT pooler layer
    # UNFREEZE_EMBEDDINGS: Whether to unfreeze the BERT embeddings layer
    FREEZE_LAYERS = 9  # Keep more layers frozen to prevent overfitting
    UNFREEZE_LAYERS = None  # Set to [9, 10, 11] to unfreeze only those layers
    UNFREEZE_POOLER = True
    UNFREEZE_EMBEDDINGS = False
    
    # Training hyperparameters
    BATCH_SIZE = 48  # Larger batch for more stable gradients
    EPOCHS = 25  # More epochs, early stopping will kick in
    LEARNING_RATE_HEAD = 1e-4  # Smaller learning rate to prevent overfitting
    LEARNING_RATE_BERT = 2e-5  # Conservative BERT fine-tuning
    WEIGHT_DECAY = 0.01  # Stronger regularization to prevent overfitting
    LABEL_SMOOTHING = 0.1  # More label smoothing for regularization
    WARMUP_STEPS = None  # Will use 10% of total steps if None
    
    # Model parameters
    DROPOUT_RATE = 0.35  # Strong dropout to reduce overfitting
    USE_CLASS_WEIGHTS = True
    
    # Class imbalance handling
    FOCAL_LOSS_GAMMA = 2.0  # Higher gamma (2.0-3.0) focuses more on hard examples. Set higher if very imbalanced
    FOCAL_LOSS_ALPHA = 1.0  # Weight for focal loss
    RESAMPLE_MINORITY = True  # Oversample minority classes to balance (enable if imbalance ratio > 10x)
    RESAMPLE_MINORITY_RATIO = 0.7  # Resample minority to this ratio (0.7 = 70% of majority)
    
    # Pooling and head configuration
    USE_MULTI_POOLING = True  # Use CLS + Mean + Max pooling (vs just CLS)
    USE_ATTENTION_POOLING = False  # Use learned attention-based pooling (disables multi-pooling if True)
    
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
