from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.online_chatbots import Rose

class RoseChatBotAdapter(LogicAdapter):
    """
    The RoseChatBotAdapter returns the response that the Rose chatbot would reply with
    """

    def __init__(self, **kwargs):
        super(RoseChatBotAdapter, self).__init__(**kwargs)
        self.adaptername = "RoseChatBotAdapter"

        self.rose = Rose()

    def process(self, statement):
        resp = self.rose.getResponse(statement.text)
        if resp == None:
            response = Statement("Sorry, I don't know how to reply to that")
            response.confidence = 0.1
        else:
            response = Statement(resp)
            response.confidence = 0.75
        return response
