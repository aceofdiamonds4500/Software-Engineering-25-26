import torch
from transformers import XLNetTokenizer, XLNetForSequenceClassification
import numpy as np

class XLNetPredictor:
    def __init__(self, model_path='./xlnet_finetuned'):
        """
        Load the trained XLNet model and tokenizer.
        
        Args:
            model_path: Path to the saved model directory
        """
        print("Loading model and tokenizer...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.tokenizer = XLNetTokenizer.from_pretrained(model_path)
        self.model = XLNetForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        print(f"Model loaded on {self.device}")
    
    def predict(self, text, max_length=128):
        """
        Predict the class for a single text.
        
        Args:
            text: Input text string
            max_length: Maximum sequence length
            
        Returns:
            Dictionary with prediction and probabilities
        """
        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Move to device
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
        
        # Process results
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'probabilities': probabilities[0].cpu().numpy()
        }
    
    def predict_batch(self, texts, max_length=128, batch_size=16):
        """
        Predict classes for multiple texts.
        
        Args:
            texts: List of text strings
            max_length: Maximum sequence length
            batch_size: Batch size for processing
            
        Returns:
            List of prediction dictionaries
        """
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            # Tokenize batch
            encodings = self.tokenizer(
                batch_texts,
                add_special_tokens=True,
                max_length=max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            # Move to device
            input_ids = encodings['input_ids'].to(self.device)
            attention_mask = encodings['attention_mask'].to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
            
            # Process results
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            predicted_classes = torch.argmax(probabilities, dim=1)
            
            for j in range(len(batch_texts)):
                results.append({
                    'text': batch_texts[j],
                    'predicted_class': predicted_classes[j].item(),
                    'confidence': probabilities[j][predicted_classes[j]].item(),
                    'probabilities': probabilities[j].cpu().numpy()
                })
        
        return results


# Example usage
def main():
    # Initialize predictor
    predictor = XLNetPredictor('./xlnet_finetuned')
    
    # Single prediction
    print("\n=== Single Prediction ===")
    text = "This product is amazing and exceeded my expectations!"
    result = predictor.predict(text)
    
    print(f"Text: {text}")
    print(f"Predicted Class: {result['predicted_class']}")
    print(f"Confidence: {result['confidence']:.4f}")
    print(f"All Probabilities: {result['probabilities']}")
    
    # Batch predictions
    print("\n=== Batch Predictions ===")
    texts = [
        "I love this product!",
        "Terrible experience, would not recommend.",
        "It's okay, nothing special.",
        "Best purchase I've made this year!",
        "Waste of money and time."
    ]
    
    results = predictor.predict_batch(texts)
    
    for result in results:
        print(f"\nText: {result['text']}")
        print(f"Predicted Class: {result['predicted_class']} (confidence: {result['confidence']:.4f})")
    
    # Get top predictions with class labels (optional)
    print("\n=== With Custom Labels ===")
    class_labels = {0: "Negative", 1: "Positive"}  # Adjust based on your task
    
    text = "This is absolutely fantastic!"
    result = predictor.predict(text)
    predicted_label = class_labels[result['predicted_class']]
    
    print(f"Text: {text}")
    print(f"Prediction: {predicted_label}")
    print(f"Confidence: {result['confidence']:.4f}")


if __name__ == "__main__":
    main()