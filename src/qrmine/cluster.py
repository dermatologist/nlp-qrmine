import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from pprint import pprint
class ClusterDocs:

    def __init__(self, documents=[], titles=[]):
        self._nlp = spacy.load("en_core_web_sm")
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
        # Tokenize and preprocess each document
        doc = self._nlp(doc)
        # Lemmatize and remove stop words
        tokens = [token.lemma_ for token in doc if not token.is_stop]
        return tokens

    def process(self):
        # Create a dictionary representation of the documents
        self._dictionary = corpora.Dictionary(self._processed_docs)
        # Create a bag-of-words representation of the documents
        self._corpus = [self._dictionary.doc2bow(doc) for doc in self._processed_docs]
        # Build the LDA (Latent Dirichlet Allocation) model

    def build_lda_model(self):
        self._lda_model = LdaModel(
            self._corpus, num_topics=self._num_topics, id2word=self._dictionary, passes=self._passes
        )

    def print_topics(self, num_words=5):
        if self._lda_model is None:
            self.build_lda_model()
        # Print the topics and their corresponding words
        pprint(self._lda_model.print_topics(num_words=num_words))

    def print_clusters(self):
        if self._lda_model is None:
            self.build_lda_model()
        # Perform semantic clustering
        for i, doc in enumerate(self._processed_docs):  # Changed from get_processed_docs() to _documents
            bow = self._dictionary.doc2bow(doc)
            print(f"Document {self._titles[i]} belongs to topic: {self._lda_model.get_document_topics(bow)}")
