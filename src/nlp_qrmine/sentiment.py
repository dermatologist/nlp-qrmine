import textacy.similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import operator

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

    """
    Returns the sentiment with maximum score
    
    pos, neg or neu

    The Positive, Negative and Neutral scores represent the proportion of text that falls in these categories.

    The Compound score is a metric that calculates the sum of all the lexicon ratings which have been normalized between -1(most extreme negative) and +1 (most extreme positive). 

    More here: https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f
    
    """

    def sentiment(self):
        self._return["score"].pop("compound", None)
        return max(self._return["score"].items(), key=operator.itemgetter(1))[0]
