import sys

import click
import textacy

from src.nlp_qrmine import Content
from src.nlp_qrmine import Network
from src.nlp_qrmine import Qrmine
from src.nlp_qrmine import ReadData
from src.nlp_qrmine import Sentiment
from src.ml_qrmine import MLQRMine

@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Will print verbose messages.")
@click.option('--inp', '-i', multiple=True, default='',
              help='Input file in the text format with <break> Topic </break>')
@click.option('--out', '-o', multiple=False, default='',
              help='Output file name')
@click.option('--csv', multiple=False, default='',
              help='csv file name')
@click.option('--corpus', '-c', multiple=True, default='',
              help='Document(s) to analyze/compare')
@click.option('--codedict', is_flag=True,
              help='Generate coding dictionary')
def cli(verbose, inp, out, csv, corpus, codedict):
    if verbose:
        click.echo("We are in the verbose mode.")
    if out:
        sys.stdout = open(out, 'w')
    if inp:
        main(inp)
    if inp and codedict:
        generate_dict(inp)


def generate_dict(inp):
    data = ReadData()
    data.read_file(inp)
    q = Qrmine()
    all_interviews = Content(data.content)
    q.print_dict(all_interviews)


def main(input_file):
    # ML
    # ml = MLQRMine()
    # ml.csvfile = "src/ml_qrmine/diabetes-risk.csv"
    # ml.prepare_data()
    # print(ml.get_nnet_predictions())
    # print("\n%s: %.2f%%" % (ml.model.metrics_names[1], ml.get_nnet_scores()[1] * 100))
    #
    # print(ml.svm_confusion_matrix())
    #
    # print(ml.knn_search(3))

    # content property returns the entire text and the documents returns the array of documents
    data = ReadData()
    data.read_file(input_file)

    q = Qrmine()
    all_interviews = Content(data.content)

    q.content = data

    ## Summary
    print(" ".join(all_interviews.generate_summary(2)))
    print("_________________________________________")

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

    q.process_content()

    print("_________________________________________")
    print("QRMine(TM) Qualitative Research Miner. v" + q.get_git_revision_short_hash)
    q.print_categories(doc)
    # q.print_topics()
    # q.print_documents()
    # q.print_dict(all_interviews)


if __name__ == '__main__':
    cli()  # run the main function
