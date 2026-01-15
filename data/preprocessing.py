"""
Text preprocessing and cleaning utilities.
"""
import re


def text_cleaner(text):
    """
    Clean text into alphanumeric characters.
    
    Args:
        text: String that will be cleaned
        
    Returns:
        Cleaned text with only alphanumeric characters and spaces
    """
    return re.sub(r'[^\w]', ' ', str(text))


def insert_clean_column(df, column_name, clean_column_name):
    """
    Create a new column with cleaned text.
    
    Args:
        df: DataFrame to be edited
        column_name: Name of the column to be cleaned
        clean_column_name: Name of the new column that will contain cleaned values
        
    Returns:
        None (modifies DataFrame in place)
    """
    df[clean_column_name] = list(map(lambda x: text_cleaner(x), df[column_name]))
    print(f"Created '{clean_column_name}' column from '{column_name}'")


def clean_medical_text(text):
    """
    Advanced cleaning for medical text.
    Keeps important medical terminology intact.
    
    Args:
        text: Medical text to clean
        
    Returns:
        Cleaned text
    """
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep important medical symbols
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    
    return text.strip()


def preprocess_dataframe(df, text_column='transcription', clean_column='clean_transcription'):
    """
    Complete preprocessing pipeline for medical text dataframe.
    
    Args:
        df: DataFrame with medical text
        text_column: Column containing raw text
        clean_column: Name for the cleaned text column
        
    Returns:
        DataFrame with cleaned text column added
    """
    print(f"\nPreprocessing '{text_column}' column...")
    
    # Basic cleaning
    insert_clean_column(df, text_column, clean_column)
    
    # Remove any NaN values
    df[clean_column] = df[clean_column].fillna('')
    
    # Remove very short transcriptions (likely invalid)
    initial_count = len(df)
    df = df[df[clean_column].str.len() > 50]
    removed_count = initial_count - len(df)
    
    if removed_count > 0:
        print(f"Removed {removed_count} samples with insufficient text")
    
    print(f"Preprocessing complete. {len(df)} samples ready for training.")
    
    return df