import sys

import click
import textacy
from textacy.vsm.vectorizers import Vectorizer

from src.ml_qrmine import MLQRMine
from src.nlp_qrmine import Content
from src.nlp_qrmine import Network
from src.nlp_qrmine import Qrmine
from src.nlp_qrmine import ReadData
from src.nlp_qrmine import Sentiment


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--inp', '-i', multiple=False, default='',
              help='Input file in the text format with <break> Topic </break>')
@click.option('--out', '-o', multiple=False, default='',
              help='Output file name')
@click.option('--csv', '-c', multiple=False, default='qrmine_output.txt',
              help='csv file name')
def cli(verbose, inp, out, csv):
    if verbose:
        click.echo("We are in the verbose mode.")
    if out:
        sys.stdout = open(out, 'w')
    if inp:
        main(inp)


def main(input_file):
    ## ML
    ml = MLQRMine()
    ml.csvfile = "src/ml_qrmine/diabetes-risk.csv"
    ml.prepare_data()
    print(ml.get_nnet_predictions())



    # content property returns the entire text and the documents returns the array of documents
    data = ReadData()
    data.read_file(input_file)

    q = Qrmine()
    all_interviews = Content(data.content)

    doc = textacy.Doc(all_interviews.doc)

    ## Sentiment
    s = Sentiment()
    x = []
    for sentence in doc.sents:
        if len(sentence) > 3:
            x.append(sentence.text)
            sent = s.sentiment_analyzer_scores(sentence.text)
            print("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
            print("{:-<40} {}\n".format(sentence.text, str(s.similarity(sentence.text, "Dummy sentence"))))

    ## Network
    n = Network()
    print(n.sents_to_network(x))
    # n.draw_graph(True)
    print(n.draw_graph(False))

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
    doc_term_matrix = vectorizer.fit_transform((documents.to_terms_list(ngrams=(1, 2, 3), named_entities=True,
                                                                        as_strings=True, filter_stops=True,
                                                                        filter_punct=True, filter_nums=True, min_freq=1)
                                                for documents in corpus))
    number_docs, terms = doc_term_matrix.shape
    model = textacy.TopicModel('nmf', n_topics=number_docs)
    model.fit(doc_term_matrix)

    doc_topic_matrix = model.transform(doc_term_matrix)

    _, number_topics = doc_topic_matrix.shape

    print("_________________________________________")
    print("QRMine(TM) Qualitative Research Miner. v" + q.get_git_revision_short_hash)
    q.print_categories(doc)
    q.print_topics(model, vectorizer, number_topics)
    q.print_documents(model, corpus, doc_topic_matrix, number_topics)
    q.print_dict(all_interviews)


if __name__ == '__main__':
    cli()  # run the main function
