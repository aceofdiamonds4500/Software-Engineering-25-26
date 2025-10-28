"""
Medical BERT Classification Models
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel


class FocalLoss(nn.Module):
    """
    Focal Loss implementation for handling class imbalance and hard examples.
    
    Args:
        alpha: Weighting factor for rare class (default: 1.0)
        gamma: Focusing parameter to down-weight easy examples (default: 2.0)
        weight: Class weights tensor (optional)
        label_smoothing: Label smoothing factor (default: 0.0)
    """
    def __init__(self, alpha=1.0, gamma=2.0, weight=None, label_smoothing=0.0):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.weight = weight
        self.label_smoothing = label_smoothing
    
    def forward(self, inputs, targets):
        # Apply label smoothing if specified
        if self.label_smoothing > 0:
            num_classes = inputs.size(-1)
            targets_one_hot = F.one_hot(targets, num_classes).float()
            targets_one_hot = targets_one_hot * (1 - self.label_smoothing) + self.label_smoothing / num_classes
            ce_loss = -torch.sum(targets_one_hot * F.log_softmax(inputs, dim=-1), dim=-1)
        else:
            ce_loss = F.cross_entropy(inputs, targets, weight=self.weight, reduction='none')
        
        # Calculate focal weight
        pt = torch.exp(-ce_loss)
        focal_weight = self.alpha * (1 - pt) ** self.gamma
        focal_loss = focal_weight * ce_loss
        
        return focal_loss.mean()


class MedicalBertClassifierAdvanced(nn.Module):
    """
    BERT-based classifier with hybrid training approach.
    Freezes early BERT layers, fine-tunes last 3 layers, and trains custom head.
    """
    def __init__(self, num_labels=40, dropout_rate=0.4, freeze_layers=9, class_weights=None, model_name='bert-base-uncased'):
        super(MedicalBertClassifierAdvanced, self).__init__()
        
        # Load pre-trained encoder (BERT/RoBERTa/ClinicalBERT, etc.)
        self.bert = AutoModel.from_pretrained(model_name)
        
        # Freeze early layers
        for i, layer in enumerate(self.bert.encoder.layer):
            if i < freeze_layers:
                for param in layer.parameters():
                    param.requires_grad = False
        
        # Keep embeddings frozen
        for param in self.bert.embeddings.parameters():
            param.requires_grad = False
        
        # Store class weights for loss calculation; register as buffer to move with model
        if class_weights is not None:
            if not isinstance(class_weights, torch.Tensor):
                class_weights = torch.tensor(class_weights, dtype=torch.float32)
            self.register_buffer('class_weights', class_weights)
        else:
            self.class_weights = None
        
        # Custom classifier with deep architecture
        self.classifier = nn.Sequential(
            nn.Linear(768, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            
            nn.Linear(256, num_labels)
        )
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None, label_smoothing=0.1):
        # Get encoder output (avoid token_type_ids to support RoBERTa)
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        # Robust pooling: use pooler_output if available; otherwise masked mean
        pooled_output = getattr(outputs, 'pooler_output', None)
        if pooled_output is None:
            last_hidden = outputs.last_hidden_state
            if attention_mask is None:
                pooled_output = last_hidden.mean(dim=1)
            else:
                mask = attention_mask.unsqueeze(-1).type_as(last_hidden)
                summed = (last_hidden * mask).sum(dim=1)
                # Avoid division by zero
                lengths = mask.sum(dim=1).clamp(min=1e-6)
                pooled_output = summed / lengths
        logits = self.classifier(pooled_output)
        
        # Calculate loss if labels provided
        loss = None
        if labels is not None:
            # Use focal loss for better handling of hard examples and class imbalance
            loss_fct = FocalLoss(
                alpha=1.0, 
                gamma=2.0, 
                weight=self.class_weights, 
                label_smoothing=label_smoothing
            )
            loss = loss_fct(logits, labels)
        
        return type('Output', (), {'loss': loss, 'logits': logits})()


class SimpleMedicalBert(nn.Module):
    """
    Simple BERT classifier - trains only the classification head.
    Fast training, good baseline.
    """
    def __init__(self, num_labels=40, dropout_rate=0.4, class_weights=None, model_name='bert-base-uncased'):
        super(SimpleMedicalBert, self).__init__()
        
        self.bert = AutoModel.from_pretrained(model_name)
        
        # Freeze all BERT parameters
        for param in self.bert.parameters():
            param.requires_grad = False
        
        # Store class weights for loss calculation; register as buffer to move with model
        if class_weights is not None:
            if not isinstance(class_weights, torch.Tensor):
                class_weights = torch.tensor(class_weights, dtype=torch.float32)
            self.register_buffer('class_weights', class_weights)
        else:
            self.class_weights = None
        
        # Simple classifier
        self.classifier = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_labels)
        )
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None, label_smoothing=0.1):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        pooled_output = getattr(outputs, 'pooler_output', None)
        if pooled_output is None:
            last_hidden = outputs.last_hidden_state
            if attention_mask is None:
                pooled_output = last_hidden.mean(dim=1)
            else:
                mask = attention_mask.unsqueeze(-1).type_as(last_hidden)
                summed = (last_hidden * mask).sum(dim=1)
                lengths = mask.sum(dim=1).clamp(min=1e-6)
                pooled_output = summed / lengths
        logits = self.classifier(pooled_output)
        
        # Calculate loss if labels provided
        loss = None
        if labels is not None:
            # Use focal loss for better handling of hard examples and class imbalance
            loss_fct = FocalLoss(
                alpha=1.0, 
                gamma=2.0, 
                weight=self.class_weights, 
                label_smoothing=label_smoothing
            )
            loss = loss_fct(logits, labels)
        
        return type('Output', (), {'loss': loss, 'logits': logits})()


def get_model(model_type, num_labels, dropout_rate=0.1, class_weights=None, model_name='bert-base-uncased', freeze_layers=9):
    """
    Factory function to create the appropriate model.
    
    Args:
        model_type: 'simple' or 'advanced'
        num_labels: Number of classification labels
        dropout_rate: Dropout probability
        class_weights: Optional weights for handling class imbalance
    
    Returns:
        Model instance
    """
    if model_type == 'simple':
        return SimpleMedicalBert(num_labels, dropout_rate, class_weights, model_name=model_name)
    elif model_type == 'advanced':
        return MedicalBertClassifierAdvanced(num_labels, dropout_rate, freeze_layers, class_weights, model_name=model_name)
    else:
        raise ValueError(f"Unknown model type: {model_type}")