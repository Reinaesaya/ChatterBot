from chatterbot import ChatBot
import logging

# Enable info level logging
logging.basicConfig(level=logging.INFO)


chatbot = ChatBot(
	'Tatora',
	read_only=True,
	storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
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
		"chatterbot.filters.RepetitiveResponseFilter"
	],
	input_adapter="chatterbot.input.TerminalAdapter",
	output_adapter="chatterbot.output.TerminalAdapter",
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	database="./tatora.db",
)

# Train based on the english corpus
#print("Training")
#chatbot.train("chatterbot.corpus.english")

#chatbot.trainer.export_for_training('./tatora.json')

print("Talk to Tatora! :)")
while True:
	try:
		chatbot.get_response(None)

	except(KeyboardInterrupt, EOFError, SystemExit):
		break

# while True:
# 	message = raw_input("Input: ")
# 	print("Waiting for response...")
# 	response = chatbot.get_response(message)
# 	print(response)