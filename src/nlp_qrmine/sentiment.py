from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Sentiment(object):

    def __init__(self):
        self._analyser = SentimentIntensityAnalyzer()

    def sentiment_analyzer_scores(self, sentence):
        score = self._analyser.polarity_scores(sentence)
        print("{:-<40} {}".format(sentence, str(score)))
