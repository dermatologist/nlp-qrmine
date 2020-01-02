import pytest



@pytest.fixture
def corpus_fixture():
    from pkg_resources import resource_filename
    from src.qrmine import ReadData
    corpus = ReadData()
    file_path = resource_filename('src.qrmine.resources', 'interview.txt')
    corpus.read_file([file_path])
    return corpus 


def test_content(corpus_fixture):
    assert 'Grounded' in corpus_fixture.content

def test_documents(corpus_fixture):
    assert len(corpus_fixture.documents) == 2

def test_titles(corpus_fixture):
    assert 'P1' in corpus_fixture.titles





