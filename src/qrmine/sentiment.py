import textacy.similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import operator
from .content import Content

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

    def get_sentiment(self, read_data, tags=[], sentence=False, verbose=True):
        # if read_data is string
        if isinstance(read_data, str):
            content = read_data
        else:
            content = ""
            if len(tags) > 0:
                ct = 0
                for title in read_data.titles:
                    for tag in tags:
                        if title == tag:
                            content += read_data.documents[ct]
                        ct += 1
            else:
                for title in read_data.titles:
                    content += read_data.documents[title]
        c = Content(content)
        spacy_doc = c.spacy_doc

        if sentence is True:
            for sentence in spacy_doc.sents:
                if len(sentence) > 3:
                    sent = self.sentiment_analyzer_scores(sentence.text)
                    if verbose:
                        print(
                            "{:-<40} {}\n".format(sent["sentence"][:10] + "...", str(sent["score"]))
                        )
                    print(self.sentiment())
        else:
            sent = self.sentiment_analyzer_scores(content)
            if verbose:
                print(
                    "{:-<40} {}\n".format(
                        sent["sentence"][:10] + "...", str(sent["score"])
                    )
                )
            print(self.sentiment())
        return self.sentiment()
