# Terminal Based Example ChatterBot
from __future__ import unicode_literals

from .chatterbot import ChatBot
from .commu import CommU
import logging

from gtts import gTTS
import pygame

import random
import time



class TatoraBot(object):
	def __init__(self, database, commu_move=False, commu_say=False, pygame_say=False, mp3file='tatora_chatbot_response.mp3', readonly=True):
		self._readonly = readonly
		self._commu_move = commu_move
		self._commu_say = commu_say
		self._pygame_say = pygame_say
		self.mp3file = mp3file

		self.dbname = database

		self.initTrainingBots()
		self.initChatBot()

		if self._pygame_say:
			self.initPygameAudio()



	def initTrainingBots(self):
		self.trainingbots = {
			"english corpus": ChatBot(
				'English Corpus Trainer',
				read_only=False,
				storage_adapter={
				"import_path": "chatterbot.storage.SQLAlchemyDatabaseAdapter",
				"create": True,
				},
				preprocessors=[
					'chatterbot.preprocessors.clean_whitespace',
					'chatterbot.preprocessors.unescape_html',
				],
				trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
				database=self.dbname,
			),
			"convo starter": ChatBot(
				'Convo Starter Trainer',
				read_only=False,
				storage_adapter={
				"import_path": "chatterbot.storage.SQLAlchemyDatabaseAdapter",
				"create": True,
				},
				preprocessors=[
					'chatterbot.preprocessors.clean_whitespace',
					'chatterbot.preprocessors.unescape_html',
				],
				trainer='chatterbot.trainers.ConvoStarterTrainer',
				database=self.dbname,
			),
		}

		return self.trainingbots

	def initChatBot(self):
		self.chatbot = ChatBot(
			'Tatora',
			read_only=self._readonly,
			storage_adapter={
				"import_path": "chatterbot.storage.SQLAlchemyDatabaseAdapter",
				"create": True,
			},
			logic_adapters=[
				"chatterbot.logic.MitsukuChatBotAdapter",
				"chatterbot.logic.TimeLogicAdapter",
				"chatterbot.logic.DateLogicAdapter",
				"chatterbot.logic.MathematicalEvaluation",
				"chatterbot.logic.ImageCaptioningAdapter",
				{
					"import_path": "chatterbot.logic.NewConversationStarter",
					"statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
					"response_selection_method": "chatterbot.response_selection.get_random_response"
				},
				#{
				#    "import_path": "chatterbot.logic.BestMatch",
				#    "statement_comparison_function": "chatterbot.comparisons.jaccard_similarity",
				#    "response_selection_method": "chatterbot.response_selection.get_random_response"
				#},
				{
					"import_path": "chatterbot.logic.BestMatch",
					"statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
					"response_selection_method": "chatterbot.response_selection.get_random_response"
				},
			],
			preprocessors=[
				'chatterbot.preprocessors.clean_whitespace',
				'chatterbot.preprocessors.unescape_html',
			],
			filters=[
				#"chatterbot.filters.RepetitiveResponseFilter"
			],
			input_adapter="chatterbot.input.VariableInputTypeAdapter",
			output_adapter="chatterbot.output.OutputAdapter",
			database=self.dbname,
		)

		return self.chatbot


# Training
	def trainall(self, convostarterpath):
		self.train_engcorp()
		self.train_convostart(convostarterpath)

	def train_convostart(self, convostarterpath):
		print("Training conversation starters")
		self.trainingbots["convo starter"].train(convostarterpath)

	def train_engcorp(self):
		print("Training english corpus")
		self.trainingbots["english corpus"].train("chatterbot.corpus.english")



	def initPygameAudio(self):
		pygame.init()
		pygame.mixer.init()

	def initCommU(self):
		self.CommURobot = CommU()
		self.CommURobot.openCommandSocket()

	def disconnectCommU(self):
		self.CommURobot.closeCommandSocket()

	def playPygameAudio(self, response_statement):
		tts = gTTS(text=response_statement.text, lang='en-us', slow=False)
		tts.save(self.mp3file)
		pygame.mixer.music.load(self.mp3file)
		pygame.mixer.music.play()

	def converse(self):
		if self._commu_move or self._commu_say:
			self.initCommU()
		print("Talk to Tatora! :)")
		try:
			while True:
				override=''
				actioncomm=False
				user_input = raw_input('You: ')
				if user_input.startswith("--override "):								# --override ImageCaptioningAdapter
					override = user_input.split()[1]
					user_input = ' '.join(user_input.split()[2:])
					tatora_response = self.chatbot.get_response(user_input, override=override)
				elif user_input.startswith("--genconvo "):								# --genconvo sports
					keyword, exists = self.chatbot.check_convo_keyword(user_input.split()[1])
					#print(keyword)
					if exists:
						tatora_response = self.chatbot.generate_conversation(keyword)
					else:
						tatora_response = self.chatbot.get_response(keyword)
				elif user_input.startswith("--genconvoimage"):							# --genconvoimage random
					tatora_response = self.chatbot.get_response(user_input, override="ImageCaptioningAdapter")
				elif user_input.startswith("--move "):
					actioncomm=True
					if self._commu_move:
						self.CommURobot.move(user_input.split()[1], user_input.split()[2], user_input.split()[3])
				elif user_input.startswith("--look "):
					actioncomm=True
					if self._commu_move:
						self.CommURobot.look(user_input.split()[1], user_input.split()[2], user_input.split()[3])
				elif user_input.startswith("--lookforconvo"):
					if self._commu_move:
						x = random.sample(xrange(100,400),1)[0]*random.sample([-1,1],1)[0]
						y = random.sample(xrange(200,400),1)[0]
						z = random.sample(xrange(250,750),1)[0]
						self.CommURobot.look(x, y, z)
						time.sleep(1)
						tatora_response = self.chatbot.get_response("genconvoimage", override="ImageCaptioningAdapter")
						self.CommURobot.look(0, 300, 300)
				elif user_input.startswith("--endconvo"):
					print("Bye bye!")
					break
				else:
					tatora_response = self.chatbot.get_response(user_input, override=override)

				if actioncomm:
					continue

				print("Tatora: "+str(tatora_response.text))

				if self._commu_say:
					self.CommURobot.say(tatora_response.text)
				if self._pygame_say:
					tts = gTTS(text=tatora_response.text, lang='en-us', slow=False)
					tts.save(self.mp3file)
					pygame.mixer.music.load(self.mp3file)
					pygame.mixer.music.play()
		except KeyboardInterrupt as e:
			pass
		finally:
			if self._commu_move or self._commu_say:
				self.disconnectCommU()