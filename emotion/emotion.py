from textblob import TextBlob as tb 
import matplotlib.pyplot as plt 
import re 
import string 
import cleanup
from autocorrect import spell 

def emotion(text): 	
	
	word_pols = {} 
	blob = tb('. '.join(re.findall(r"[\w']+", text)))
	for word in blob.sentences:
		word_pols[word[:-1]] = word.sentiment[0] 
	
	split = re.findall(r"[\w']+|[.,!?;\']", text)
	
	clean = ''
	for word in split: 
		if word not in string.punctuation:
			clean += ' ' + spell(word)
		else: clean += word
	clean = cleanup.cleanup(clean.strip())
	blob = tb(clean)
	sentence_pols = [sentence.sentiment[0] for sentence in blob.sentences]

	return sentence_pols, word_pols

