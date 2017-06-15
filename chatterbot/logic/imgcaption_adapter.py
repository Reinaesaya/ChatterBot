from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.constants import *

import os
import re
import random

class ImageCaptioningAdapter(LogicAdapter):
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



    def process(self, statement):
        # Statement doesn't do anything

        # Read captions
        while os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
            continue
        open(COMMU_IMG_CAPTIONS_LOCK, 'w').close()
        with open(COMMU_IMG_CAPTIONS, 'r') as f:
            lines = f.readlines()
        os.remove(COMMU_IMG_CAPTIONS_LOCK)

        captions = [x.split('.')[0].strip() for x in lines]

        #response = Statement('; '.join(captions))
        #response.confidence = 0.01      # Very small (never a prioirity unless forced)
        response = self.chooseresponse(statement, captions)

        return response

    def chooseresponse(self, statement, captions):

        tempresp = 'I think I see '+''.join([x for x in captions[0] if x not in ['is', 'are']])
        response = Statement(tempresp)

        statement_cleaned = ''.join([x for x in statement.text.lower() if x.isalpha() or x==' '])

        prompt_match = False
        for p in self.visual_prompts:
            if p in statement_cleaned:
                prompt_match = True
                break
        if prompt_match:
            tempresp = 'I think I see '+''.join([x for x in captions[0] if x not in ['is', 'are']])
            response = Statement(tempresp)
            response.confidence = 1
        else:
            response.confidence = 0.01
        return response