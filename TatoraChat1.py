# Terminal Based Example ChatterBot

from chatterbot import TatoraBot
import logging

import argparse

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

chatbot = TatoraBot(database='./test', commu_move=args.commumove, commu_say=args.commutalk, pygame_say=args.audio, readonly=args.readonly)

if args.train:
	#chatbot.trainall("/home/user2/Desktop/OUIRL-ChatBot/chatterbot/convostarters.txt")
	chatbot.train_convostart("/home/user2/Desktop/OUIRL-ChatBot/chatterbot/convostarters.txt")


chatbot.converse()