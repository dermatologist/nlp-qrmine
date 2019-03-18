"""
This script was largely pulled from the Keras repo, and then
modifications were made for handling data in CSV files and for saving
the created network. Keras source:
https://github.com/fchollet/keras/blob/master/examples/imdb_cnn.py

"""

from __future__ import print_function

import csv
import pickle
import sys

import numpy as np
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence


def main():
    # set parameters:
    max_features = 5000
    maxlen = 400
    batch_size = 64
    embedding_dims = 50
    filters = 10
    kernel_size = 3
    hidden_dims = 50
    epochs = 10

    print('Loading data...')
    # (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
    (x_train, y_train), (x_test, y_test), vocab = load_data(sys.argv[1])
    print(len(x_train), 'train sequences')
    print(len(x_test), 'test sequences')

    print('Pad sequences (samples x time)')
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    print('x_train shape:', x_train.shape)
    print('x_test shape:', x_test.shape)

    print('Build model...')
    model = Sequential()

    # we start off with an efficient embedding layer which maps
    # our vocab indices into embedding_dims dimensions
    model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen))
    model.add(Dropout(0.2))

    # we add a Convolution1D, which will learn filters
    # word group filters of size filter_length:
    model.add(Conv1D(filters,
                     kernel_size,
                     padding='valid',
                     activation='relu',
                     strides=1))
    # we use max pooling:
    model.add(GlobalMaxPooling1D())

    # We add a vanilla hidden layer:
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))

    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test))

    classifier_fname = 'data/classifier.h5'
    vocab_fname = 'data/vocab.pkl'

    print("Saving classifier to:", classifier_fname)
    model.save(classifier_fname)
    print("Saving vocab to:", vocab_fname)
    pickle.dump(vocab, open(vocab_fname, 'wb'))


"""
The segment below are mostly from https://github.com/mindmech/blog/tree/master/02_keras_txt_classifier]

Thank you @mindmech

Changes were made to partition data into 75% train and 25% test.
Combined data_functions into this file
Added __main__ and some text sanitization code. 

"""


def process_msg(message, vocab):
    '''
    message:	the message string to classify.
    vocab: 		a dict of unique integers assigned to unique words.

    Insert your preprocessing here. For now we'll just lowercase,
    skip punctuation, and add unk tags.
    '''
    msg_arr = []
    tokenized = "".join((char if char.isalpha() else " ") for char in message.lower()).split()

    for word in tokenized:

        if word in vocab:
            msg_arr.append(vocab[word])
        else:
            msg_arr.append(vocab['<unk>'])

    return np.asarray(msg_arr)


def get_vocab(train_fname):
    '''
    Creates a vocabulary from a CSV file (must have "message" column), by
    assigning a unique integer to each unique word seen in the file.
    Replaces words only occurring once with an <unk> tag, to give the
    network the capability to process unknown words.
    '''
    print("Reading vocab from:", train_fname)
    reader = csv.reader(open(train_fname, 'r', encoding='utf-8'))
    freqs = {}

    header = next(reader)
    for row in reader:
        if row == []:
            continue
        message = row[header.index('message')]
        if " | " in message:
            message, value = message.split(" | ", 1)
        if " - " in message:
            message, value = message.split(" - ", 1)

        msg_arr = message.lower().split()

        for word in msg_arr:
            if word not in freqs.keys():
                freqs[word] = 0
        freqs[word] += 1

    vocab = {}
    vocab_idx = 1
    for word in freqs.keys():
        if freqs[word] > 1:
            vocab[word] = vocab_idx
            vocab_idx += 1

    vocab['<unk>'] = vocab_idx
    print("Vocab:", vocab)
    return vocab


def get_xy(csv_fname, vocab):
    '''
    csv_fname: 	filename for a CSV with columns "message" (string)
                and "annotation" (int).
    vocab: 		a dict of unique integers assigned to unique words

    Returns "x" and "y" data from csv file, i.e. converts each message
    into a list of corresponding word integers from the vocabulary for
    "x". The "y" data, of course, is simply the annotation for each
    message in the csv file.
    '''
    print("Getting x and y data from file", csv_fname)
    reader = csv.reader(open(csv_fname, 'r', encoding='utf-8'))
    header = next(reader)

    """
    Partition 75% as train and 25% as test
    """
    row_count = sum(1 for rows in reader)
    train_count = int(round(row_count * 0.75))
    row_count = 0

    reader = csv.reader(open(csv_fname, 'r', encoding='utf-8'))
    header = next(reader)

    xtrain = []
    ytrain = []
    xtest = []
    ytest = []

    for row in reader:
        row_count += 1
        if row == []:
            continue
        message = row[header.index('message')]

        # Text sanitization
        if " | " in message:
            message, value = message.split(" | ", 1)
        if " - " in message:
            message, value = message.split(" - ", 1)

        msg_x = process_msg(message, vocab)
        annotation = int(row[header.index('annotation')])
        if row_count < train_count:
            xtrain.append(msg_x)
            ytrain.append(annotation)
        else:
            xtest.append(msg_x)
            ytest.append(annotation)
    return np.asarray(xtrain), np.asarray(ytrain), np.asarray(xtest), np.asarray(ytest)


def load_data(train_fname):
    '''
    Load the messages and annotations from the input CSV files as
    lists of integers assigned to vocabulary words. Return also the
    vocabulary for later use by the live tool.
    '''
    vocab = get_vocab(train_fname)
    x_train, y_train, x_test, y_test = get_xy(train_fname, vocab)
    return (x_train, y_train), (x_test, y_test), vocab


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
