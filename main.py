import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px

# runner
def main():
    file_name = 'mtsamples.csv'
    df = pd.read_csv(file_name)

    #chart
    class_counts = df['medical_specialty'].value_counts()
    fig = px.bar(class_counts,
        labels={'value':'Count of Cases', 'index':'Specialty'},
        title='Count of Cases per Specialty',
        orientation='v')
    fig.show()

    #word cleaning

    '''
    #indexing each medical_specialty
    possible_labels = df.medical_specialty.unique()
    label_dict = {}
    for index, possible_label in enumerate(possible_labels):
        label_dict[possible_label] = index
    label_dict

    df['label'] = df.medical_specialty.replace(label_dict)
    '''

    df['transcription'] = df['transcription'].astype(str)
    print(df.head())

    # displaying vector of top 20 phrases
    # adjust int n_words to increase the length of the phrase
    common_words = get_top_Nwords(df['transcription'].drop_duplicates(), 20, remove_stop_words=True, n_words=2)

    for word, freq in common_words:
        print(word, freq)

    #training
    X,y = df['transcription'].values,df['medical_specialty'].values
    x_train,x_test,y_train,y_test = train_test_split(X,y,stratify=y)
    print(f'train data shape: {x_train.shape}')
    print(f'test data shape: {x_test.shape}')
    #...

    # needs further work here
    # implement pytorch tensors to work with numpy arrays


# Vectorizing the top words
# Stop words are phrases like "there are", "it is", and other extremely common phrases that are unrelated
# The some parameters like n, remove_stop_words are set by default unless explicitly called
def get_top_Nwords(entry, n=None, remove_stop_words=False, n_words=1):
    if remove_stop_words:
        vec = CountVectorizer(stop_words='english', ngram_range=(n_words, n_words)).fit(entry)
    else:
        vec = CountVectorizer(ngram_range=(n_words, n_words)).fit(entry)

    bag_ofWords =vec.transform(entry)
    sum_words = bag_ofWords.sum(axis=0)
    words_freq = [(word, sum_words[0,idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


main()