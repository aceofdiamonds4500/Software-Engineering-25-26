import re   #Regular Expression module. Used for the sub function below.
                            
def insert_clean_column(df, column_name, clean_column_name):    #df: dataframe to be edited, 
                                                                #column_name: name of the column to be cleaned,
                                                                #clean_column_name: name of the new column that will contain the cleaned values

    df[clean_column_name] = list(map(lambda x:text_cleaner(x), df[column_name])) #Applies the text_cleaner method below to every value in a specified column, and assigns the values to a new column in the dataframe

def text_cleaner(text): #text: String that will be cleaned into alphanumeric characters.

    return re.sub(r'[^\w]', ' ', str(text)) #Takes anything in the string that isn't an alphanumeric character and replaces it with a space.
