import datetime
import random
import time
import numpy as np
from transformers import BertForSequenceClassification, BertTokenizer, BertConfig, TrainingArguments, T5ForConditionalGeneration
from torch.optim import AdamW
# from transformers import AutoTokenizer, AutoModel
import torch

from torch.utils.data import TensorDataset, random_split, DataLoader, RandomSampler, SequentialSampler

from transformers import Trainer, DataCollatorWithPadding, EarlyStoppingCallback
from evaluate import load

from read_file import pd_read
import text_clean_and_insert as tci
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

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

    print(sentences[0])

    input_ids, attention_masks, labels= tokenize_dataset(sentences, labels, tokenizer)
    train_dataset, validation_dataset = training_validation_split(input_ids, attention_masks, labels)

    batch_size = 16

    # Create the DataLoaders for our training and validation sets.
    # We'll take training samples in random order. 
    train_dataloader = DataLoader(
                train_dataset,  # The training samples.
                sampler = RandomSampler(train_dataset), # Select batches randomly
                batch_size = batch_size # Trains with this batch size.
            )

    # For validation the order doesn't matter, so we'll just read them sequentially.
    validation_dataloader = DataLoader(
                validation_dataset, # The validation samples.
                sampler = SequentialSampler(validation_dataset), # Pull out batches sequentially.
                batch_size = batch_size # Evaluate with this batch size.
        )
    model = BertForSequenceClassification.from_pretrained(  #
    "bert-base-uncased",                                    #
    problem_type="single_label_classification",              #
    num_labels = 40,                                        #
    output_attentions = False,                              #
    output_hidden_states = False).to(device)                           #
    model.cuda()
    params = list(model.named_parameters())

    print('The BERT model has {:} different named parameters.\n'.format(len(params)))

    print('==== Embedding Layer ====\n')

    for p in params[0:5]:
        print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))

    print('\n==== First Transformer ====\n')

    for p in params[5:21]:
        print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))

    print('\n==== Output Layer ====\n')

    for p in params[-4:]:
        print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))

    optimizer = AdamW(model.parameters(), lr = 2e-5, eps = 1e-8)   #
    epochs = 4                                                     #
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2)  #uses AdamW optimizer and a learning rate scheduler to adjust the learning rate during training
    
    # Set the seed value all over the place to make this reproducible.
    seed_val = 245

    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)

    # We'll store a number of quantities such as training and validation loss, 
    # validation accuracy, and timings.
    training_stats = []

    # Measure the total training time for the whole run.
    total_t0 = time.time()

    # For each epoch...
    for epoch_i in range(0, epochs):

        # ========================================
        #               Training
        # ========================================

        # Perform one full pass over the training set.

        print("")
        print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, epochs))
        print('Training...')

        # Measure how long the training epoch takes.
        t0 = time.time()

        # Reset the total loss for this epoch.
        total_train_loss = 0

        # Put the model into training mode. Don't be mislead--the call to 
        # `train` just changes the *mode*, it doesn't *perform* the training.
        # `dropout` and `batchnorm` layers behave differently during training
        # vs. test (source: https://stackoverflow.com/questions/51433378/what-does-model-train-do-in-pytorch)
        
        model.train()

        # For each batch of training data...
        for step, batch in enumerate(train_dataloader):

            # Progress update every 8 batches.
            if step % 8 == 0 and not step == 0:
                # Calculate elapsed time in minutes.
                elapsed = format_time(time.time() - t0)

                # Report progress.
                print('  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.'.format(step, len(train_dataloader), elapsed))

            # Unpack this training batch from our dataloader. 
            #
            # As we unpack the batch, we'll also copy each tensor to the GPU using the 
            # `to` method.
            #
            # `batch` contains three pytorch tensors:
            #   [0]: input ids 
            #   [1]: attention masks
            #   [2]: labels 
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)

            # Always clear any previously calculated gradients before performing a
            # backward pass. PyTorch doesn't do this automatically because 
            # accumulating the gradients is "convenient while training RNNs". 
            # (source: https://stackoverflow.com/questions/48001598/why-do-we-need-to-call-zero-grad-in-pytorch)
            model.zero_grad()        

            # Perform a forward pass (evaluate the model on this training batch).
            # The documentation for this `model` function is here: 
            # https://huggingface.co/transformers/v2.2.0/model_doc/bert.html#transformers.BertForSequenceClassification
            # It returns different numbers of parameters depending on what arguments
            # are given and what flags are set. For our usage here, it returns
            # the loss (because we provided labels) and the "logits"--the model
            # outputs prior to activation.
            outputs = model(b_input_ids, 
                                 token_type_ids=None, 
                                 attention_mask=b_input_mask, 
                                 labels=b_labels)
            loss = outputs.loss
            logits = outputs.logits
            # Accumulate the training loss over all of the batches so that we can
            # calculate the average loss at the end. `loss` is a Tensor containing a
            # single value; the `.item()` function just returns the Python value 
            # from the tensor.
            total_train_loss += loss.item()

            # Perform a backward pass to calculate the gradients.
            loss.backward()

            # Clip the norm of the gradients to 1.0.
            # This is to help prevent the "exploding gradients" problem.
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            # Update parameters and take a step using the computed gradient.
            # The optimizer dictates the "update rule"--how the parameters are
            # modified based on their gradients, the learning rate, etc.
            optimizer.step()

            

        # Calculate the average loss over all of the batches.
        avg_train_loss = total_train_loss / len(train_dataloader)            

        # Update the learning rate.
        scheduler.step()

        # Measure how long this epoch took.
        training_time = format_time(time.time() - t0)

        print("")
        print("  Average training loss: {0:.2f}".format(avg_train_loss))
        print("  Training epcoh took: {:}".format(training_time))

        # ========================================
        #               Validation
        # ========================================
        # After the completion of each training epoch, measure our performance on
        # our validation set.

        print("")
        print("Running Validation...")

        t0 = time.time()

        # Put the model in evaluation mode--the dropout layers behave differently
        # during evaluation.
        model.eval()

        # Tracking variables 
        total_eval_accuracy = 0
        total_eval_loss = 0
        nb_eval_steps = 0

        # Evaluate data for one epoch
        for batch in validation_dataloader:

            # Unpack this training batch from our dataloader. 
            #
            # As we unpack the batch, we'll also copy each tensor to the GPU using 
            # the `to` method.
            #
            # `batch` contains three pytorch tensors:
            #   [0]: input ids 
            #   [1]: attention masks
            #   [2]: labels 
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)

            # Tell pytorch not to bother with constructing the compute graph during
            # the forward pass, since this is only needed for backprop (training).
            with torch.no_grad():        

                # Forward pass, calculate logit predictions.
                # token_type_ids is the same as the "segment ids", which 
                # differentiates sentence 1 and 2 in 2-sentence tasks.
                # Get the "logits" output by the model. The "logits" are the output
                # values prior to applying an activation function like the softmax.
                outputs = model(b_input_ids, 
                                       token_type_ids=None, 
                                       attention_mask=b_input_mask,
                                       labels=b_labels)
            loss = outputs.loss
            logits = outputs.logits
            # Accumulate the validation loss.
            total_eval_loss += loss.item()

            # Move logits and labels to CPU
            logits = logits.detach().cpu().numpy()
            label_ids = b_labels.to('cpu').numpy()

            # Calculate the accuracy for this batch of test sentences, and
            # accumulate it over all batches.
            total_eval_accuracy += flat_accuracy(logits, label_ids)


        # Report the final accuracy for this validation run.
        avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
        print("  Accuracy: {0:.2f}".format(avg_val_accuracy))

        # Calculate the average loss over all of the batches.
        avg_val_loss = total_eval_loss / len(validation_dataloader)

        # Measure how long the validation run took.
        validation_time = format_time(time.time() - t0)

        print("  Validation Loss: {0:.2f}".format(avg_val_loss))
        print("  Validation took: {:}".format(validation_time))

        # Record all statistics from this epoch.
        training_stats.append(
            {
                'epoch': epoch_i + 1,
                'Training Loss': avg_train_loss,
                'Valid. Loss': avg_val_loss,
                'Valid. Accur.': avg_val_accuracy,
                'Training Time': training_time,
                'Validation Time': validation_time
            }
        )

    print("")
    print("Training complete!")

    print("Total training took {:} (h:mm:ss)".format(format_time(time.time()-total_t0)))

def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

def compute_metrics(pred):
    metric = load("f1")                                #
    logits, labels = pred                                   #
    predictions = logits.argmax(logits, axis=-1)                #
    return metric.compute(predictions=predictions, references=labels)  #


def tokenize_dataset(sentences, labels, tokenizer):
    input_ids = []
    attention_masks = []
    for i in sentences:
        encode_dict = tokenizer.encode_plus(
            i, 
            add_special_tokens=True,
            max_length=512,            # 512 is the BERT limit, 3481 is too big
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encode_dict['input_ids'])
        attention_masks.append(encode_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    # For single-label classification, labels should be 1D integers
    labels = torch.tensor(labels, dtype=torch.long)

    print('Original: ', sentences[1])
    print('Token IDs:', input_ids[1])
    return input_ids, attention_masks, labels


def save_model(model):
    model.save_pretrained("./medical_classificaion_model", from_pt=True) #Saves the model to the specified directory


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
    return train_dataset, validation_dataset                                                        #

def format_time(elapsed):
    '''
    Takes a time in seconds and returns a string hh:mm:ss
    '''
    # Round to the nearest second.
    elapsed_rounded = int(round((elapsed)))
    
    # Format as hh:mm:ss
    return str(datetime.timedelta(seconds=elapsed_rounded))

bert()