import pandas as pd
import numpy as np
from cleantext import clean 
import re 
from transformers import XLNetTokenizer, XLNetForSequenceClassification, TrainingArguments, Trainer, pipeline
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import datasets
import evaluate
import random
import matplotlib.pyplot as plt

data = pd.read_csv("../datasets/mtsamples.csv")

#data['text_clean'] = data['transcription'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]+','',x) if pd.notna(x) else '')
data['text_clean'] = data.apply(
    lambda row: re.sub(r'[^a-zA-Z0-9\s]+', '', 
                       ' '.join([str(row['description']) if pd.notna(row['description']) else '',
                                 str(row['sample_name']) if pd.notna(row['sample_name']) else '',
                                 str(row['transcription']) if pd.notna(row['transcription']) else '',
                                 str(row['keywords']) if pd.notna(row['keywords']) else ''])),
    axis=1
)
data['medspec_int'] = LabelEncoder().fit_transform(data['medical_specialty']) 

NUM_LABELS = 40

train_split, test_split = train_test_split(data, train_size = 0.8)
train_split, val_split = train_test_split(train_split, train_size = 0.9)
#print(len(train_split))
#print(len(test_split))
#print(len(val_split))

train_df = pd.DataFrame({
    "labels": train_split.medspec_int.values,
    "text": train_split.text_clean.values
})

test_df = pd.DataFrame({
    "labels": test_split.medspec_int.values,
    "text": test_split.text_clean.values
})

train_df = datasets.Dataset.from_dict(train_df)
test_df = datasets.Dataset.from_dict(test_df)

dataset_dict = datasets.DatasetDict({"train": train_df, "test": test_df})

#print(dataset_dict)

tokenizer = XLNetTokenizer.from_pretrained("xlnet-base-cased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding = "max_length", max_length = 256, truncation=True)

tokenized_datasets = dataset_dict.map(tokenize_function, batched=True)

#print(tokenized_datasets['train']['attention_mask'][0])
small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))

medspec_labels= {
0: 'Surgery',
1: 'Consult - History and Phy.',
2: 'Cardiovascular / Pulmonary',
3: 'Orthopedic',
4: 'Radiology',
5: 'General Medicine',
6: 'Gastroenterology',
7: 'Neurology',
8: 'SOAP / Chart / Progress Notes',
9: 'Obstetrics / Gynecology',
10:'Urology',
11:'Discharge Summary',
12:'ENT - Otolaryngology',
13:'Neurosurgery',
14:'Hematology - Oncology',
15:'Ophtalmology',
16:'Nephrology',
17:'Emergency Room Reports',
18:'Pediatrics - Neonatal',
19:'Pain Management',
20:'Psychiatry / Psychology',
21:'Office Notes',
22:'Podiatry',
23:'Dermatology',
24:'Dentistry',
25:'Cosmetic / Plastic Surgery',
26:'Letters',
27:'Physical Medicine - Rehab',
28:'Sleep Medicine',
29:'Endocrinology',
30:'Bariatrics',
31:'IME-QME-Work Comp etc.',
32:'Chiropractic',
33:'Diets and Nutritions',
34:'Rheumatology',
35:'Speech - Language',
36:'Autopsy',
37:'Lab Medicine - Pathology',
38:'Allergy / Immunology',
39:'Hospice - Palliative Care'}

model = XLNetForSequenceClassification.from_pretrained('xlnet-base-cased',
                                                        num_labels=NUM_LABELS,
                                                        id2label=medspec_labels)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(output_dir="test_trainer", eval_strategy="epoch",num_train_epochs=8)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics
)

#trainer.train()

#print(trainer.evaluate())
#model.save_pretrained("fine_tuned_model")

fine_tuned_model = XLNetForSequenceClassification.from_pretrained("fine_tuned_model")

clf = pipeline("text-classification", fine_tuned_model, tokenizer=tokenizer)

rand_int = random.randint(0, len(val_split) - 1)  # Also fix: should be len-1

print(val_split['text_clean'].iloc[rand_int])  # Use .iloc
answer = clf(val_split['text_clean'].iloc[rand_int])
print(answer[0])  # Get highest confidence