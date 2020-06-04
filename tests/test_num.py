import pytest



@pytest.fixture
def ml_fixture():
    from pkg_resources import resource_filename
    from src.qrmine import MLQRMine
    ml = MLQRMine()
    file_path = resource_filename('src.qrmine.resources', 'numeric.csv')
    ml.csvfile = file_path
    return ml 



# Ref: https://docs.pytest.org/en/latest/capture.html
def test_nn(ml_fixture, capsys):
    ml_fixture.epochs = 2
    ml_fixture.prepare_data(True)
    ml_fixture.get_nnet_predictions()
    captured = capsys.readouterr()
    assert 'accuracy' in captured.out

def test_svm(ml_fixture, capsys):
    ml_fixture.prepare_data(True)
    print(ml_fixture.svm_confusion_matrix())
    captured = capsys.readouterr()
    assert '[4 0]' in captured.out

def test_knn(ml_fixture, capsys):
    ml_fixture.prepare_data()
    print(ml_fixture.knn_search())
    captured = capsys.readouterr()
    assert '[ 2 11 12]' in captured.out

def test_kmeans(ml_fixture, capsys):
    ml_fixture.prepare_data()
    print(ml_fixture.get_kmeans())
    captured = capsys.readouterr()
    assert 'Cluster Length' in captured.out

def test_pca(ml_fixture, capsys):
    ml_fixture.prepare_data()
    print(ml_fixture.get_pca())
    captured = capsys.readouterr()
    assert 'Covariance matrix' in captured.out

# def test_association(ml_fixture, capsys):
#     ml_fixture.prepare_data()
#     print(ml_fixture.get_apriori())
#     captured = capsys.readouterr()
#     assert 'Covariance matrix' in captured.out






