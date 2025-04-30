import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel

class ClusterDocs:

    def __init__(self, documents=[], titles=[]):
        self._nlp = spacy.load("en_core_web_sm")
        self._documents = documents
        self._titles = titles
        self._dictionary = None
        self._corpus = None
        # Apply preprocessing to each document
        self._processed_docs = [self.preprocess(doc) for doc in documents]
        self.process()

    @property
    def documents(self):
        return self._documents

    @property
    def titles(self):
        return self._titles

    @documents.setter
    def documents(self, documents):
        self._documents = documents
        self._processed_docs = [self.preprocess(doc) for doc in documents]
        self.process()

    @titles.setter
    def titles(self, titles):
        self._titles = titles

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

    def print_topics(self, num_topics=5, passes=15):
        # Build the LDA (Latent Dirichlet Allocation) model
        lda_model = LdaModel(self._corpus, num_topics=num_topics, id2word=self._dictionary, passes=passes)
        # Print the topics and their corresponding words
        print(lda_model.print_topics(num_words=5))

    def print_clusters(self, num_topics=5, passes=15):
        # Perform semantic clustering
        lda_model = LdaModel(self._corpus, num_topics=num_topics, id2word=self._dictionary, passes=passes)
        for i, doc in enumerate(self._processed_docs):  # Changed from get_processed_docs() to _documents
            bow = self._dictionary.doc2bow(doc)
            print(f"Document {self._titles[i]} belongs to topic: {lda_model.get_document_topics(bow)}")
