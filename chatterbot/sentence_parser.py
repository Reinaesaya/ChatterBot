import nltk
import os
import random

from constants import *

def getFreqDist(sentences, tag):

	all_nouns = []
	for s in sentences:
		text = nltk.word_tokenize(s)
		for word in nltk.pos_tag(text):
			if word[1] == tag:
				all_nouns.append(word[0].lower())
		#print nltk.pos_tag(text)
	all_nouns = nltk.FreqDist(all_nouns)
	return all_nouns
	print all_nouns.most_common(3)

def getFreqDistCaptions(tags):

	while os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
		continue
	open(COMMU_IMG_CAPTIONS_LOCK, 'w').close()
	with open(COMMU_IMG_CAPTIONS, 'r') as f:
		lines = f.readlines()
	os.remove(COMMU_IMG_CAPTIONS_LOCK)

	captions = [x.split('.')[0].strip() for x in lines]

	freq_dists = {}
	for tag in tags:
		freq_dists[tag] = getFreqDist(captions, tag)

	return freq_dists


if __name__ == "__main__":
	print(getFreqDistCaptions(['NN']))


