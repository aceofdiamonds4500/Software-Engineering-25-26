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


class MultiHeadPooling(nn.Module):
    """Multi-strategy pooling layer for richer representations."""
    def __init__(self, hidden_size=768, use_cls=True, use_mean=True, use_max=True):
        super(MultiHeadPooling, self).__init__()
        self.use_cls = use_cls
        self.use_mean = use_mean
        self.use_max = use_max
    
    def forward(self, last_hidden_state, attention_mask=None):
        """
        Args:
            last_hidden_state: [batch_size, seq_length, hidden_size]
            attention_mask: [batch_size, seq_length]
        """
        pooled_outputs = []
        
        # CLS token pooling
        if self.use_cls:
            cls_output = last_hidden_state[:, 0, :]  # [batch_size, hidden_size]
            pooled_outputs.append(cls_output)
        
        # Mean pooling
        if self.use_mean:
            if attention_mask is not None:
                mask = attention_mask.unsqueeze(-1).type_as(last_hidden_state)
                summed = (last_hidden_state * mask).sum(dim=1)
                lengths = mask.sum(dim=1).clamp(min=1e-6)
                mean_output = summed / lengths
            else:
                mean_output = last_hidden_state.mean(dim=1)
            pooled_outputs.append(mean_output)
        
        # Max pooling
        if self.use_max:
            if attention_mask is not None:
                # Mask out padding tokens
                mask = attention_mask.unsqueeze(-1).type_as(last_hidden_state)
                masked = last_hidden_state * mask - (1 - mask) * 1e9
                max_output = masked.max(dim=1)[0]
            else:
                max_output = last_hidden_state.max(dim=1)[0]
            pooled_outputs.append(max_output)
        
        # Concatenate all pooling strategies
        if len(pooled_outputs) > 1:
            return torch.cat(pooled_outputs, dim=-1)
        else:
            return pooled_outputs[0]


class AttentionPooling(nn.Module):
    """Learned attention-based pooling."""
    def __init__(self, hidden_size=768):
        super(AttentionPooling, self).__init__()
        self.attention = nn.Linear(hidden_size, 1)
    
    def forward(self, last_hidden_state, attention_mask=None):
        """
        Args:
            last_hidden_state: [batch_size, seq_length, hidden_size]
            attention_mask: [batch_size, seq_length]
        """
        # Compute attention weights
        scores = self.attention(last_hidden_state)  # [batch_size, seq_length, 1]
        
        if attention_mask is not None:
            # Mask padding tokens
            mask = attention_mask.unsqueeze(-1)  # [batch_size, seq_length, 1]
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        weights = F.softmax(scores, dim=1)  # [batch_size, seq_length, 1]
        weighted = (last_hidden_state * weights).sum(dim=1)  # [batch_size, hidden_size]
        
        return weighted


class ResidualDenseBlock(nn.Module):
    """Dense layer with residual connection."""
    def __init__(self, in_features, out_features, dropout=0.4, use_layer_norm=True):
        super(ResidualDenseBlock, self).__init__()
        self.use_layer_norm = use_layer_norm
        self.use_residual = in_features == out_features
        
        if use_layer_norm:
            self.norm = nn.LayerNorm(in_features)
        self.linear = nn.Linear(in_features, out_features)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.GELU()
    
    def forward(self, x):
        residual = x if self.use_residual else None
        
        if self.use_layer_norm:
            x = self.norm(x)
        
        x = self.linear(x)
        x = self.activation(x)
        x = self.dropout(x)
        
        if self.use_residual:
            x = x + residual
        
        return x


class MedicalBertClassifierAdvanced(nn.Module):
    """BERT-based classifier with hybrid training and advanced pooling."""
    def __init__(self, num_labels=40, dropout_rate=0.4, freeze_layers=9, class_weights=None, 
                 model_name='bert-base-uncased', use_multi_pooling=True, use_attention_pooling=False):
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
        
        # Pooling setup
        hidden_size = 768
        if use_attention_pooling:
            self.pooling = AttentionPooling(hidden_size)
            pooled_size = hidden_size
        elif use_multi_pooling:
            self.pooling = MultiHeadPooling(hidden_size=hidden_size, use_cls=True, use_mean=True, use_max=True)
            pooled_size = hidden_size * 3  # CLS + Mean + Max
        else:
            self.pooling = None
            pooled_size = hidden_size
        
        # Enhanced classifier with residual connections
        self.classifier = nn.Sequential(
            ResidualDenseBlock(pooled_size, 512, dropout_rate, use_layer_norm=True),
            ResidualDenseBlock(512, 256, dropout_rate, use_layer_norm=True),
            nn.LayerNorm(256),
            nn.Linear(256, num_labels)
        )
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None, label_smoothing=0.1):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        last_hidden = outputs.last_hidden_state
        
        # Apply pooling
        if self.pooling is not None:
            pooled_output = self.pooling(last_hidden, attention_mask)
        else:
            # Fallback to BERT's pooler output or mean pooling
            pooled_output = getattr(outputs, 'pooler_output', None)
            if pooled_output is None:
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
    """Simple BERT classifier with enhanced pooling."""
    def __init__(self, num_labels=40, dropout_rate=0.4, class_weights=None, 
                 model_name='bert-base-uncased', use_multi_pooling=True):
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
        
        # Pooling setup
        hidden_size = 768
        if use_multi_pooling:
            self.pooling = MultiHeadPooling(hidden_size=hidden_size, use_cls=True, use_mean=True, use_max=True)
            pooled_size = hidden_size * 3
        else:
            self.pooling = None
            pooled_size = hidden_size
        
        self.classifier = nn.Sequential(
            nn.LayerNorm(pooled_size),
            nn.Linear(pooled_size, 256),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_labels)
        )
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None, label_smoothing=0.1):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        last_hidden = outputs.last_hidden_state
        
        # Apply pooling
        if self.pooling is not None:
            pooled_output = self.pooling(last_hidden, attention_mask)
        else:
            # Fallback
            pooled_output = getattr(outputs, 'pooler_output', None)
            if pooled_output is None:
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


def get_model(model_type, num_labels, dropout_rate=0.1, class_weights=None, 
              model_name='bert-base-uncased', freeze_layers=9, use_multi_pooling=True, use_attention_pooling=False):
    """Factory function to create the appropriate model."""
    if model_type == 'simple':
        return SimpleMedicalBert(num_labels, dropout_rate, class_weights, 
                               model_name=model_name, use_multi_pooling=use_multi_pooling)
    elif model_type == 'advanced':
        return MedicalBertClassifierAdvanced(num_labels, dropout_rate, freeze_layers, class_weights, 
                                            model_name=model_name, use_multi_pooling=use_multi_pooling,
                                            use_attention_pooling=use_attention_pooling)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
