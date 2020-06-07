import nltk
import nltk.data
from nltk.tokenize import sent_tokenize
from .findMatch import horspool_match
from .negex import *
import pkg_resources



resource_package = 'VTEReportsAnalysis'
resource_path = '/'.join(('config','negex_triggers.txt'))
path = pkg_resources.resource_filename(resource_package, resource_path)

rfile = open(path)
irules = sortRules(rfile.readlines())



'''
def splitSentence(paragraph):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(paragraph)
	return sentences 
'''

def splitSentence(paragraph):
    sentences = []
    for sentence in paragraph.split('.'):
        if '?' in sentence:
            sentences.extend(sentence.split('?'))
        elif '!' in sentence:
            sentences.extend(sentence.split('!'))
        else:
            sentences.append(sentence)
    return sentences


class reExtractor:
	def __init__(self, target, skip, absolute_negative, absolute_positive, start):
		self.target = target
		self.skip = skip
		self.absolute_positive = absolute_positive
		self.absolute_negative = absolute_negative
		self.start = start
	
	def test(self):
		print(self.target)
	
	def processing(self,text):
		for phrase in self.start:
			temp = horspool_match(phrase,text)
			if temp != -1:
				text = text[temp:]
		text = text.lower()

		for phrase in self.absolute_negative:
			temp = horspool_match(phrase,text)
			if temp != -1:
				print(phrase,text)
				return -99,-99

		sentences = splitSentence(text)
		
		presentCount = 0
		absentCount = 0

		for sentence in sentences:


			present = 0

			mark = 0
			for phrase in self.skip:
				temp = horspool_match(phrase,sentence)
				if temp != -1:  # -1 is 404 not found
					mark = 1
			if mark == 1:		# 'skip' found, so skip this sentence
				continue

			mark = 0
			for phrase in self.target:
				temp = horspool_match(phrase,sentence)
				if temp != -1:
					mark = 1
			if mark == 1:		# 'target' found, so check negation
				tagger = negTagger(sentence, phrases = '', rules = irules, negP=False)
				negexResult = tagger.getNegationFlag()
				if negexResult == 'affirmed':
					present = 1
				elif negexResult == 'negated':
					present = 0
			if present == 1:
				presentCount += 1
			else:
				absentCount += 1
		return presentCount, absentCount