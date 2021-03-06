from __future__ import unicode_literals
from chatterbot.adapters import Adapter
from chatterbot.conversation import Statement
from chatterbot.constants import *
import random
import time


class InputAdapter(Adapter):
	"""
	This is an abstract class that represents the
	interface that all input adapters should implement.
	"""

	def __init__(self, **kwargs):
		super(InputAdapter, self).__init__(**kwargs)
		self.abstractadaptertype = "NORMAL"

		self.genconvoimage = [
			"generate conversation from image",
			"make conversation from image",
			"genconvoimage",
		]

		self.takepicture = [
			"take picture",
			"take a picture",
			"takepicture",
		]

		self.lookforconvo = [
			"look for conversation",
			"lookforconvo",
		]

		self.lookatscreenforconvo = [
			"look at screen for conversation",
			"new topic",
			"new topic of conversation",
			"new conversation",
			"what is on the screen",
			"lookatscreenforconvo",
		]

		self.cycle = 0

	def process_input(self, *args, **kwargs):
		"""
		Returns a statement object based on the input source.
		"""
		raise self.AdapterMethodNotImplementedError()

	def process_input_statement(self, *args, **kwargs):
		"""
		Return an existing statement object (if one exists).
		"""
		input_statement = self.process_input(*args, **kwargs)
		self.logger.info('Received input statement: {}'.format(input_statement.text))

		existing_statement = self.chatbot.storage.find(input_statement.text)

		if existing_statement:
			self.logger.info('"{}" is a known statement'.format(input_statement.text))
			input_statement = existing_statement
			exists = True
		else:
			self.logger.info('"{}" is not a known statement'.format(input_statement.text))
			exists = False

		return input_statement, exists

	def check_if_known(self, s):
		input_statement = Statement(s)
		self.logger.info('Received input statement: {}'.format(input_statement.text))

		existing_statement = self.chatbot.storage.find(input_statement.text)

		if existing_statement:
			self.logger.info('"{}" is a known statement'.format(input_statement.text))
			input_statement = existing_statement
			exists = True
		else:
			self.logger.info('"{}" is not a known statement'.format(input_statement.text))
			exists = False

		return input_statement, exists


	def process_input_statement_cmdline(self, *args, **kwargs):
		"""
		Return an existing statement object (if one exists).
		"""
		input_statement = self.process_input(*args, **kwargs)
		self.logger.info('Received input statement: {}'.format(input_statement.text))

		override = ''

		if input_statement.text.startswith("--override "):                                # --override ImageCaptioningAdapter
			override = input_statement.text.split()[1]
			input_statement = Statement(' '.join(input_statement.text.split()[2:]))

		elif input_statement.text.startswith("--genconvo "):                              # --genconvo sports
			keyword, exists = self.chatbot.check_convo_keyword(input_statement.text.split()[1])
			print(keyword)
			if exists:
				tatora_response = self.chatbot.generate_conversation(keyword)
				override = "NewConversationStarter"
				input_statement = Statement(keyword.lower())

		elif input_statement.text.startswith("--genconvoimage"):                          # --genconvoimage random
			override = "ImageCaptioningAdapter"

		elif input_statement.text.startswith("--move "):
			if self.chatbot.commu_move:
				self.chatbot.commu.move(input_statement.text.split()[1], input_statement.text.split()[2], input_statement.text.split()[3])
			input_statement = Statement("*actioncommand*")

		elif input_statement.text.startswith("--look "):
			if self.chatbot.commu_move:
				self.chatbot.commu.look(input_statement.text.split()[1], input_statement.text.split()[2], input_statement.text.split()[3])
			input_statement = Statement("*actioncommand*")

		elif input_statement.text.startswith("--takepicture"):
			if self.chatbot.commu is not None:
				self.chatbot.commu.takepicture()
			input_statement = Statement("*actioncommand*")

		elif input_statement.text.startswith("--lookforconvo"):
			if self.chatbot.commu_move:
				x = random.sample(xrange(100,400),1)[0]*random.sample([-1,1],1)[0]
				y = random.sample(xrange(200,400),1)[0]
				z = random.sample(xrange(250,750),1)[0]
				self.chatbot.commu.look(x, y, z)
				
				picturecommandsendtime = time.time()
				self.chatbot.commu.takepicture()
				while self.chatbot.getcaptiontimestamp() < picturecommandsendtime:
					time.sleep(0.5)

				self.chatbot.resetCommU_initPos()
				input_statement = Statement("genconvoimage")
				override = "ImageCaptioningAdapter"

		elif input_statement.text.startswith("--lookatscreenforconvo"):
			if self.chatbot.commu_move:
				self.chatbot.commu.move(self.chatbot.commu.AXIS['LATERAL_BODY'], 100, 100)
				self.chatbot.commu.move(self.chatbot.commu.AXIS['TURN_HEAD'], 100, 50)
				self.chatbot.commu.move(self.chatbot.commu.AXIS['PITCH_HEAD'], 0, 25)

				picturecommandsendtime = time.time()
				self.chatbot.commu.takepicture()
				while self.chatbot.getcaptiontimestamp() < picturecommandsendtime:
					time.sleep(0.5)

				self.chatbot.resetCommU_initPos()
				input_statement = Statement("genconvoimage")
				override = "ImageCaptioningAdapter"

		else:
			pass


		existing_statement = self.chatbot.storage.find(input_statement.text)

		if existing_statement:
			self.logger.info('"{}" is a known statement'.format(input_statement.text))
			input_statement = existing_statement
			exists = True
		else:
			self.logger.info('"{}" is not a known statement'.format(input_statement.text))
			exists = False

		return input_statement, exists, override



	def process_input_statement_tatora(self, *args, **kwargs):
		"""
		Return an existing statement object (if one exists).
		"""
		self.cycle += 1

		input_statement = self.process_input(*args, **kwargs)
		self.logger.info('Received input statement: {}'.format(input_statement.text))

		override = ''

		cleaned = self.cleansentence(input_statement.text)

		if self.statementmatch(cleaned, self.lookatscreenforconvo) or \
				(self.convoforce and self.cycle >= CONVOSTART_FORCE):
			if self.chatbot.commu_move:
				self.chatbot.commu.move(self.chatbot.commu.AXIS['LATERAL_BODY'], 100, 100)
				self.chatbot.commu.move(self.chatbot.commu.AXIS['TURN_HEAD'], 100, 50)
				self.chatbot.commu.move(self.chatbot.commu.AXIS['PITCH_HEAD'], 0, 150)

				picturecommandsendtime = time.time()
				self.chatbot.commu.takepicture()
				while self.chatbot.getcaptiontimestamp() < picturecommandsendtime:
					time.sleep(0.5)

				self.chatbot.resetCommU_initPos()
				input_statement = Statement("genconvoimage")
				override = "ImageCaptioningAdapter"

				if (self.convoforce and self.cycle >= CONVOSTART_FORCE):
					print("Forcing new conversation")
				self.cycle = 0

		elif self.statementmatch(cleaned, self.genconvoimage):
			input_statement = Statement("genconvoimage")
			override = "ImageCaptioningAdapter"

		elif self.statementmatch(cleaned, self.takepicture):
			if self.chatbot.commu is not None:
				self.chatbot.commu.takepicture()
			input_statement = Statement("*actioncommand*")

		elif self.statementmatch(cleaned, self.lookforconvo):
			if self.chatbot.commu_move:
				x = random.sample(xrange(100,400),1)[0]*random.sample([-1,1],1)[0]
				y = random.sample(xrange(200,400),1)[0]
				z = random.sample(xrange(250,750),1)[0]
				self.chatbot.commu.look(x, y, z)
				
				picturecommandsendtime = time.time()
				self.chatbot.commu.takepicture()
				while self.chatbot.getcaptiontimestamp() < picturecommandsendtime:
					time.sleep(0.5)

				self.chatbot.resetCommU_initPos()
				input_statement = Statement("genconvoimage")
				override = "ImageCaptioningAdapter"

		else:
			pass


		existing_statement = self.chatbot.storage.find(input_statement.text)

		if existing_statement:
			self.logger.info('"{}" is a known statement'.format(input_statement.text))
			input_statement = existing_statement
			exists = True
		else:
			self.logger.info('"{}" is not a known statement'.format(input_statement.text))
			exists = False

		return input_statement, exists, override


	def process_input_statement_tatoraControl(self, *args, **kwargs):
		"""
		Return an existing statement object (if one exists).
		"""
		self.cycle += 1

		input_statement = self.process_input(*args, **kwargs)
		self.logger.info('Received input statement: {}'.format(input_statement.text))

		override = ''

		cleaned = self.cleansentence(input_statement.text)

		if self.statementmatch(cleaned, self.genconvoimage) or \
				self.statementmatch(cleaned, self.lookforconvo) or \
				self.statementmatch(cleaned, self.lookatscreenforconvo) or \
				(self.convoforce and self.cycle >= CONVOSTART_FORCE):
			input_statement = Statement("genconvoimage")
			override = "ImageCaptioningAdapter"

			if (self.convoforce and self.cycle >= CONVOSTART_FORCE):
				print("Forcing new conversation")
			self.cycle = 0

		else:
			pass


		existing_statement = self.chatbot.storage.find(input_statement.text)

		if existing_statement:
			self.logger.info('"{}" is a known statement'.format(input_statement.text))
			input_statement = existing_statement
			exists = True
		else:
			self.logger.info('"{}" is not a known statement'.format(input_statement.text))
			exists = False

		return input_statement, exists, override


	def statementmatch(self, cleaned_statement, match_list):
		match = False
		for p in match_list:
			if p in cleaned_statement:
				match = True
				break
		return match

	def cleansentence(self, sentence):
		cleaned = ''.join([x for x in sentence.lower() if x.isalpha() or x==' '])
		return cleaned
