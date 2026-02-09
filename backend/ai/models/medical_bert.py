"""Medical BERT Classification Models"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel


class FocalLoss(nn.Module):
    """Focal Loss for handling class imbalance."""
    def __init__(self, alpha=1.0, gamma=2.0, weight=None, label_smoothing=0.0):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.weight = weight
        self.label_smoothing = label_smoothing
    
    def forward(self, inputs, targets):
        if self.label_smoothing > 0:
            num_classes = inputs.size(-1)
            targets_one_hot = F.one_hot(targets, num_classes).float()
            targets_one_hot = targets_one_hot * (1 - self.label_smoothing) + self.label_smoothing / num_classes
            ce_loss = -torch.sum(targets_one_hot * F.log_softmax(inputs, dim=-1), dim=-1)
        else:
            ce_loss = F.cross_entropy(inputs, targets, weight=self.weight, reduction='none')
        
        pt = torch.exp(-ce_loss)
        focal_weight = self.alpha * (1 - pt) ** self.gamma
        focal_loss = focal_weight * ce_loss
        
        return focal_loss.mean()


class MedicalBertClassifierAdvanced(nn.Module):
    """BERT-based classifier with hybrid training approach."""
    def __init__(self, num_labels=40, dropout_rate=0.4, freeze_layers=9, class_weights=None, model_name='bert-base-uncased'):
        super(MedicalBertClassifierAdvanced, self).__init__()
        
        self.bert = AutoModel.from_pretrained(model_name)
        
        for i, layer in enumerate(self.bert.encoder.layer):
            if i < freeze_layers:
                for param in layer.parameters():
                    param.requires_grad = False
        
        for param in self.bert.embeddings.parameters():
            param.requires_grad = False
        
        if class_weights is not None:
            if not isinstance(class_weights, torch.Tensor):
                class_weights = torch.tensor(class_weights, dtype=torch.float32)
            self.register_buffer('class_weights', class_weights)
        else:
            self.class_weights = None
        
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
        
        loss = None
        if labels is not None:
            loss_fct = FocalLoss(
                alpha=1.0, 
                gamma=2.0, 
                weight=self.class_weights, 
                label_smoothing=label_smoothing
            )
            loss = loss_fct(logits, labels)
        
        return type('Output', (), {'loss': loss, 'logits': logits})()


class SimpleMedicalBert(nn.Module):
    """Simple BERT classifier - trains only the classification head."""
    def __init__(self, num_labels=40, dropout_rate=0.4, class_weights=None, model_name='bert-base-uncased'):
        super(SimpleMedicalBert, self).__init__()
        
        self.bert = AutoModel.from_pretrained(model_name)
        
        for param in self.bert.parameters():
            param.requires_grad = False
        
        if class_weights is not None:
            if not isinstance(class_weights, torch.Tensor):
                class_weights = torch.tensor(class_weights, dtype=torch.float32)
            self.register_buffer('class_weights', class_weights)
        else:
            self.class_weights = None
        
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
        
        loss = None
        if labels is not None:
            loss_fct = FocalLoss(
                alpha=1.0, 
                gamma=2.0, 
                weight=self.class_weights, 
                label_smoothing=label_smoothing
            )
            loss = loss_fct(logits, labels)
        
        return type('Output', (), {'loss': loss, 'logits': logits})()


def get_model(model_type, num_labels, dropout_rate=0.1, class_weights=None, model_name='bert-base-uncased', freeze_layers=9):
    """Factory function to create the appropriate model."""
    if model_type == 'simple':
        return SimpleMedicalBert(num_labels, dropout_rate, class_weights, model_name=model_name)
    elif model_type == 'advanced':
        return MedicalBertClassifierAdvanced(num_labels, dropout_rate, freeze_layers, class_weights, model_name=model_name)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
