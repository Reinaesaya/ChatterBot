from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter


class DateLogicAdapter(LogicAdapter):
    """
    The DateLogicAdapter returns the current time.
    """

    def __init__(self, **kwargs):
        super(DateLogicAdapter, self).__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = [
            'what date is it here',
            'do you know the date',
            'do you know what date it is',
            'what is the date',
            'whats the date'
        ]

        self.negative = [
            "when do we go"
            'it is time to go to sleep',
            'what is your favorite color',
            'i had a great time',
            'what is',
            'how are you',
            'it was amazing',
            'do you know where',
            'i like'
        ]

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        # train_set = apply_features(self.time_question_features, training_data)
        train_set = [(self.date_question_features(n), text) for (n, text) in labeled_data]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def date_question_features(self, text):
        """
        Provide an analysis of significan features in the string.
        """
        features = {}

        all_words = " ".join(self.positive + self.negative).split()

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def process(self, statement):
        from chatterbot.conversation import Statement

        now = datetime.now()

        time_features = self.date_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        response = Statement('Today is ' + now.strftime('%A, %B %d %Y'))

        statement_cleaned = ''.join([x for x in statement.text.lower() if x.isalpha() or x==' '])
        statement_match = False
        for p in self.positive:
            if p in statement_cleaned:
                statement_match = True
                break
        if statement_match:
            response.confidence = 1
        else:
            response.confidence = confidence*0.5
        return response
