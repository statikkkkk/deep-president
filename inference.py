# for normal ultilities
from __future__ import print_function
# import twitter
# import pickle
import re
# for NN
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
# from keras.layers.core import TimeDistributedDense, Activation, Dropout  
from keras.optimizers import RMSprop
# import tensorflow as tf
# import tensorflow as tf
import os
from tqdm import tqdm
import glob
import string

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['MXNET_GPU_WORKER_NTHREADS'] = '8' 
os.environ['MXNET_ENABLE_GPU_P2P'] = '1'
os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '1'
# from numba import jit

# from keras import backend as K
# config = tf.ConfigProto()
# config.gpu_options.allow_growth=True
# sess = tf.Session(config=config)
# K.set_session(sess)

class DeepText(object):
    """docstring for DeepText"""
    def __init__(self, folderName, party):
        super(DeepText, self).__init__()
        self.fpath = folderName
        if party is 'Democrat':
            self.step = 9
        else:
            self.step = 3

    def LoadText(self):
        read_files = glob.glob(self.fpath + '/*.txt')
        text = []
        for f in read_files:
            with open(f, "rb") as infile:
                text.append(str(infile.read()))
        return self._cleanCorpus(text)

    def _cleanCorpus(self, corpus):
        cleanCorpus = []
        for line in corpus:
            text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', line)
            cleanCorpus.append(text)
        return ' '.join(cleanCorpus)
    
    # @jit
    def GenrateData(self, corpus):
        raw_text = corpus.lower()
        # create mapping of unique chars to integers, and a reverse mapping
        chars = sorted(list(set(raw_text)))
        char_to_int = dict((c, i) for i, c in enumerate(chars))
        self.int_to_char = dict((i, c) for i, c in enumerate(chars))
        # summarize the loaded data
        n_chars = len(raw_text)
        self.n_vocab = len(chars)
        print("Total Characters: ", n_chars)
        print("Total Vocab: ", self.n_vocab)
        # prepare the dataset of input to output pairs encoded as integers
        seq_length = 50
        self.dataX = []
        dataY = []
        for i in tqdm(range(0, n_chars - seq_length, self.step)):
            seq_in = raw_text[i:i + seq_length]
            seq_out = raw_text[i + seq_length]
            self.dataX.append([char_to_int[char] for char in seq_in])
            dataY.append(char_to_int[seq_out])
        n_patterns = len(self.dataX)
        print("Total Patterns: ", n_patterns)
        # reshape X to be [samples, time steps, features]
        self.X = np.reshape(self.dataX, (n_patterns, seq_length, 1))
        # normalize
        self.X = self.X / float(self.n_vocab)
        # one hot encode the output variable
        self.y = np_utils.to_categorical(dataY)
        return True

    def LSTM(self):
        model = Sequential()
        # LSTM LAYERS
        # output shape: (nb_samples, timesteps, 10)
        # model.add(TimeDistributedDense(1024, input_shape=(self.VOCAB_SIZE))) 
        model.add(LSTM(600, return_sequences=True, input_shape=(self.X.shape[1], self.X.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(600, return_sequences=True))
        model.add(Dropout(0.1))
        model.add(LSTM(600, return_sequences=True))
        model.add(Dropout(0.1))
        model.add(LSTM(600, return_sequences=False))
        model.add(Dropout(0.1))
        # output layer
        model.add(Dense(self.y.shape[1], activation='softmax'))
        model.summary()
        return model

    def generate(self, model, diversity=0.5, length=100):
        '''
        generate with letter-level model
        '''
        def sample(a, temperature=1.0):
            # helper function to sample an index from a probability array
            a = np.log(a) / temperature 
            dist = np.exp(a) / np.sum(np.exp(a)) 
            choices = range(len(a)) 
            return np.random.choice(choices, p=dist)

        # compile the model
        optimize = RMSprop(lr=0.001)
        # Prepare the list of GPUs to be used in training
        NUM_GPU = 1
        gpu_list = []
        for i in range(NUM_GPU): 
            gpu_list.append('gpu(%d)' % i)
        model.compile(loss='categorical_crossentropy', optimizer=optimize, context=gpu_list)

        # pick a random seed
        start = np.random.randint(0, len(self.dataX) - 1)
        pattern = self.dataX[start]
        # print "Seed:"
        speech = ''.join([self.int_to_char[value] for value in pattern])
        # print('Seed: ', speech)
        # generate characters
        for i in tqdm(range(1000)):
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / float(self.n_vocab)
            # print(x, x.shape)
            # preds = model.predict(x, verbose=0)[0]
            prediction = model.predict(x, verbose=0, batch_size=32)[0]
            index = sample(prediction, diversity)
            result = self.int_to_char[index]
            # seq_in = [self.int_to_char[value] for value in pattern]
            # sys.stdout.write(result)
            speech += result
            pattern.append(index)
            pattern = pattern[1:len(pattern)]

        # making the last sentence full
        print('[INFO] Filling last sentence.')
        while speech[-1] not in string.punctuation:
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / float(self.n_vocab)
            # print(x, x.shape)
            # preds = model.predict(x, verbose=0)[0]
            prediction = model.predict(x, verbose=0, batch_size=32)[0]
            index = sample(prediction, diversity)
            result = self.int_to_char[index]
            # seq_in = [self.int_to_char[value] for value in pattern]
            # sys.stdout.write(result)
            speech += result
            pattern.append(index)
            pattern = pattern[1:len(pattern)]

        # print('==========')
        # print(speech)
        # print('==========')
        return speech


def main(folderName, modelPath, party):
    ryan = DeepText(folderName, party)
    raw = ryan.LoadText()
    ryan.GenrateData(raw)
    model = ryan.LSTM()
    model.load_weights(modelPath)
    return ryan.generate(model)
