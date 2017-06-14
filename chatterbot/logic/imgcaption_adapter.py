from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.constants import *

import os

class ImageCaptioningAdapter(LogicAdapter):
    """
    The RoseChatBotAdapter returns the response that the Rose chatbot would reply with
    """

    def __init__(self, **kwargs):
        super(ImageCaptioningAdapter, self).__init__(**kwargs)
        self.adaptername = "ImageCaptioningAdapter"

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

        response = Statement('; '.join(captions))
        response.confidence = 0.01      # Very small (never a prioirity unless forced)

        return response