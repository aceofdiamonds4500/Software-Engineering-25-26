import pandas as pd #The pandas module. Used to convert structured data files (in our case, CSV) into dataframes, which are easier for our program to read and manipulate

def pd_read(file):  #Simple function to convert our CSV file to a dataframe.
    file_name = file
    df = pd.read_csv(file_name)
    return df