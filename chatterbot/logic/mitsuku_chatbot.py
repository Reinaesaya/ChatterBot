from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.online_chatbots import Mitsuku

class MitsukuChatBotAdapter(LogicAdapter):
    """
    The MitsukuChatBotAdapter returns the response that the Mitsuku chatbot would reply with
    """

    def __init__(self, **kwargs):
        super(MitsukuChatBotAdapter, self).__init__(**kwargs)
        self.adaptername = "MitsukuChatBotAdapter"

        self.mitsuku = Mitsuku()

    def process(self, statement):
        resp = self.mitsuku.getResponse(statement.text)
        if resp == None:
            response = Statement("Sorry, I don't know how to reply to that")
            response.confidence = 0.1
        else:
            response = Statement(resp)
            response.confidence = 0.9
        return response
