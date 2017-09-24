from flask import Flask
from random import choice
import pipeline

app = Flask(__name__)



#--------MARKOV CODE-----------


END_PUNCTATION = ["!","?","."]
MAX_SENTENCES = 10

DEBUG = True

def generateDict(text):
    words = text.split()
    if len(words) > 2:
        dictionary = {}
        for i,w in enumerate(words):
            firstWord = words[i];
            try:    #try to get the other words, maybe i am at the end of the list
                secondWord = words[i+1];
                thirdWord = words[i+2];
            except: #we don't care if we don't have words following the current one and then we exit the loop
                break

            key = (firstWord,secondWord)

            if key not in dictionary:   #this pair of words is new to the dictionary, and so doesn't have a list of following words
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
                sentence.append("\033" + chosenWord + "\033")
                print("\'" + chosenWord + "\' from " + str(possibleWords))
            else:
                sentence.append(chosenWord)

            if chosenWord[-1] in END_PUNCTATION:    #if the last char of the word is a end sentence thing
                sentence.append("\n")
                sentences = sentences + 1
                if sentences > MAX_SENTENCES:
                    break 

        except KeyError:    #the path is closed, better start another sentence!
            key = getStartingKey(dictionary)
            sentence.append("\n")
            sentence.append(key[0])
            sentence.append(key[1])

    return " ".join(sentence)

def string_from_file(filename):
    with open(filename, 'r') as inputFile:
        text = inputFile.read()
        dictionary = generateDict(text)
        if dictionary:
            text = generateText(dictionary)
            return text
        else:
            return "Can't generate dictionary from the input text.\nERROR in generateDict."

queueDemocrat = []
@app.route('/generate_democrat_sentence', methods=["GET"])

def generate_democrat_sentence():
    return queueDemocrat.pop(0)

queueRepublican = []
@app.route('/generate_republican_sentence', methods=["GET"])
def generate_republican_sentence():
    return pipeline.generateSpeech('Republican')

@app.route('/generate_clinton_sentence', methods=["GET"])
def generate_clinton_sentence():
    return string_from_file("backend/democrat/merged-clinton.txt")

@app.route('/generate_obama_sentence', methods=["GET"])
def generate_obama_sentence():
    return string_from_file("backend/democrat/merged-obama.txt")

@app.route('/generate_sanders_sentence', methods=["GET"])
def generate_sanders_sentence():
    return string_from_file("backend/democrat/merged-sanders.txt")

@app.route('/generate_trump_sentence', methods=["GET"])
def generate_trump_sentence():
    return string_from_file("backend/republican/merged-trump.txt")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # # queue for democrat
    # queueDemocrat = [pipeline.generateSpeech('Democrat') for i in range(5)]
    # # queue for republican
    # queueRepublican = [pipeline.generateSpeech('Republican') for i in range(5)]
    # # queue for cliton
    # queueCliton = [string_from_file("./democrat/merged-clinton.txt") for i in range(5)]
    # # queue for obama
    # queueObama = [string_from_file("./democrat/merged-obama.txt") for i in range(5)]
    # # queue for sanders
    # queueSanders = [string_from_file("./democrat/merged-sanders.txt") for i in range(5)]
    # # queue for trump
    # queueTrump = [string_from_file("./republican/merged-trump.txt") for i in range(5)]

