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
	def __init__(self, name='Sean', commandhost=SEND_COMMAND_HOST, commandport=SEND_COMMAND_PORT, \
		customcommandhost=CUSTOM_SEND_COMMAND_HOST, customcommandport=CUSTOM_SEND_COMMAND_PORT):
			# Custom command ports are used for image capture (not part of CommUManager)
		self.name = name
		
		self.commandhost = commandhost
		self.commandport = commandport

		self.customcommandhost = customcommandhost
		self.customcommandport = customcommandport

		self.AXIS = {
			'PITCH_WAIST': 0,
			'LATERAL_BODY': 1,
			'RAISEFORWARD_LEFTARM': 2,
			'RAISELATERAL_LEFTARM': 3,
			'RAISEFORWARD_RIGHTARM': 4,
			'RAISELATERAL_RIGHTARM': 5,
			'PITCH_HEAD': 6,
			'TILT_HEAD': 7,
			'TURN_HEAD': 8,
			'EYES_UPDOWN': 9,
			'LEFT_EYE_LATERAL': 10,
			'RIGHT_EYE_LATERAL': 11,
			'EYELIDS': 12,
			'MOUTH': 13,
		}

	def openCommandSocket(self):
		self.commandsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.commandsocket.connect((self.commandhost,self.commandport))

	def openCustomCommandSocket(self):
		self.customcommandsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.customcommandsocket.connect((self.customcommandhost,self.customcommandport))

	def takepicture(self):
		command = '/takepicture'
		print(command)
		self.customcommandsocket.sendall(command)
		time.sleep(1)

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

	def look(self, x, y, z):
		try:
			x = str(int(x))
			y = str(int(y))
			z = str(int(z))

			command = '/look M '+x+' '+y+' '+z+' normal'
			print(command)
			self.commandsocket.sendall(command)
			time.sleep(0.5)

		except Exception as e:
			print(e)

	def move(self, axis_int, angle, speed):
		try:
			axis_int = str(int(axis_int))
			angle = str(int(angle))
			speed = str(int(speed))

			command = '/move '+axis_int+' '+angle+' '+speed
			print(command)
			self.commandsocket.sendall(command)
			time.sleep(0.5)

		except Exception as e:
			print(e)

	def closeCommandSocket(self):
		self.commandsocket.shutdown(socket.SHUT_RDWR)
		self.commandsocket.close() 

	def closeCustomCommandSocket(self):
		self.customcommandsocket.shutdown(socket.SHUT_RDWR)
		self.customcommandsocket.close() 