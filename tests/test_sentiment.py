import pytest


@pytest.fixture
def corpus_fixture():
    from pkg_resources import resource_filename
    from src.qrmine import ReadData

    corpus = ReadData()
    file_path = resource_filename("src.qrmine.resources", "interview.txt")
    corpus.read_file(file_path)
    return corpus


def test_sentiment(corpus_fixture, capsys):
    from src.qrmine import Sentiment
    s = Sentiment()
    for title, doc in zip(corpus_fixture.titles, corpus_fixture.documents):
        # Get the sentiment score
        sentiment = s.get_sentiment(doc, tags=[], sentence=False, verbose=True)
        # Print the sentiment score
        print(f"Title: {title}")
        print(f"Sentiment: {sentiment}")
