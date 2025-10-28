"""
File reading utilities for loading data.
"""
import pandas as pd


def pd_read(file):
    """
    Simple function to convert CSV file to a dataframe.
    
    Args:
        file: Path to CSV file
        
    Returns:
        DataFrame containing the CSV data
    """
    file_name = file
    df = pd.read_csv(file_name)
    return df


def load_medical_data(file_path='mtsamples.csv'):
    """
    Load medical samples dataset.
    
    Args:
        file_path: Path to the mtsamples CSV file
        
    Returns:
        DataFrame with medical transcription data
    """
    df = pd_read(file_path)
    print(f"Loaded {len(df)} medical samples")
    print(f"Columns: {list(df.columns)}")
    return df