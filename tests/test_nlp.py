import pytest



@pytest.fixture
def corpus_fixture():
    from pkg_resources import resource_filename
    from src.qrmine import ReadData
    corpus = ReadData()
    file_path = resource_filename('src.qrmine.resources', 'interview.txt')
    corpus.read_file([file_path])
    return corpus

# instannce of Qrmine as fixture
@pytest.fixture
def q():
    from src.qrmine import Qrmine
    _q = Qrmine()
    return _q

# Ref: https://docs.pytest.org/en/latest/capture.html
def test_generate_dict(corpus_fixture, capsys, q):
    from src.qrmine import Content
    num = 10
    all_interviews = Content(corpus_fixture.content)
    q.print_dict(all_interviews, num)
    captured = capsys.readouterr()
    print(captured.out)
    assert 'code' in captured.out

def test_generate_topics(corpus_fixture, capsys, q):
    q.content = corpus_fixture
    q.process_content()
    q.print_topics()
    captured = capsys.readouterr()
    print(captured.out)
    assert 'TOPIC' in captured.out

def test_category_basket(corpus_fixture, capsys, q):
    q.content = corpus_fixture
    print(q.category_basket())
    captured = capsys.readouterr()
    print(captured.out)
    assert 'theory' in captured.out

def test_category_association(corpus_fixture, capsys, q):
    q.content = corpus_fixture
    print(q.category_association())
    captured = capsys.readouterr()
    print(captured.out)
    assert 'theory' in captured.out




