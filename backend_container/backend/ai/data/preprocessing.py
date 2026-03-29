"""Text preprocessing and cleaning utilities for medical documents."""
import re


def text_cleaner(text):
    """Clean text into alphanumeric characters."""
    return re.sub(r'[^\w]', ' ', str(text))


def insert_clean_column(df, column_name, clean_column_name):
    """Create a new column with cleaned text."""
    df[clean_column_name] = list(map(lambda x: text_cleaner(x), df[column_name]))
    print(f"Created '{clean_column_name}' column from '{column_name}'")


def clean_medical_text(text):
    """Advanced cleaning for medical text."""
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    return text.strip()


def preprocess_dataframe(df, text_column='transcription', clean_column='clean_transcription'):
    """Complete preprocessing pipeline for medical text dataframe."""
    print(f"\nPreprocessing '{text_column}' column...")
    
    insert_clean_column(df, text_column, clean_column)
    
    df[clean_column] = df[clean_column].fillna('')
    
    initial_count = len(df)
    df = df[df[clean_column].str.len() > 50]
    removed_count = initial_count - len(df)
    
    if removed_count > 0:
        print(f"Removed {removed_count} samples with insufficient text")
    
    print(f"Preprocessing complete. {len(df)} samples ready for training.")
    
    return df
