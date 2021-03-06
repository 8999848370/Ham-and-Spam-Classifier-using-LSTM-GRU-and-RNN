# -*- coding: utf-8 -*-
"""spam_ham_keras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HUmRj1cfy5OT9ThiC4V7wnrUod6pC1EB

# SPAM CLASSIFICATION with LSTM Network in Keras
"""

# Import the necessary libraries, modules
import pandas as pd # Pandas library for reading '.csv' files as dataframes
import numpy as np  # Numpy library for creating and modifying arrays.
from keras.layers import Dense, SimpleRNN, GRU, LSTM, RNN, SimpleRNN, Embedding # Import layers from Keras
from keras.models import Sequential

"""### Reading the data"""

raw_data = pd.read_csv('train.csv',encoding='latin-1') # Read the data as a DataFrame using Pandas
raw_test_data = pd.read_csv('test.csv', encoding='latin-1')

print(raw_data.shape) # Print the dimensions of train DataFrame
print(raw_data.columns) # Print the column names of the DataFrame
print('\n')
raw_data.head(5) # Print the top few records

"""### Check the labels and their frequencies"""

raw_data.dropna(inplace=True)

raw_test_data.dropna(inplace=True)

# Print the unique classes and their counts/frequencies
classes = np.unique(raw_data['Label'], return_counts=True) # np.unique returns a tuple with class names and counts
print(classes[0]) #Print the list of unique classes
print(classes[1]) #Print the list of frequencies of the above classes

pd.value_counts(raw_data['Label'])

"""### Converting unstructured text to structured numeric form
This includes:
1. Tokenizing
2. Converting sequence of words to sequence of word indeces
3. Converting varing length sequences to fixed length sequences through padding
"""

max_num_words = 10000
seq_len = 50
embedding_size = 100

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=max_num_words) #Tokenizer is used to tokenize text
tokenizer.fit_on_texts(raw_data.Message)  #Fit this to our corpus

x_train = tokenizer.texts_to_sequences(raw_data.Message) #'text to sequences converts the text to a list of indices
x_train = pad_sequences(x_train, maxlen=50) #pad_sequences makes every sequence a fixed size list by padding with 0s 
x_test = tokenizer.texts_to_sequences(raw_test_data.Message) 
x_test = pad_sequences(x_test, maxlen=50)

x_train.shape, x_test.shape # Check the dimensions of x_train and x_test

type(x_train)

"""### Prepare the target vectors for the network"""

unique_labels = list(raw_data.Label.unique())
print(unique_labels)

raw_data.replace(['ham', 'info', 'spam'], [0,1,2] ,inplace = True)
raw_test_data.replace(['ham', 'info', 'spam'], [0,1,2] ,inplace = True)

y_train = raw_data.iloc[:,0].values
y_test = raw_test_data.iloc[:,0].values

"""### Building and training an LSTM model"""

# Building an LSTM model
model = Sequential() # Call Sequential to initialize a network
model.add(Embedding(input_dim = max_num_words, 
                    input_length = seq_len, 
                    output_dim = embedding_size)) # Add an embedding layer which represents each unique token as a vector
model.add(LSTM(10, return_sequences=True)) # Add an LSTM layer
model.add(LSTM(5, return_sequences=False))
model.add(Dense(3, activation='softmax')) # Add an ouput layer. Since classification, 3 nodes for 3 classes.

model.summary()

from keras.optimizers import Adam
adam = Adam(lr=0.001)

# Mention the optimizer, Loss function and metrics to be computed
model.compile(optimizer=adam,                  # 'Adam' is a variant of gradient descent technique
              loss='sparse_categorical_crossentropy', # categorical_crossentropy for multi-class classification
              metrics=['accuracy'])            # These metrics are computed for evaluating and stored in history

model.fit(x_train, y_train, epochs=1, validation_split=0.25)

from sklearn.metrics import confusion_matrix, accuracy_score
print("Accurcy" , accuracy_score(y_train , model.predict_classes(x_train)))
cm1 = confusion_matrix(y_train , model.predict_classes(x_train))
cm1

"""## **`**RNN**`**"""

# Building an LSTM model
model1 = Sequential() # Call Sequential to initialize a network
model1.add(Embedding(input_dim = max_num_words, 
                    input_length = seq_len, 
                    output_dim = embedding_size)) # Add an embedding layer which represents each unique token as a vector
model1.add(SimpleRNN(10, return_sequences=True)) # Add an SimpleRNN
model1.add(SimpleRNN(5, return_sequences=False))
model1.add(Dense(3, activation='softmax')) # Add an ouput layer. Since classification, 3 nodes for 3 classes.
model1.summary()

# Mention the optimizer, Loss function and metrics to be computed
model1.compile(optimizer=adam,                  # 'Adam' is a variant of gradient descent technique
              loss='sparse_categorical_crossentropy', # categorical_crossentropy for multi-class classification
              metrics=['accuracy'])            # These metrics are computed for evaluating and stored in history
model1.fit(x_train, y_train, epochs=1, validation_split=0.25)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_train , model1.predict_classes(x_train))
cm

from sklearn.metrics import accuracy_score
print("Accurcy" , accuracy_score(y_train , model1.predict_classes(x_train)))

"""# **GRU**"""

model2 = Sequential() # Call Sequential to initialize a network
model2.add(Embedding(input_dim = max_num_words, 
                    input_length = seq_len, 
                    output_dim = embedding_size)) # Add an embedding layer which represents each unique token as a vector
model2.add(GRU(10, return_sequences=True)) # Add an GRU
model2.add(GRU(5, return_sequences=False))
model2.add(Dense(3, activation='softmax')) # Add an ouput layer. Since classification, 3 nodes for 3 classes.
model2.summary()

# Mention the optimizer, Loss function and metrics to be computed
model2.compile(optimizer=adam,                  # 'Adam' is a variant of gradient descent technique
              loss='sparse_categorical_crossentropy', # categorical_crossentropy for multi-class classification
              metrics=['accuracy'])            # These metrics are computed for evaluating and stored in history
model2.fit(x_train, y_train, epochs=1, validation_split=0.25)

from sklearn.metrics import confusion_matrix, accuracy_score
print("Accurcy" , accuracy_score(y_train , model2.predict_classes(x_train)))
cm2 = confusion_matrix(y_train , model2.predict_classes(x_train))
cm2