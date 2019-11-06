import operator

import en_core_web_sm


class Content(object):
    def __init__(self, content):
        self._content = content
        self._nlp = en_core_web_sm.load()
        self._processed = self._nlp(self._content)
        self._lemma = {}
        self._pos = {}
        self._pos_ = {}
        self._word = {}
        self._sentiment = {}
        self._tag = {}
        self._dep = {}
        self._prob = {}
        self._idx = {}
        self.process()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def lemma(self, token):
        return self._lemma.get(token, '')

    @property
    def pos(self, token):
        return self._pos.get(token, '')

    @property
    def pos_(self, token):
        return self._pos_.get(token, 0)

    @property
    def word(self, token):
        return self._word.get(token, '')

    @property
    def sentiment(self, token):
        return self._sentiment.get(token, 0)

    @property
    def tag(self, token):
        return self._tag.get(token, '')

    @property
    def dep(self, token):
        return self._dep.get(token, 0)

    @property
    def prob(self, token):
        return self._prob.get(token, 0)

    @property
    def idx(self, token):
        return self._idx.get(token, 0)

    @property
    def doc(self):
        return self._processed

    def process(self):
        for token in self._processed:
            if token.is_stop or token.is_digit or token.is_punct or token.is_space:
                continue
            if token.like_url or token.like_num or token.like_email:
                continue
            if len(token.text) < 3 or token.text.isupper():
                continue
            # self._lemma[token] = token.lemma_
            self._pos[token] = token.pos_
            self._pos_[token] = token.pos
            self._word[token] = token.lemma_
            self._sentiment = token.sentiment
            self._tag = token.tag_
            self._dep = token.dep_
            self._prob = token.prob
            self._idx = token.idx

    def common_words(self, index=10):
        _words = {}
        for key, value in self._word.items():
            _words[value] = _words.get(value, 0) + 1
        return sorted(_words.items(), key=operator.itemgetter(1), reverse=True)[:index]

    def common_nouns(self, index=10):
        _words = {}
        for key, value in self._word.items():
            if self._pos.get(key, None) == 'NOUN':
                _words[value] = _words.get(value, 0) + 1
        return sorted(_words.items(), key=operator.itemgetter(1), reverse=True)[:index]

    def common_verbs(self, index=10):
        _words = {}
        for key, value in self._word.items():
            if self._pos.get(key, None) == 'VERB':
                _words[value] = _words.get(value, 0) + 1
        return sorted(_words.items(), key=operator.itemgetter(1), reverse=True)[:index]

    def sentences_with_common_nouns(self, index=10):
        _nouns = self.common_nouns(index)
        # Let's look at the sentences
        sents = []
        # the "sents" property returns spans
        # spans have indices into the original string
        # where each index value represents a token
        for span in self._processed.sents:
            # go from the start to the end of each span, returning each token in the sentence
            # combine each token using join()
            sent = ''.join(self._processed[i].string for i in range(span.start, span.end)).strip()
            for noun, freq in _nouns:
                if noun in sent:
                    sents.append(sent)
        return sents

    def spans_with_common_nouns(self, word):
        # Let's look at the sentences
        spans = []
        # the "sents" property returns spans
        # spans have indices into the original string
        # where each index value represents a token
        for span in self._processed.sents:
            # go from the start to the end of each span, returning each token in the sentence
            # combine each token using join()
            for token in span:
                if word in self._word.get(token, ' '):
                    spans.append(span)
        return spans

    def dimensions(self, word, index=3):
        _spans = self.spans_with_common_nouns(word)
        _ad = {}
        for span in _spans:
            for token in span:
                if self._pos.get(token, None) == 'ADJ':
                    _ad[self._word.get(token)] = _ad.get(self._word.get(token), 0) + 1
                if self._pos.get(token, None) == 'ADV':
                    _ad[self._word.get(token)] = _ad.get(self._word.get(token), 0) + 1
                if self._pos.get(token, None) == 'VERB':
                    _ad[self._word.get(token)] = _ad.get(self._word.get(token), 0) + 1
        return sorted(_ad.items(), key=operator.itemgetter(1), reverse=True)[:index]

    def attributes(self, word, index=3):
        _spans = self.spans_with_common_nouns(word)
        _ad = {}
        for span in _spans:
            for token in span:
                if self._pos.get(token, None) == 'NOUN' and word not in self._word.get(token, ''):
                    _ad[self._word.get(token)] = _ad.get(self._word.get(token), 0) + 1
                    # if self._pos.get(token, None) == 'VERB':
                    # _ad[self._word.get(token)] = _ad.get(self._word.get(token), 0) + 1
        return sorted(_ad.items(), key=operator.itemgetter(1), reverse=True)[:index]

    # this is function for text summarization

    def generate_summary(self, weight=10):
        words = self.common_words()
        spans = []
        ct = 0
        for key, value in words:
            ct += 1
            if ct > weight:
                continue
            for span in self.spans_with_common_nouns(key):
                spans.append(span.text)
        return list(dict.fromkeys(spans))  # remove duplicates
