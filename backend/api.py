from flask import Flask
from random import choice
import textblob
import os.path
import glob
import pickle
import random
import json
import nlp_util
import unicodedata

app = Flask(__name__)



#--------MARKOV CODE-----------


END_PUNCTATION = ["!","?","."]
MAX_SENTENCES = 10

DEBUG = True

def remove_unicode(string):
    return "".join(string.split("\\u"))

def u2a(string):
    return remove_unicode(string)


def generateDict(text):
    words = text.split()
    if len(words) > 2:
        dictionary = {}
        for i,w in enumerate(words):
            firstWord = words[i];
            try:
                secondWord = words[i+1];
                thirdWord = words[i+2];
            except: 
                break

            key = (firstWord,secondWord)

            if key not in dictionary:
                dictionary[key]  = []

            dictionary[key].append(thirdWord)

        return dictionary
    else:
        return None

def getStartingKey(dictionary):
    #only upper cased first-in-tuple words are valid for a startingKey 
    possibleStartingKeys = [key for key in list(dictionary.keys()) if key[0][0].isupper()] 
    startingKey = choice(possibleStartingKeys)
    return startingKey

def generateText(dictionary):

    startingKey = getStartingKey(dictionary)

    sentence = []
    sentence.append(startingKey[0])
    sentence.append(startingKey[1])

    sentences = 0
    key = startingKey
    while True:
        try:
            possibleWords = dictionary[key]
            chosenWord = choice(possibleWords)

            key = (key[1],chosenWord)

            if DEBUG and len(possibleWords)>1:   #with DEBUG enabled you will see a colored word when the word was chosen from a more-than-1 choice list, aka the sentence could have gone 2 or more ways.
                sentence.append("" + chosenWord + "")
                print("" + chosenWord + " from " + str(possibleWords))
            else:
                sentence.append(chosenWord)

            if chosenWord[-1] in END_PUNCTATION:    #if the last char of the word is a end sentence thing
                sentence.append(" ")
                sentences = sentences + 1
                if sentences > MAX_SENTENCES:
                    break 

        except KeyError:    #the path is closed, better start another sentence!
            key = getStartingKey(dictionary)
            sentence.append("")
            sentence.append(key[0])
            sentence.append(key[1])

    return " ".join(sentence)


global dem_buffer
global rep_buffer


def string_from_file(filename):
    global current_sentence
    with open(filename, 'r') as inputFile:
        text = inputFile.read()
        dictionary = generateDict(text)
        if dictionary:
            text = generateText(dictionary)
            wordP, sentenceP = nlp_util.emotion(text)

            current_sentence = json.dumps({"words": text.replace(".", ". "), "word_polarity": wordP, "sentence_polarity": sentenceP})
            return current_sentence
        else:
            return json.dumps({"words": "Can't generate dictionary from the input text.\nERROR in generateDict.", "word_polarity": {}, "sentence_polarity": {}})


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

@app.route('/generate_democrat_sentence_markov', methods = ["GET"])
def generate_democrat_sentence_markov():
    return string_from_file("./democrat/merged-dem.txt")

@app.route('/generate_republican_sentence_markov', methods = ["GET"])
def generate_republican_sentence_markov():
    return string_from_file("./republican/merged-rep.txt")


@app.route('/generate_democrat_sentence', methods = ["GET"])
def generate_democrat_sentence():
    global dem_buffer
    global current_sentence
    if(len(dem_buffer)>0):
        d = random.choice(dem_buffer)
        dem_buffer = []
        repopulate()
        current_sentence = json.dumps({"words": d[0].replace(".", ". "), "word_polarity": d[1], "sentence_polarity": d[2]})
        return current_sentence
    else:
        return json.dumps({"words": "", "word_polarity": [], "sentence_polarity": []})

@app.route('/generate_republican_sentence', methods = ["GET"])
def generate_republican_sentence():
    global rep_buffer
    global current_sentence 
    if(len(rep_buffer)>0):
        r = random.choice(rep_buffer)
        rep_buffer = []
        repopulate()
        current_sentence = json.dumps({"words": r[0].replace(".", ". "), "word_polarity": r[1], "sentence_polarity": r[2]})
        return current_sentence
    else:
        return json.dumps({"words": "", "word_polarity": [], "sentence_polarity": []})



#HMMS

@app.route('/generate_clinton_sentence', methods = ["GET"])
def generate_clinton_sentence():
	return string_from_file("./democrat/merged-clinton.txt")

@app.route('/generate_obama_sentence', methods = ["GET"])
def generate_obama_sentence():
	return string_from_file("./democrat/merged-obama.txt")

@app.route('/generate_sanders_sentence', methods = ["GET"])
def generate_sanders_sentence():
	return string_from_file("./democrat/merged-sanders.txt")

@app.route('/generate_trump_sentence', methods = ["GET"])
def generate_trump_sentence():
	return string_from_file("./republican/merged-trump.txt")





def extract_rep(fn):
    rep_buffer.append(pickle.load( open( fn, "rb" ) ))
    print(len(rep_buffer))


def extract_dem(fn):
    dem_buffer.append(pickle.load( open( fn, "rb" ) ))
    print(len(dem_buffer))

    


def populate_rep(n):
    count_rep = 0
    for file in os.listdir(os.getcwd()+"/buffer/Republican"):
        print(file)
        if(count_rep < n):
            extract_rep(os.getcwd()+"/buffer/Republican/"+file)
            count = count_rep+1


def populate_dem(n):
    count_rep = 0
    print(os.listdir(os.getcwd()+"/buffer/Democrat"))
    for file in os.listdir(os.getcwd()+"/buffer/Democrat"):
        print(file)
        if(count_rep < n):
            extract_dem(os.getcwd()+"/buffer/Democrat/"+file)
            count = count_rep+1


def f(input):
    # do something here ...
    # call f() again in 60 seconds
    if(len(rep_buffer)<5):
        extract_rep(5-len(rep_buffer))
    if(len(dem_buffer)<5):
        extract_dem(5-len(dem_buffer))

    return input


def repopulate():
    if(len(rep_buffer)<5):
        populate_rep(5-len(rep_buffer))
    if(len(dem_buffer)<5):
        populate_dem(5-len(dem_buffer))


@app.route('/get_current_speech', methods = ["GET"])
def get_current_speech():
    global current_sentence
    return current_sentence


if __name__ == '__main__':
    global dem_buffer
    global rep_buffer
    global current_sentence

    dem_buffer = []
    rep_buffer = []
    current_sentence = json.dumps({"words": "", "word_polarity": [], "sentence_polarity": []})




    

    #rep

    # populate_rep(5)

    repopulate()

           






    app.run(host='0.0.0.0')



