import pandas as pd

def pd_read(file):
    file_name = file
    df = pd.read_csv(file_name)
    return df