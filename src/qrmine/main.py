import sys

import click
import textacy

from . import Content
from . import Network
from . import Qrmine
from . import ReadData
from . import Sentiment
from . import MLQRMine
from . import __version__


@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Will print verbose messages.")
@click.option('--inp', '-i', multiple=True, default='',
              help='Input file in the text format with <break>Topic</break>')
@click.option('--out', '-o', multiple=False, default='',
              help='Output file name')
@click.option('--csv', multiple=False, default='',
              help='csv file name')
@click.option('--num', '-n', multiple=False, default=3,
              help='N (clusters/epochs etc depending on context)')
@click.option('--rec', '-r', multiple=False, default=3,
              help='Record (based on context)')
@click.option('--titles', '-t', multiple=True, default='',
              help='Document(s) or csv title(s) to analyze/compare')
@click.option('--filters', '-f', multiple=True, default='',
              help='Filters to apply')
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
@click.option('--sentence', is_flag=True, default=False,
              help='Generate sentence level scores when applicable')
@click.option('--nlp', is_flag=True,
              help='Generate all NLP reports')
@click.option('--nnet', is_flag=True,
              help='Display accuracy of a neural network model')
@click.option('--svm', is_flag=True,
              help='Display confusion matrix from an svm classifier')
@click.option('--knn', is_flag=True,
              help='Display nearest neighbours')
@click.option('--kmeans', is_flag=True,
              help='Display KMeans clusters')
@click.option('--cart', is_flag=True,
              help='Display Association Rules')
@click.option('--pca', is_flag=True,
              help='Display PCA')
def cli(verbose, inp, out, csv, num, rec, titles, filters, codedict, topics, assign, cat, summary, sentiment, sentence,
        nlp, nnet,
        svm,
        knn, kmeans, cart, pca):
    data = ReadData()
    if inp:
        data.read_file(inp)
    if len(filters) > 0:
        data = filter_data(inp, filters, sentence, num)
    if verbose:
        click.echo("We are in the verbose mode.")
    if out:
        sys.stdout = open(out, 'w')
    if inp and codedict:
        generate_dict(data, num)
    if inp and topics:
        generate_topics(data, assign, num)
    # if inp and assign:
    #     assign_topics(data)
    if inp and cat:
        generate_categories(data, titles, num)
    if inp and summary:
        generate_summary(data, titles)
    if inp and sentiment:
        get_sentiment(data, titles, sentence, verbose)
    if inp and cart: #python qrminer.py --cart -i src/qrmine/resources/interview.txt -n 10
        get_categories_association(data, num)
    if inp and nlp:
        main(inp)
    if csv:
        ml = MLQRMine()
        ml.csvfile = csv
        if len(titles) > 0:
            ml.titles = titles
    if csv and nnet:
        get_nnet(ml, num)
    if csv and svm:
        get_svm(ml)
    if csv and knn:
        get_knn(ml, num, rec)
    if csv and kmeans:
        get_kmeans(ml, num)
    if csv and cart:
        get_association(ml)
    if csv and pca:
        get_pca(ml, num, verbose)


"""
The following functions work on all the text sections.
"""

"""
This filters data according to search criteria

If search is empty, return entire data

If search is pos, neg or neu apply a sentiment filter

Here search is the filters applied

filters variable refers to the titles
"""


def filter_data(inp, search, sentence, num):
    data = ReadData()
    to_return = ReadData()
    data.read_file(inp)

    filters = []
    for s in search:
        if s == 'pos':
            for title in data.titles:
                t = [title]
                if get_sentiment(data, t, sentence, False) == 'pos':
                    filters.append(title)
        if s == 'neg':
            for title in data.titles:
                t = [title]
                if get_sentiment(data, t, sentence, False) == 'neg':
                    filters.append(title)
        if s == 'neu':
            for title in data.titles:
                t = [title]
                if get_sentiment(data, t, sentence, False) == 'neu':
                    filters.append(title)
        # If search itself is a title
        if any(s in l for l in data.titles):
            filters.append(s)
        # If the given category is present in the document
        for title in data.titles:
            t = [title]
            if any(s in l for l in generate_categories(data, t, num)):
                filters.append(title)

    click.echo("Selected Titles")
    for filter in filters:
        click.echo(filter)

    ct = 0
    for title in data.titles:
        if any(title in l for l in filters):
            to_return.append(title, data.documents[ct])
        ct += 1

    if len(search) > 0 and len(to_return.documents) > 0:
        click.echo("Filters applied. \n")
        return to_return
    else:
        return data


# test: test_generate_dict in test_nlp.py
def generate_dict(data, num):
    if not num:
        num = 10
    q = Qrmine()
    all_interviews = Content(data.content)
    q.print_dict(all_interviews, num)


def generate_topics(data, assign, num):
    q = Qrmine()
    q.content = data
    q.process_content()
    q.print_topics()
    if assign:
        q.print_documents(num)


# def assign_topics(data):
#     q = Qrmine()
#     q.content = data
#     q.process_content()
#     q.print_documents()

def get_categories_association(data, num):
    q = Qrmine()
    q.content = data
    click.echo(q.category_association(num))
    click.echo("Frequent Itemsets")
    click.echo("---------------------------")

"""
Function working at both levels
"""


def generate_categories(data, tags, num):
    q = Qrmine()

    if len(tags) > 0:
        ct = 0
        for title in data.titles:
            for tag in tags:
                if title == tag:
                    click.echo(tag)
                    content = data.documents[ct]
            ct += 1
        interview = Content(content)
        doc = textacy.make_spacy_doc(interview.doc)
        return q.print_categories(doc, num)

    else:
        all_interviews = Content(data.content)
        doc = textacy.make_spacy_doc(all_interviews.doc)
        return q.print_categories(doc, num)


def generate_summary(data, tags):
    if len(tags) > 0:
        ct = 0
        for title in data.titles:
            for tag in tags:
                if title == tag:
                    click.echo(tag)
                    content = data.documents[ct]
            ct += 1
        interview = Content(content)
        click.echo(" ".join(interview.generate_summary(2)))
        click.echo("_________________________________________")

    else:
        all_interviews = Content(data.content)
        click.echo(" ".join(all_interviews.generate_summary(2)))
        click.echo("_________________________________________")


"""
"""


def get_sentiment(data, tags, sentence, verbose):
    if len(tags) > 0:
        ct = 0
        for title in data.titles:
            for tag in tags:
                if title == tag:
                    click.echo(tag)
                    content = data.documents[ct]
            ct += 1
        interview = Content(content)
        doc = textacy.make_spacy_doc(interview.doc)

        ## Sentiment
        s = Sentiment()

        if sentence is True:
            for sentence in doc.sents:
                if len(sentence) > 3:
                    sent = s.sentiment_analyzer_scores(sentence.text)
                    if verbose:
                        click.echo("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
                    click.echo(s.sentiment())

        else:
            sent = s.sentiment_analyzer_scores(doc.text)
            if verbose:
                click.echo("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
            click.echo(s.sentiment())
        return s.sentiment()
    else:
        all_interviews = Content(data.content)
        doc = textacy.make_spacy_doc(all_interviews.doc)

        ## Sentiment
        s = Sentiment()
        if sentence is True:
            for sentence in doc.sents:
                if len(sentence) > 3:
                    sent = s.sentiment_analyzer_scores(sentence.text)
                    if verbose:
                        click.echo("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
                    click.echo(s.sentiment())

        else:
            sent = s.sentiment_analyzer_scores(doc.text)
            if verbose:
                click.echo("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
            click.echo(s.sentiment())
        return s.sentiment()


"""
ML
"""


def get_nnet(ml, n=3):
    ml.epochs = n
    ml.prepare_data(True)  # Oversample
    ml.get_nnet_predictions()
    click.echo("\n%s: %.2f%%" % (ml.model.metrics_names[1], ml.get_nnet_scores()[1] * 100))


def get_svm(ml):
    ml.prepare_data(True)  # Oversample
    click.echo(ml.svm_confusion_matrix())


# https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree
def get_knn(ml, n=3, r=3):
    ml.prepare_data()
    knn = ml.knn_search(n, r)
    for n in knn:
        print("Records: ", n + 1)


def get_kmeans(ml, n=3):
    ml.prepare_data()
    click.echo("K-Means Clusters:")
    click.echo(ml.get_kmeans(n))


def get_association(ml):
    ml.prepare_data()
    click.echo(ml.get_apriori())


def get_pca(ml, n=3, verbose=None):
    ml.prepare_data()
    if verbose:
        click.echo(ml.head)
    click.echo(ml.get_pca(n))


def main(input_file):
    # content property returns the entire text and the documents returns the array of documents
    data = ReadData()
    data.read_file(input_file)

    q = Qrmine()
    all_interviews = Content(data.content)

    q.content = data

    ## Summary
    click.echo(" ".join(all_interviews.generate_summary(2)))
    click.echo("_________________________________________")

    doc = textacy.make_spacy_doc(all_interviews.doc)

    ## Sentiment
    s = Sentiment()
    x = []
    for sentence in doc.sents:
        if len(sentence) > 3:
            x.append(sentence.text)
            sent = s.sentiment_analyzer_scores(sentence.text)
            click.echo("{:-<40} {}\n".format(sent["sentence"], str(sent["score"])))
            click.echo("{:-<40} {}\n".format(sentence.text, str(s.similarity(sentence.text, "Dummy sentence"))))

    ## Network
    n = Network()
    click.echo(n.sents_to_network(x))
    # n.draw_graph(True)
    click.echo(n.draw_graph(False))

    q.process_content()

    q.print_categories(doc)
    q.print_topics()
    q.print_documents()
    q.print_dict(all_interviews)


def main_routine():
    click.echo("_________________________________________")
    click.echo("QRMine(TM) Qualitative Research Miner. v" + __version__)
    cli()  # run the main function


if __name__ == '__main__':
    main_routine()
