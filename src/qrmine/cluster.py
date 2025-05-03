"""
Copyright (C) 2025 Bell Eapen

This file is part of qrmine.

qrmine is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

qrmine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with qrmine.  If not, see <https://www.gnu.org/licenses/>.
"""


import pandas as pd
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from .content import Content

class ClusterDocs:

    def __init__(self, content: Content, documents = [], titles=[]):
        self._content = content
        self._documents = documents
        self._titles = titles
        self._num_topics = 5
        self._passes = 15
        self._dictionary = None
        self._corpus = None
        self._lda_model = None
        # Apply preprocessing to each document
        self._processed_docs = [self.preprocess(doc) for doc in documents]
        self.process()

    @property
    def documents(self):
        return self._documents

    @property
    def titles(self):
        return self._titles

    @property
    def num_topics(self):
        return self._num_topics

    @property
    def passes(self):
        return self._passes

    @property
    def processed_docs(self):
        return self._processed_docs

    @documents.setter
    def documents(self, documents):
        self._documents = documents
        self._processed_docs = [self.preprocess(doc) for doc in documents]
        self.process()

    @titles.setter
    def titles(self, titles):
        self._titles = titles

    @num_topics.setter
    def num_topics(self, num_topics):
        self._num_topics = num_topics

    @passes.setter
    def passes(self, passes):
        self._passes = passes

    # Preprocess the documents using spaCy
    def preprocess(self, doc):
        self._content.content = doc
        return self._content.tokens

    def process(self):
        # Create a dictionary representation of the documents
        self._dictionary = corpora.Dictionary(self._processed_docs)
        # Create a bag-of-words representation of the documents
        self._corpus = [self._dictionary.doc2bow(doc) for doc in self._processed_docs]
        # Build the LDA (Latent Dirichlet Allocation) model

    def build_lda_model(self):
        if self._lda_model is None:
            self._lda_model = LdaModel(
                self._corpus,
                num_topics=self._num_topics,
                id2word=self._dictionary,
                passes=self._passes,
            )
        return self._lda_model.show_topics(formatted=False)

    def print_topics(self, num_words=5):
        if self._lda_model is None:
            self.build_lda_model()
        # Print the topics and their corresponding words
        # print(self._lda_model.print_topics(num_words=num_words))
        output = self._lda_model.print_topics(num_words=num_words)
        """ Output is like:
        [(0, '0.116*"category" + 0.093*"comparison" + 0.070*"incident" + 0.060*"theory" + 0.025*"Theory"'), (1, '0.040*"GT" + 0.026*"emerge" + 0.026*"pragmatic" + 0.026*"Barney" + 0.026*"contribution"'), (2, '0.084*"theory" + 0.044*"GT" + 0.044*"evaluation" + 0.024*"structure" + 0.024*"Glaser"'), (3, '0.040*"open" + 0.040*"QRMine" + 0.040*"coding" + 0.040*"category" + 0.027*"researcher"'), (4, '0.073*"coding" + 0.046*"structure" + 0.045*"GT" + 0.042*"Strauss" + 0.038*"Corbin"')]
        format this into human readable format as below:
        Topic 0: category(0.116), comparison(0.093), incident(0.070), theory(0.060), Theory(0.025)
        """
        print("\nTopics: \n")
        for topic in output:
            topic_num = topic[0]
            topic_words = topic[1]
            words = []
            for word in topic_words.split("+"):
                word = word.split("*")
                words.append(f"{word[1].strip()}({word[0].strip()})")
            print(f"Topic {topic_num}: {', '.join(words)}")
        return output

    def print_clusters(self):
        if self._lda_model is None:
            self.build_lda_model()
        # Perform semantic clustering
        print("\n Main topic in doc: \n")

        for i, doc in enumerate(
            self._processed_docs
        ):  # Changed from get_processed_docs() to _documents
            bow = self._dictionary.doc2bow(doc)
            print(
                f"Document {self._titles[i]} belongs to topic: {self._lda_model.get_document_topics(bow)}"
            )

    def format_topics_sentences(self, visualize=False):
        self.build_lda_model()
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(self._lda_model[self._corpus]):
            row = row_list[0] if self._lda_model.per_word_topics else row_list
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = self._lda_model.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    new_row = pd.DataFrame(
                        [[self._titles[i], int(topic_num), round(prop_topic, 4), topic_keywords]],
                        columns=[
                            "Title",
                            "Dominant_Topic",
                            "Perc_Contribution",
                            "Topic_Keywords",
                        ],
                    )
                    sent_topics_df = pd.concat(
                        [sent_topics_df, new_row], ignore_index=True
                    )
                else:
                    break
        sent_topics_df.columns = [
            "Title",
            "Dominant_Topic",
            "Perc_Contribution",
            "Topic_Keywords",
        ]

        # Add original text to the end of the output
        if visualize:
            contents = pd.Series(self._processed_docs)
            sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        return sent_topics_df.reset_index(drop=False)

    # https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/
    def most_representative_docs(self):
        sent_topics_df = self.format_topics_sentences()
        sent_topics_sorteddf_mallet = pd.DataFrame()
        sent_topics_outdf_grpd = sent_topics_df.groupby("Dominant_Topic")

        for i, grp in sent_topics_outdf_grpd:
            sent_topics_sorteddf_mallet = pd.concat(
                [
                    sent_topics_sorteddf_mallet,
                    grp.sort_values(["Perc_Contribution"], ascending=False).head(1),
                ],
                axis=0,
            )

        return sent_topics_sorteddf_mallet

    def topics_per_document(self, start=0, end=1):
        corpus_sel = self._corpus[start:end]
        dominant_topics = []
        topic_percentages = []
        for i, corp in enumerate(corpus_sel):
            topic_percs = self._lda_model[corp]
            dominant_topic = sorted(topic_percs, key=lambda x: x[1], reverse=True)[0][0]
            dominant_topics.append((i, dominant_topic))
            topic_percentages.append(topic_percs)
        return (dominant_topics, topic_percentages)
