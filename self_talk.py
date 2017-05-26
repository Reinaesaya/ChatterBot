from chatterbot import ChatBot
import logging

import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store_true', help='Turn on logging')
parser.add_argument('-t', action='store_true', help='Train chatbot')
parser.add_argument('-ro', action='store_true', help='Read-only (do not learn from conversation)')

args = parser.parse_args()

if args.l:
	# Enable info level logging
	logging.basicConfig(level=logging.INFO)

if args.ro:
	print("ChatBots initiated with read-only. Learning OFF")
else:
	print("ChatBots not initiated with read-only. Learning ON")

CB1 = ChatBot(
	'M',
	read_only=args.ro,
	storage_adapter="chatterbot.storage.SQLAlchemyDatabaseAdapter",
	logic_adapters=[
		"chatterbot.logic.MitsukuChatBotAdapter",
		"chatterbot.logic.TimeLogicAdapter",
		"chatterbot.logic.DateLogicAdapter",
		"chatterbot.logic.MathematicalEvaluation",
	],
	preprocessors=[
		'chatterbot.preprocessors.clean_whitespace',
		'chatterbot.preprocessors.unescape_html',
	],
	filters=[
		"chatterbot.filters.RepetitiveResponseFilter"
	],
	input_adapter="chatterbot.input.VariableInputTypeAdapter",
	output_adapter="chatterbot.output.OutputAdapter",
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	database="./test.db",
)

CB2 = ChatBot(
	'R',
	read_only=args.ro,
	storage_adapter="chatterbot.storage.SQLAlchemyDatabaseAdapter",
	logic_adapters=[
		"chatterbot.logic.RoseChatBotAdapter",
		"chatterbot.logic.TimeLogicAdapter",
		"chatterbot.logic.DateLogicAdapter",
		"chatterbot.logic.MathematicalEvaluation",
	],
	preprocessors=[
		'chatterbot.preprocessors.clean_whitespace',
		'chatterbot.preprocessors.unescape_html',
	],
	filters=[
		"chatterbot.filters.RepetitiveResponseFilter"
	],
	input_adapter="chatterbot.input.VariableInputTypeAdapter",
	output_adapter="chatterbot.output.OutputAdapter",
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	database="./test.db",
)

if args.t:
	# Train based on the english corpus
	print("Training")
	CB1.train("chatterbot.corpus.english")
	CB2.train("chatterbot.corpus.english")
	#chatbot.trainer.export_for_training('./test.json')


print("ChatBot talking to each other!")
first = raw_input('Conversation start: ')
resp1 = CB1.get_response(first)
resp2 = ""
while True:
	try:
		#time.sleep(1)
		print('CB1: '+resp1.text)
		resp2 = CB2.get_response(resp1.text)
		#time.sleep(1)
		print('CB2: '+resp2.text)
		resp1 = CB1.get_response(resp2.text)

	except(KeyboardInterrupt, EOFError, SystemExit):
		break