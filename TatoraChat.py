# Terminal Based Example ChatterBot

from chatterbot import ChatBot
import logging

from gtts import gTTS
import pygame

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-log', action='store_true', help='Turn on logging')
parser.add_argument('-train', action='store_true', help='Train chatbot')
parser.add_argument('-audio', action='store_true', help='Turn on audio response')

args = parser.parse_args()

if args.log:
	# Enable info level logging
	logging.basicConfig(level=logging.INFO)


chatbot = ChatBot(
	'Tatora',
	read_only=False,
	storage_adapter={
		"import_path": "chatterbot.storage.SQLAlchemyDatabaseAdapter",
		"create": True,
	},
	logic_adapters=[
		"chatterbot.logic.MitsukuChatBotAdapter",
		"chatterbot.logic.TimeLogicAdapter",
		"chatterbot.logic.DateLogicAdapter",
		"chatterbot.logic.MathematicalEvaluation",
		#{
        #    "import_path": "chatterbot.logic.BestMatch",
        #    "statement_comparison_function": "chatterbot.comparisons.jaccard_similarity",
        #    "response_selection_method": "chatterbot.response_selection.get_random_response"
        #},
		#{
        #    "import_path": "chatterbot.logic.BestMatch",
        #    "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
        #    "response_selection_method": "chatterbot.response_selection.get_random_response"
        #},
	],
	preprocessors=[
		'chatterbot.preprocessors.clean_whitespace',
		'chatterbot.preprocessors.unescape_html',
	],
	filters=[
		#"chatterbot.filters.RepetitiveResponseFilter"
	],
	input_adapter="chatterbot.input.TerminalAdapter",
	output_adapter="chatterbot.output.TerminalAdapter",
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	database="./test",
)

if args.train:
	# Train based on the english corpus
	print("Training")
	chatbot.train("chatterbot.corpus.english")
	#chatbot.trainer.export_for_training('./tatora.json')

if args.audio:
	mp3file = 'tatora_chatbot_response.mp3'
	pygame.init()
	pygame.mixer.init()

print("Talk to Tatora! :)")
while True:
	try:
		tatora_response = chatbot.get_response(None)
		if args.audio:
			tts = gTTS(text=tatora_response, lang='en-us', slow=False)
			tts.save(mp3file)
			pygame.mixer.music.load(mp3file)
			pygame.mixer.music.play()


	except(KeyboardInterrupt, EOFError, SystemExit):
		break