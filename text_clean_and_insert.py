import re

def insert_clean_column(df, column_name, clean_column_name):
    df[clean_column_name] = list(map(lambda x:text_cleaner(x), df[column_name]))

def text_cleaner(text):
    return re.sub(r'[^\w]', ' ', str(text))
