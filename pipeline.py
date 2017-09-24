# data processing pipeline for poli-speech
import inference
import nlp_util
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import pickle
import os
import time.time

def generateSpeech(party):
    if party is 'Republican':
        folder = 'data/republican'
        modelP = 'models/republican.hdf5'
    elif party is 'Democrat':
        folder = 'data/democrate'
        modelP = 'models/democrate.hdf5'
    else:
        raise(ValueError('Party must be Republican or Democrat.'))
    # get raw text
    rawText = inference.main(folder, modelP, party)
    # spell check
    cleaned = nlp_util.spellCheck(rawText)
    # get polarity
    wordPolarity, sentencePolarity = nlp_util.emotion(cleaned)

    print('=========')
    print(cleaned)
    print('=========')
    print(wordPolarity)
    print('=========')
    # print(sentencePolarity)
    return (cleaned, wordPolarity, sentencePolarity)

flag = True
while True:
    if flag:
        party = 'Republican'
    else:
        party = 'Democrat'
    pickle.dump(generateSpeech(party), open(os.join('buffer','Republican', str(time.time())+'.p'), "wb" ) ) 


