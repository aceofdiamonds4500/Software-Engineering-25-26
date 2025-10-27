import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Create id2label from your label_dict
label_dict = {
    ' Allergy / Immunology': 0,
    ' Bariatrics': 1, 
    ' Cardiovascular / Pulmonary': 2, 
    ' Neurology': 3, 
    ' Dentistry': 4, 
    ' Urology': 5, 
    ' General Medicine': 6, 
    ' Surgery': 7,
    ' Speech - Language': 8, 
    ' SOAP / Chart / Progress Notes': 9, 
    ' Sleep Medicine': 10, 
    ' Rheumatology': 11,
    ' Radiology': 12, 
    ' Psychiatry / Psychology': 13, 
    ' Podiatry': 14, 
    ' Physical Medicine - Rehab': 15, 
    ' Pediatrics - Neonatal': 16, 
    ' Pain Management': 17,
    ' Orthopedic': 18, 
    ' Ophthalmology': 19, 
    ' Office Notes': 20, 
    ' Obstetrics / Gynecology': 21,
    ' Neurosurgery': 22, 
    ' Nephrology': 23, 
    ' Letters': 24, 
    ' Lab Medicine - Pathology': 25,
    ' IME-QME-Work Comp etc.': 26,
    ' Hospice - Palliative Care': 27, 
    ' Hematology - Oncology': 28, 
    ' Gastroenterology': 29,
    ' ENT - Otolaryngology': 30,
    ' Endocrinology': 31,
    ' Emergency Room Reports': 32, 
    ' Discharge Summary': 33, 
    ' Diets and Nutritions': 34,
    ' Dermatology': 35, 
    ' Cosmetic / Plastic Surgery': 36,
    ' Consult - History and Phy.': 37, 
    ' Chiropractic': 38,
    ' Autopsy': 39
}

id2label = {v: k for k, v in label_dict.items()}

def load_trained_model(model_dir="./medical_classification_model"):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained(model_dir)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return tokenizer, model, device

def predict(text, tokenizer, model, device):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probs = torch.softmax(logits, dim=1)
    pred_id = torch.argmax(probs, dim=1).item()
    pred_label = id2label[pred_id]

    print("\n=== Prediction ===")
    print(f"Text: {text}")
    print(f"Predicted specialty: {pred_label} (ID: {pred_id})")
    print(f"Probabilities: {probs.cpu().numpy()}")
    return pred_label, probs

if __name__ == "__main__":
    tokenizer, model, device = load_trained_model()

    examples = [
        "The patient was diagnosed with pneumonia and prescribed antibiotics.",
        "Postoperative findings show no complications after cardiac surgery.",
        "CT scan of the abdomen reveals multiple liver lesions."
    ]

    for text in examples:
        predict(text, tokenizer, model, device)
