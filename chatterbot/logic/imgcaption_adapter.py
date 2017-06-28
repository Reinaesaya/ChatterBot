from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from .best_match import BestMatch
from chatterbot.conversation import Statement
from chatterbot.constants import *

import os
import re
import random
import nltk

class ImageCaptioningAdapter(BestMatch):
    """
    The RoseChatBotAdapter returns the response that the Rose chatbot would reply with
    """

    def __init__(self, **kwargs):
        super(ImageCaptioningAdapter, self).__init__(**kwargs)
        self.adaptername = "ImageCaptioningAdapter"

        self.visual_prompts = [
            'what do you see',
            'what you see',
            'do you see something',
            'what are you looking at',
            'whats in front of you',
            'what is in front of you',
        ]

        self.caption_prompts = [
            'image captions',
            'caption the things you see',
            'caption the stuff you see',
        ]

        self.convo_starters = [
            'start a conversation with what you see',
            'start a conversation with with you see',
            'start a conversation from what you see',
            'start a conversation from what you see',
            'ask a question based on what you see',
            'genconvoimage',
        ]

    def getFreqDist(self, sentences, tag):

        all_nouns = []
        for s in sentences:
            text = nltk.word_tokenize(s)
            for word in nltk.pos_tag(text):
                if word[1] == tag:
                    all_nouns.append(word[0].lower())
            #print nltk.pos_tag(text)
        all_nouns = nltk.FreqDist(all_nouns)
        return all_nouns

    def process(self, statement):
        # Statement doesn't do anything

        # Read captions
        while os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
            continue
        open(COMMU_IMG_CAPTIONS_LOCK, 'w').close()
        with open(COMMU_IMG_CAPTIONS, 'r') as f:
            lines = f.readlines()
        os.remove(COMMU_IMG_CAPTIONS_LOCK)

        time = float(lines[0].strip())

        captions = [x.split('.')[0].strip() for x in lines[1:]]

        #response = Statement('; '.join(captions))
        #response.confidence = 0.01      # Very small (never a prioirity unless forced)
        response = self.chooseresponse(statement, captions)

        return response

    def chooseresponse(self, statement, captions):
        default_resp = "What is it I am looking at?"

        statement_cleaned = ''.join([x for x in statement.text.lower() if x.isalpha() or x==' '])

        if self.statementmatch(statement_cleaned, self.visual_prompts):
            pre_resp = [
                "I'm not certain. ",
                "Sorry, my eyesight is not so great. "
                "My visual processing is not well developed. "
            ]
            body_responses = [
                "I think I see "+' '.join([x for x in captions[0].split() if x not in ['is', 'are']]),
                "I think I'm observing "+' '.join([x for x in captions[0].split() if x not in ['is', 'are']]),
                "Can you tell me what you see?"
            ]
            response = Statement(random.choice(pre_resp)+random.choice(body_responses))
            response.confidence = 1
        elif self.statementmatch(statement_cleaned, self.caption_prompts):
            response = Statement('; '.join(captions))
            response.confidence = 1
        elif self.statementmatch(statement_cleaned, self.convo_starters):
            nouns = self.getFreqDist(captions, 'NN')
            topic_exists = False

            if 'random' in statement_cleaned:
                mc5nouns = random.shuffle(nouns.most_common(5))
            elif 'mostfrequent' in statement_cleaned:
                mc5nouns = nouns.most_common(5)
            else:
                mc5nouns = nouns.most_common(5)                                         # Default to most frequent

            for n in mc5nouns:
                keyword, topic_exists = self.chatbot.check_convo_keyword(n[0])
                if topic_exists:
                    input_statement = Statement(keyword)
                    closest_match = self.get(input_statement)
                    response_list = self.chatbot.storage.filter(
                        in_response_to__contains=closest_match.text
                    )
                    self.logger.info(
                        'Selecting response from {} optimal responses.'.format(
                            len(response_list)
                        )
                    )
                    response = self.select_response(input_statement, response_list)
                    response.confidence = closest_match.confidence
                    self.logger.info('Response selected. Using "{}"'.format(response.text))
                    break
            if not topic_exists:
                response = Statement("I don't know a concrete conversation starter for caption nouns: "+" ".join([n[0] for n in mc5nouns]))
                response.confidence = 1
        else:
            response = Statement(default_resp)
            response.confidence = 0.01

        return response

    def statementmatch(self, cleaned_statement, match_list):
        match = False
        for p in match_list:
            if p in cleaned_statement:
                match = True
                break
        return match