import subprocess

import textacy
from textacy.vsm.vectorizers import Vectorizer

from src.nlp_qrmine import Content
from src.nlp_qrmine import ReadData
from src.nlp_qrmine import __version__


def main():
    # content property returns the entire text and the documents returns the array of documents
    data = ReadData()
    all_interviews = Content(data.content)

    doc = textacy.Doc(all_interviews.doc)


    # create an empty corpus
    en = textacy.load_spacy('en_core_web_sm', disable=('parser',))
    corpus = textacy.Corpus(lang=en)

    ct = 0
    for document in data.documents:
        metadata = {}
        try:
            metadata['title'] = data.titles[ct]
        except IndexError:
            metadata['title'] = 'Empty'
        corpus.add_text(textacy.preprocess_text(document, lowercase=True, no_punct=True, no_numbers=True),
                        metadata=metadata)
        ct += 1
    vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth',
                            norm='l2', min_df=3, max_df=0.95, max_n_terms=100000)
    doc_term_matrix = vectorizer.fit_transform((documents.to_terms_list(ngrams=(1, 2, 3), named_entities=True, as_strings=True, filter_stops=True, filter_punct=True, filter_nums=True, min_freq=1)
                                                for documents in corpus))
    number_docs, terms = doc_term_matrix.shape
    model = textacy.TopicModel('nmf', n_topics=number_docs)
    model.fit(doc_term_matrix)

    doc_topic_matrix = model.transform(doc_term_matrix)

    _, number_topics = doc_topic_matrix.shape


    print("_________________________________________")
    print("QRMine(TM) Qualitative Research Miner. v" + get_git_revision_short_hash())
    print (__version__)
    print("\n")
    print("gtdict - Grounded Coding Dictionary\n")
    print_categories(doc)
    print_topics(model, vectorizer, number_topics)
    print_documents(model, corpus, doc_topic_matrix, number_topics)
    print_dict(all_interviews)



def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode("utf-8")
    # return subprocess.check_output(['git', 'log', '-1', '--format=%cd']).strip().decode("utf-8")[10:]


def print_categories(doc):
    bot = doc.to_bag_of_terms(ngrams=(2, 3), named_entities=True, normalize='lemma', weighting='count',
                              as_strings=True, filter_stops=True, filter_punct=True, filter_nums=True, min_freq=2)
    categories = sorted(bot.items(), key=lambda x: x[1], reverse=True)[:15]
    output = []
    print("\n\n---Categories with count---")
    output.append(("CATEGORY", "COUNT"))
    for category, count in categories:
        output.append((category, str(count)))
    print_table(output)
    print("---------------------------\n\n")


def print_topics(model, vectorizer, number_topics):
    topic_list = list(range(1, number_topics))
    output = []
    print("\n\n---Topics---")
    output.append(("TOPIC", "DESCRIPTION"))
    for topic_idx, top_terms in model.top_topic_terms(vectorizer.id_to_term, topics=topic_list):
        output.append(("TOPIC:" + str(topic_idx), '   '.join(top_terms)))
    print_table(output)
    print("---------------------------\n\n")


def print_documents(model, corpus, doc_topic_matrix, number_topics):
    topic_list = list(range(1, number_topics))
    output = []
    print("\n\n---Topics---")
    output.append(("TOPIC", "DOCUMENTS"))
    for topic_idx, top_docs in model.top_topic_docs(doc_topic_matrix, topics=topic_list, top_n=2):
        str_topic_idx = str(topic_idx)
        for j in top_docs:
            output.append((str_topic_idx, corpus[j].metadata['title']))
            str_topic_idx = "..."
    print_table(output)
    print("---------------------------\n\n")


def print_dict(content):
    output = []
    print("\n\n---Coding Dictionary---")
    output.append(("CATEGORY", "PROPERTY", "DIMENSION"))
    words = content.common_verbs(10)
    for word, f1 in words:
        for attribute, f2 in content.attributes(word, 3):
            for dimension, f3 in content.dimensions(attribute, 3):
                output.append((word, attribute, dimension))
                word = '...'
                attribute = '...'

    print_table(output)
    print("---------------------------\n\n")


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
