'''
Source: http://mindmech.net

(https://github.com/mindmech/blog/blob/master/02_keras_txt_classifier/run_classifier.py)
Changes were made in file names
'''

import pickle

from keras.models import load_model
from keras.preprocessing import sequence

from src.misc_qrmine.sentiment import process_msg

model = load_model('data/classifier.h5')
vocab = pickle.load(open('data/vocab.pkl', 'rb'))

command = ''

print("Enter a message and see its sentiment:")
while True:
    command = input('-> ')
    if command == 'exit':
        break

    x = process_msg(command, vocab)
    x = sequence.pad_sequences([x], maxlen=400)
    print("Sentiment:", model.predict(x)[0][0])
