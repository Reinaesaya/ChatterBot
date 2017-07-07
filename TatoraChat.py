# Terminal Based Example ChatterBot

from chatterbot import ChatBot, CommU
import logging

from gtts import gTTS
import pygame

import argparse

import random
import time


parser = argparse.ArgumentParser()
parser.add_argument('-log', action='store_true', help='Turn on logging')
parser.add_argument('-readonly', action='store_true', help='Turn on read-only')
parser.add_argument('-train', action='store_true', help='Train chatbot (forces off read-only)')
parser.add_argument('-audio', action='store_true', help='Turn on audio response')
parser.add_argument('-commumove', action='store_true', help='Connect and use CommU Robot moving')
parser.add_argument('-commutalk', action='store_true', help='Connect and use CommU Robot speech')

args = parser.parse_args()

if args.log:
	# Enable info level logging
	logging.basicConfig(level=logging.INFO)

if args.readonly and not args.train:
	ro = True
else:
	ro = False

chatbot = ChatBot(
	'Tatora',
	read_only=ro,
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
		#{
		#	"import_path": "chatterbot.logic.BestMatch",
		#	"statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
		#	"response_selection_method": "chatterbot.response_selection.get_random_response"
		#},
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
	#trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	trainer='chatterbot.trainers.ConvoStarterTrainer',
	database="./test",
)

if args.train:
	# Train based on the english corpus
	print("Training")
	#chatbot.train("chatterbot.corpus.english")
	chatbot.train("/home/user2/Desktop/OUIRL-ChatBot/chatterbot/convostarters.txt")
	#chatbot.trainer.export_for_training('./tatora.json')

if args.audio:
	mp3file = 'tatora_chatbot_response.mp3'
	pygame.init()
	pygame.mixer.init()

if args.commumove or args.commutalk:
	CommURobot = CommU()
	CommURobot.openCommandSocket()
	CommURobot.openCustomCommandSocket()

print("Talk to Tatora! :)")
while True:
	try:
		override=''
		actioncomm=False
		user_input = raw_input('You: ')
		if user_input.startswith("--override "):								# --override ImageCaptioningAdapter
			override = user_input.split()[1]
			user_input = ' '.join(user_input.split()[2:])
			tatora_response = chatbot.get_response(user_input, override=override)
		elif user_input.startswith("--genconvo "):								# --genconvo sports
			keyword, exists = chatbot.check_convo_keyword(user_input.split()[1])
			#print(keyword)
			if exists:
				tatora_response = chatbot.generate_conversation(keyword)
			else:
				tatora_response = chatbot.get_response(keyword)
		elif user_input.startswith("--genconvoimage"):							# --genconvoimage random
			tatora_response = chatbot.get_response(user_input, override="ImageCaptioningAdapter")
		elif user_input.startswith("--move "):
			actioncomm=True
			if args.commumove:
				CommURobot.move(user_input.split()[1], user_input.split()[2], user_input.split()[3])
		elif user_input.startswith("--look "):
			actioncomm=True
			if args.commumove:
				CommURobot.look(user_input.split()[1], user_input.split()[2], user_input.split()[3])
		elif user_input.startswith("--takepicture"):
			actioncomm=True
			if args.commumove or args.commutalk:
				CommURobot.takepicture()
		elif user_input.startswith("--lookforconvo"):
			if args.commumove:
				x = random.sample(xrange(100,400),1)[0]*random.sample([-1,1],1)[0]
				y = random.sample(xrange(200,400),1)[0]
				z = random.sample(xrange(250,750),1)[0]
				CommURobot.look(x, y, z)
				
				picturecommandsendtime = time.time()
				CommURobot.takepicture()
				while chatbot.getcaptiontimestamp() < picturecommandsendtime:
					time.sleep(0.5)

				tatora_response = chatbot.get_response("genconvoimage", override="ImageCaptioningAdapter")
				CommURobot.look(0, 400, 500)
		elif user_input.startswith("--lookatscreenforconvo"):
			if args.commumove:
				CommURobot.move(CommURobot.AXIS['LATERAL_BODY'], 100, 100)
				CommURobot.move(CommURobot.AXIS['TURN_HEAD'], 100, 50)
				CommURobot.move(CommURobot.AXIS['PITCH_HEAD'], 0, 50)

				picturecommandsendtime = time.time()
				CommURobot.takepicture()
				while chatbot.getcaptiontimestamp() < picturecommandsendtime:
					time.sleep(0.5)

				tatora_response = chatbot.get_response("genconvoimage", override="ImageCaptioningAdapter")
				CommURobot.look(0, 400, 500)
		else:
			tatora_response = chatbot.get_response(user_input, override=override)

		if actioncomm:
			continue

		print("Tatora: "+str(tatora_response.text))

		if args.commutalk:
			CommURobot.say(tatora_response.text)
		if args.audio:
			tts = gTTS(text=tatora_response.text, lang='en-us', slow=False)
			tts.save(mp3file)
			pygame.mixer.music.load(mp3file)
			pygame.mixer.music.play()


	except(KeyboardInterrupt, EOFError, SystemExit):
		if args.commumove or args.commutalk:
			CommURobot.closeCommandSocket()
			CommURobot.closeCustomCommandSocket()
		break