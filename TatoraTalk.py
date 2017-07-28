# Voice Communication with CommU ChatterBot

from chatterbot import ChatBot, CommU
import logging

import argparse

import random
import time


parser = argparse.ArgumentParser()
parser.add_argument('-log', action='store_true', help='Turn on logging')
parser.add_argument('-commumove', action='store_true', help='Connect and use CommU Robot moving')
parser.add_argument('-commutalk', action='store_true', help='Connect and use CommU Robot speech')
parser.add_argument('-control', action='store_true', help='Control condition')
parser.add_argument('-convoforce', action='store_true', help='Force conversation start cycle')
parser.add_argument('-terminal', action='store_true', help='Use terminal commands (overrides microphone and control') 		# TERMINAL OVERRIDES CONTROL

args = parser.parse_args()

if args.log:
	# Enable info level logging
	logging.basicConfig(level=logging.INFO)

if args.terminal:
	input_adapt = "chatterbot.input.TatoraVariableInputTypeAdapter"
else:
	input_adapt = "chatterbot.input.TatoraVoiceAdapter"

chatbot = ChatBot(
	'Tatora',
	read_only=True,
	storage_adapter={
		"import_path": "chatterbot.storage.SQLAlchemyDatabaseAdapter",
		"create": True,
	},
	logic_adapters=[
		"chatterbot.logic.MitsukuChatBotAdapter",
		"chatterbot.logic.TimeLogicAdapter",
		"chatterbot.logic.DateLogicAdapter",
		#"chatterbot.logic.MathematicalEvaluation",
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
	input_adapter=input_adapt,
	output_adapter="chatterbot.output.OutputAdapter",
	database="./test",
	commu_talk=args.commutalk,
	commu_move=args.commumove,
	control=args.control,
	terminal=args.terminal,
	convoforce=args.convoforce,
)


print("Talk to Tatora! :)")
while True:
	try:
		print("Talk!")
		if args.terminal:
			user_input = raw_input('You: ')
			tatora_response = chatbot.get_response(user_input)

		else:
			tatora_response = chatbot.get_response(5)
		
		if tatora_response.text == "*actioncommand*":
			continue

		print("Tatora: "+str(tatora_response.text))

		if args.commutalk:
			chatbot.commu.say(tatora_response.text)

	except(KeyboardInterrupt, EOFError, SystemExit):
		chatbot.disconnectCommU()
		break