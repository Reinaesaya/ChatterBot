import socket
import time
import math
import string
import re

import curses
from curses.ascii import isdigit
import nltk
from nltk.corpus import cmudict

from .constants import *

d = cmudict.dict()
def countsyllables(word):
	try:
		return max([len(list(y for y in x if isdigit(str(y[-1])))) for x in d[word.lower()]])
	except:
		print("Syllables for word can't be count: "+word+". Defaulting to 3")
		return 5

class CommU():
	def __init__(self, name='Sean', commandhost=SEND_COMMAND_HOST, commandport=SEND_COMMAND_PORT):
		self.name = name
		self.commandhost = commandhost
		self.commandport = commandport

	def openCommandSocket(self):
		self.commandsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.commandsocket.connect((self.commandhost,self.commandport))

	def say(self, sentence):
		sentences = [re.sub(r'[\[\]\{\}\(\)\~\`\@\#\^\&\*\"\:\;\<\>\/\|\+\=\_\\"]','',s).strip() for s in sentence.split('.')]

		for s in sentences:
			if s == '':
				continue

			#words = [w.translate(None,string.punctuation) for w in s.split()]
			words = [re.sub(r'[\~\!\?\.\,\@\#\$\%\^\&\*\(\)\{\}\[\]\"\:\;\<\`\+\=\_\|\\"]','',w) for w in s.split()]
			syllables = 0
			for w in words:
				syllables += countsyllables(w)
			
			command = '/say_eng '
			command += '{ '+str(s)+' }'
			for g in GREETINGS:
				if g in s.lower():
					greetcommand = '/gesture hi'
					#print(greetcommand)
					#self.commandsocket.sendall(greetcommand)
			print(command)
			self.commandsocket.sendall(command)
			time.sleep(math.ceil(0.6*syllables))

	def closeCommandSocket(self):
		self.commandsocket.shutdown(socket.SHUT_RDWR)
		self.commandsocket.close()