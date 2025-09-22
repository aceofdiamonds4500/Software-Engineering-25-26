import tensorflow as tf #team fortress
from transformers import BertForSequenceClassification, BertTokenizer, BertConfig
# from transformers import AutoTokenizer, AutoModel
import torch

from torch.utils.data import TensorDataset, random_split

from read_file import pd_read
import text_clean_and_insert as tci

def bert():
    if __name__ == "__main__":
        df = pd_read('mtsamples.csv') 

    device_name = tf.test.gpu_device_name()
    print("Torch version:",torch.__version__)
    print("Is CUDA enabled?",torch.cuda.is_available())
    
    if torch.cuda.is_available():       
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    tci.insert_clean_column(df, 'transcription', 'clean_transcription')
    serialize_specialty(df)


    sentences = df.clean_transcription.values
    labels = df.specialty_id.values


    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

    print(tokenizer.tokenize(sentences[0]))
    print(sentences[0])

    input_ids, attention_masks, labels= tokenize_dataset(sentences, labels, tokenizer)
    training_validation_split(input_ids, attention_masks, labels)

    
    model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    problem_type="multi_label_classification",
    num_labels = 40,
    output_attentions = False,
    output_hidden_states = False)

    # model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

    model.cuda()






def tokenize_dataset(sentences, labels, tokenizer):
    input_ids = []
    attention_masks = []
    for i in sentences:
        encode_dict = tokenizer.encode_plus(i, 
                                            add_special_tokens=True, 
                                            max_length = 3481,
                                            padding = 'max_length',
                                            truncation = True,
                                            return_attention_mask= True, 
                                            return_tensors = 'pt')
        
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
    possible_labels = df.medical_specialty.unique()
    label_dict = {}
    for i, possible_label in enumerate(possible_labels):
        label_dict[possible_label] = i
    label_dict

    df['specialty_id'] = df.medical_specialty.replace(label_dict)

def training_validation_split(input_ids, attention_masks, labels):

    dataset = TensorDataset(input_ids, attention_masks, labels)

    train_size = int(0.85* len(dataset))
    validation_size = len(dataset) - train_size

    train_dataset, validation_dataset = random_split(dataset, [train_size, validation_size])
    print('{:>5,} training samples'.format(train_size))
    print('{:>5,} validation samples'.format(validation_size))


bert()