import tensorflow as tf #team fortress
from transformers import BertForSequenceClassification, BertTokenizer, BertConfig
# from transformers import AutoTokenizer, AutoModel
import torch

from torch.utils.data import TensorDataset, random_split

from read_file import pd_read
import text_clean_and_insert as tci

def bert():
    if __name__ == "__main__":                              
        df = pd_read('mtsamples.csv')                       #Turns the mtsamples CSV file into a dataframe
                                                            #The CSV file/dataframe contains the following columns:
                                                            #The index
                                                            #description, which is a short description of the patient and/or operation
                                                            #medical_specialty, which is the medical field the visit pertains to
                                                            #sample_name, which contains the specific name of the diagnosis or operation
                                                            #transcription, which is a more detailed description of the visit
                                                            #keywords, which contains important keywords relating to the medical specialty of the visit

    device_name = tf.test.gpu_device_name()                 #Returns the name of the GPU if one is available. Returns an empty string if not
    print("Torch version:",torch.__version__)               #Yoinks the version of torch installed
    print("Is CUDA enabled?",torch.cuda.is_available())
    
    if torch.cuda.is_available():       
        device = torch.device("cuda")                       #Uses a CUDA-enabled GPU if one is available
    else:
        device = torch.device("cpu")                        #Uses CPU if not

    tci.insert_clean_column(df, 'transcription', 'clean_transcription') #Creates a "clean_transcription" column based on the "transcription" column
                                                                        #It contains all the data from 'transcription', but without punctuation or any other non-alphanumeric characters

    serialize_specialty(df)                                 #Call to the serialize_specialty method below
                                                            #It creates a new column in the dataframe, 'specialty_id'

    #'sentences' and 'labels' are numpy arrays that contain all the values from the 'clean_transcription' and 'specialty_id' columns respectively
    sentences = df.clean_transcription.values               
    labels = df.specialty_id.values


    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  #bert-base-uncased is the standard-sized BERT model. uncased means it doesn't differentiate between lowercase and uppercase letters
    # tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

    print(tokenizer.tokenize(sentences[0]))
    print(sentences[0])

    input_ids, attention_masks, labels= tokenize_dataset(sentences, labels, tokenizer)
    training_validation_split(input_ids, attention_masks, labels)

    
    model = BertForSequenceClassification.from_pretrained(  #
    "bert-base-uncased",                                    #
    problem_type="multi_label_classification",              #
    num_labels = 40,                                        #
    output_attentions = False,                              #
    output_hidden_states = False)                           #

    # model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

    model.cuda()






def tokenize_dataset(sentences, labels, tokenizer):
    input_ids = []
    attention_masks = []
    for i in sentences:
        encode_dict = tokenizer.encode_plus(i, 
                                            add_special_tokens=True,        #  
                                            max_length = 3481,              #
                                            padding = 'max_length',         #
                                            truncation = True,              #
                                            return_attention_mask= True,    #
                                            return_tensors = 'pt')          #
        #Check for if the dictionary actually has data in it
        if encode_dict is not None:
            input_ids.append(encode_dict['input_ids'])
        if encode_dict is not None:
            attention_masks.append(encode_dict['attention_mask'])
        

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks,dim=0)

    labels = torch.tensor(labels)
    print('Original: ', sentences[1])
    print('Token IDs:', input_ids[1])
    return input_ids, attention_masks, labels



def serialize_specialty(df):
    possible_labels = df.medical_specialty.unique()         #Compiles every unique value in the medical_specialty column into a numpy array
    label_dict = {}                  
    
    #Iterates over all the values in possible_labels and assigns the name of the specialty as the key to the dictionary. It assigns i as the value, 
    for i, possible_label in enumerate(possible_labels):
        label_dict[possible_label] = i
    label_dict

    df['specialty_id'] = df.medical_specialty.replace(label_dict)   #Replaces the medical_specialty column with numerical IDs for the specialties

def training_validation_split(input_ids, attention_masks, labels):  #

    dataset = TensorDataset(input_ids, attention_masks, labels)     #

    train_size = int(0.85* len(dataset))                            #
    validation_size = len(dataset) - train_size                     #

    train_dataset, validation_dataset = random_split(dataset, [train_size, validation_size])    #
    print('{:>5,} training samples'.format(train_size))                                         #
    print('{:>5,} validation samples'.format(validation_size))                                  #


bert()