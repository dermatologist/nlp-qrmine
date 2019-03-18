import textacy.similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Sentiment(object):

    def __init__(self):
        self._analyser = SentimentIntensityAnalyzer()
        self._return = {}

    def sentiment_analyzer_scores(self, sentence):
        score = self._analyser.polarity_scores(sentence)
        self._return["sentence"] = sentence
        self._return["score"] = score
        # print("{:-<40} {}\n".format(sentence, str(score)))
        return self._return

    def similarity(self, obj1, obj2, fuzzy_match=False, match_threshold=0.8):
        return textacy.similarity.jaccard(obj1, obj2, fuzzy_match=fuzzy_match, match_threshold=match_threshold)

    def hamming(self, str1, str2):
        textacy.similarity.hamming(str1, str2)
