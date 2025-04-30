import pytest
import pandas as pd
from src.qrmine.visualize import QRVisualize

@pytest.fixture
def v():
    from pkg_resources import resource_filename
    file_path = resource_filename("src.qrmine.resources", "df_dominant_topic.csv")
    data = pd.read_csv(file_path)
    _v = QRVisualize(data)
    return _v

def test_frequency_distribution_of_words(v, capsys):
    v.plot_frequency_distribution_of_words(v.data, folder_path='/tmp/frequency_distribution.png')
    captured = capsys.readouterr()
    print(captured.out)

