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
@click.option('--titles', '-t', multiple=True, default='',
              help='Document(s) title(s) to analyze/compare')
@click.option('--codedict', is_flag=True,
              help='Generate coding dictionary')
@click.option('--topics', is_flag=True,
              help='Generate topic model')
@click.option('--assign', is_flag=True,
              help='Assign documents to topics')
@click.option('--cat', is_flag=True,
              help='List categories of entire corpus or individual docs')
@click.option('--summary', is_flag=True,
              help='Generate summary for entire corpus or individual docs')
@click.option('--sentiment', is_flag=True,
              help='Generate sentiment score for entire corpus or individual docs')
@click.option('--sentence', is_flag=True,
              help='Generate sentence level scores when applicable')
@click.option('--nlp', is_flag=True,
              help='Generate all NLP reports')
def cli(verbose, inp, out, csv, titles, codedict, topics, assign, cat, summary, sentiment, sentence, nlp):
    if verbose:
        click.echo("We are in the verbose mode.")
    if out:
        sys.stdout = open(out, 'w')
    if inp and codedict:
        generate_dict(inp)
    if inp and topics:
        generate_topics(inp)
    if inp and assign:
        assign_topics(inp)
    if inp and cat:
        generate_categories(inp, titles)
    if inp and summary:
        generate_summary(inp, titles)
    if inp and sentiment:
        get_sentiment(inp, titles, sentence)
    if inp and nlp:
        main(inp)

"""
The following functions work on all the text sections.
"""
def generate_dict(inp):
    data = ReadData()
    data.read_file(inp)
    q = Qrmine()
    all_interviews = Content(data.content)
    q.print_dict(all_interviews)


def generate_topics(inp):
    data = ReadData()
    data.read_file(inp)
    q = Qrmine()
    q.content = data
    q.process_content()
    q.print_topics()


def assign_topics(inp):
    data = ReadData()
    data.read_file(inp)
    q = Qrmine()
    q.content = data
    q.process_content()
    q.print_documents()

"""
Function working at both levels
"""


def generate_categories(inp, tags):
    if len(tags) > 0:
        data = ReadData()
        data.read_file(inp)
        q = Qrmine()
        ct = 0
        for title in data.titles:
            for tag in tags:
                if title == tag:
                    print (tag)
                    content = data.documents[ct]
            ct += 1
        interview = Content(content)
        doc = textacy.Doc(interview.doc)
        q.print_categories(doc)

    else:
        data = ReadData()
        data.read_file(inp)
        q = Qrmine()
        all_interviews = Content(data.content)
        doc = textacy.Doc(all_interviews.doc)
        q.print_categories(doc)


def generate_summary(inp, tags):
    if len(tags) > 0:
        data = ReadData()
        data.read_file(inp)
        ct = 0
        for title in data.titles:
            for tag in tags:
                if title == tag:
                    print (tag)
                    content = data.documents[ct]
            ct += 1
        interview = Content(content)
        print(" ".join(interview.generate_summary(2)))
        print("_________________________________________")

    else:
        data = ReadData()
        data.read_file(inp)
        all_interviews = Content(data.content)
        print(" ".join(all_interviews.generate_summary(2)))
        print("_________________________________________")

"""
"""
def get_sentiment(inp, tags, sentence):
    if len(tags) > 0:
        data = ReadData()
        data.read_file(inp)
        ct = 0
        for title in data.titles:
            for tag in tags:
                if title == tag:
                    print (tag)
                    content = data.documents[ct]
            ct += 1
        interview = Content(content)
        doc = textacy.Doc(interview.doc)

        ## Sentiment
        s = Sentiment()

        if len(sentence) > 0:
            for sentence in doc.sents:
                if len(sentence) > 3:
                    sent = s.sentiment_analyzer_scores(sentence.text)
                    print("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))

        else:
            sent = s.sentiment_analyzer_scores(doc.text)
            print("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
           
    else:
        data = ReadData()
        data.read_file(inp)
        all_interviews = Content(data.content)
        doc = textacy.Doc(all_interviews.doc)

        ## Sentiment
        s = Sentiment()
        if len(sentence) > 0:
            for sentence in doc.sents:
                if len(sentence) > 3:
                    sent = s.sentiment_analyzer_scores(sentence.text)
                    print("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))

        else:
            sent = s.sentiment_analyzer_scores(doc.text)
            print("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))

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

    q.print_categories(doc)
    q.print_topics()
    q.print_documents()
    q.print_dict(all_interviews)


if __name__ == '__main__':
    q = Qrmine()
    print("_________________________________________")
    print("QRMine(TM) Qualitative Research Miner. v" + q.get_git_revision_short_hash)
    cli()  # run the main function
