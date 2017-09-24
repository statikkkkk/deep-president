from textblob import TextBlob as tb 
# import matplotlib.pyplot as plt 
import re 
import string 
from autocorrect import spell
import nltk
from nltk.tokenize.moses import MosesDetokenizer

def cleaner(s):
    count = 0
    i = 0
    while i < len(s) - 1:
        if s[i] in ['.', '!', '?']:
            # capitalize first character of a setence 
            s1 = s[i + 1].upper()
            s = s[0: i + 1] + s1 + s[i + 2:]
            count += 1
            if count == 1:
                #delete all things before the first full stop
                s = s1 + s[i + 2:]
        i += 1
    return s

def spellCheck(s):
    tokens = nltk.word_tokenize(cleaner(s))
    corrected = [spell(s) if s not in string.punctuation else s for s in tokens]
    mose = MosesDetokenizer()
    return mose.detokenize(corrected, return_str=True)

def emotion2(text):
    # word polarity
    word_pols = {} 
    blob = tb('. '.join(re.findall(r"[\w']+", text)))
    word_pols = {str(word[:-1]): word.sentiment[0] for word in blob.sentences}
    # sentence polarity
    blob = tb(text)
    sentence_pols = [sentence.sentiment[0] for sentence in blob.sentences]
    return word_pols, sentence_pols



def emotion(text):

    linep = []
    linen = []
    #load positive file
    with open('positive.txt') as fp:
        linep = fp.read().split("\n")

    #load negative file
    with open('negative.txt') as fp:
        linen = fp.read().split("\n")

    word_pols = {} 
    blob = re.findall(r"[\w']+", text)

    print(blob)
    for word in blob:
        if word in linep:
            word_pols[str(word[:])] = 1
        elif word in linen:
            word_pols[str(word[:])] = -1
        else:
            word_pols[str(word[:])] = 0

    print(word_pols)
    return word_pols, {}


