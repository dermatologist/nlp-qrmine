import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample documents
documents = [
    "Natural language processing is a field of AI.",
    "Topic modeling helps in uncovering the main themes in a collection of documents.",
    "Semantic clustering groups similar documents together based on meaning.",
    "SpaCy is a popular NLP library.",
    "Gensim is commonly used for topic modeling.",
]


# Preprocess the documents using spaCy
def preprocess(doc):
    # Tokenize and preprocess each document
    doc = nlp(doc)
    print(f"Original Document: {doc}")
    # Lemmatize and remove stop words
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    print(f"Processed Tokens: {tokens}")
    return tokens


# Apply preprocessing to each document
processed_docs = [preprocess(doc) for doc in documents]


# Print the processed documents
for i, doc in enumerate(processed_docs):
    print(f"Document {i + 1}: {doc}")