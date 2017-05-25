from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.online_chatbots import Mitsuku

class MitsukuChatBotAdapter(LogicAdapter):
    """
    The MitsukuLogicAdapter returns the response that the Mitsuku chatbot would reply with
    """

    def __init__(self, **kwargs):
        super(MitsukuChatBotAdapter, self).__init__(**kwargs)

        self.mitsuku = Mitsuku()

    def process(self, statement):
        resp = self.mitsuku.getResponse(statement.text)
        response = Statement(resp)
        response.confidence = 0.75
        return response
