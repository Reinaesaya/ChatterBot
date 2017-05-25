import re
from mechanize import Browser
from bs4 import BeautifulSoup
import urllib
import urllib2
import random
import string


### Compare outputs for all chatbots ###

class ChatBotComparator():
	def __init__(self, user='User'):
		self.mitsuku = Mitsuku()
		self.rose = Rose(user)
		self.chatbots = {
			'Mitsuku': self.mitsuku,
			'Rose': self.rose
		}

	def refresh(self):
		self.mitsuku.refresh()
		self.rose.refresh()

	def getResponse(self, message):
		messages = {
			'Mitsuku': self.mitsuku.getResponse(message),
			'Rose': self.rose.getResponse(message),
		}
		return messages

	def runSimulation(self):
		print('\n*------*')
		print('Welcome to the chatbot comparison simulator on Python')
		print('Chatbots being tested: '+', '.join(self.chatbots.keys()))
		print('To stop chat, Ctrl-C')
		print('*------*')

		try:
			while True:
				message = raw_input('\nEnter message: ')
				responses = self.getResponse(message)
				for bot in responses.keys():
					print(bot+': '+responses[bot])
		except KeyboardInterrupt:
			print('\n*------*')
			print('Simulation ended.')
			print('*------*')


### Mitsuku ChatBot ###

class Mitsuku:
	def __init__(self):
		self.refresh()

	def refresh(self):
		self.br = Browser()
		self.br.set_handle_robots( False )
		response = self.br.open('https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&skin=chat')
		self.br_soup = BeautifulSoup(response.read(), "lxml")
		

		self.last_convohtml = str(self.br_soup.find('font', {'color':'#000000'}))
		self.all_messages = []
		self.last_message = None
		self.all_responses = []
		self.last_response = None

	def getResponse(self, message):
		self.last_message = message
		self.all_messages.append(self.last_message)
		self.br.select_form(name='f')
		self.br.form['message'] = message
		
		response = self.br.submit()
		self.br_soup = BeautifulSoup(response.read(), "lxml")
		p = str(self.br_soup.find('font', {'color':'#000000'}))
		if self.last_convohtml == p:    # No response generated
			#print('Invalid input. Mitsuku had no answer')
			return None
		self.last_convohtml = p
		self.last_response = p.split('<br/> <br/>')[0].split('</b>')[-1].strip()
		#print(self.last_response.strip())
		self.last_response = self.removeTextWithinAngleBrackets(self.last_response)
		self.all_responses.append(self.last_response)

		return self.last_response

	def removeTextWithinAngleBrackets(self, text):
		new = ""
		left = 0
		for t in text:
			if t == '<':
				left += 1
				continue
			elif t == '>':
				left -= 1
				new = new+' '
				continue

			if left < 0:
				print("Something went wrong in removing angle brackets")
				print(text)
				return text
			if left == 0:
				new = new+t
		return new.strip()

	def runSimulation(self):
		print('\n*------*')
		print('Welcome to the Mitsuku chatbot simulator on Python')
		print('Implemented through use of mechanize library on https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&skin=chat')
		print('Original Mitsuku chatbot at www.mitsuku.com')
		print('To stop chat, Ctrl-C')
		print('*------*')

		try:
			while True:
				message = raw_input('\nEnter message: ')
				response = self.getResponse(message)
				if response == None:
					print('Invalid input. Mitsuku had no answer')
					continue
				print('Mitsuku: '+response)
		except KeyboardInterrupt:
			print('\n*------*')
			print('Simulation ended.')
			print('*------*')


### Rose ChatBot ###

class Rose:
	def __init__(self, user=None):
		self.url = 'http://ec2-54-215-197-164.us-west-1.compute.amazonaws.com/ui.php'
		self.refresh(user)

	def generateRandomID(self, length=10):
		rose_id = ''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(length))
		print('Chatbot Rose User ID: '+rose_id)

	def refresh(self, user=None):
		if user is not None:
			self.User = user
		else:
			self.User = self.generateRandomID()				# Rose history might be stored by User, so refresh it
		self.all_messages = []
		self.last_message = None
		self.all_responses = []
		self.last_response = None

	def getResponse(self, message):
		self.last_message = message
		self.all_messages.append(self.last_message)

		values = {
			'user': self.User,
			'send': "",
			'message': message
		}
		data = urllib.urlencode(values)
		req = urllib2.Request(self.url, data)
		response = urllib2.urlopen(req)

		self.last_response = response.read().split(']')[-1]    # Get rid of the "[callback=3000 ]"
		self.last_response = self.last_response.strip()
		self.all_responses.append(self.last_response)

		return self.last_response

	def runSimulation(self):
		print('\n*------*')
		print('Welcome to the Rose chatbot simulator on Python')
		print('Implemented through use of HTTP POST requests on http://ec2-54-215-197-164.us-west-1.compute.amazonaws.com/ui.php')
		print('Interactive webapp is at http://ec2-54-215-197-164.us-west-1.compute.amazonaws.com/speech.php')
		print('To stop chat, Ctrl-C')
		print('*------*')

		try:
			while True:
				message = raw_input('\nEnter message: ')
				response = self.getResponse(message)
				print('Rose: '+str(response))
		except KeyboardInterrupt:
			print('\n*------*')
			print('Simulation ended.')
			print('*------*')



if __name__ == "__main__":
	CBC = ChatBotComparator()
	CBC.runSimulation()