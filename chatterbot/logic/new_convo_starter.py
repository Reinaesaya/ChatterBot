from __future__ import unicode_literals
from .best_match import BestMatch


class NewConversationStarter(BestMatch):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.
    """

    def __init__(self, **kwargs):
        super(NewConversationStarter, self).__init__(**kwargs)
        self.adaptername = "NewConversationStarter"
