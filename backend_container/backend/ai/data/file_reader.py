"""File I/O utilities for loading medical data."""
import pandas as pd


def pd_read(file):
    """Simple function to convert CSV file to a dataframe."""
    file_name = file
    df = pd.read_csv(file, header=None, names=['description', 'medical_specialty', 'sample_name', 'transcription', 'keywords'])
    return df


def load_medical_data(file_path='mtsamples.csv'):
    """Load medical samples dataset."""
    df = pd_read(file_path)
    print(f"Loaded {len(df)} medical samples")
    print(f"Columns: {list(df.columns)}")
    return df
