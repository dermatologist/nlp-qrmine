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

@pytest.fixture
def topics():
    return [
        (
            0,
            [
                (".", 0.095292516),
                (",", 0.053392828),
                ("category", 0.032462463),
                ("coding", 0.032456465),
                ("open", 0.032437164),
                ("QRMine", 0.03243305),
                ("datum", 0.021980358),
                ("researcher", 0.021978099),
                ("theory", 0.011536299),
                ("GT", 0.011533132),
            ],
        ),
        (
            1,
            [
                (".", 0.007783216),
                (",", 0.007773952),
                ("open", 0.007728422),
                ("researcher", 0.0077227736),
                ("coding", 0.007722049),
                ("category", 0.007721938),
                ("datum", 0.007717547),
                ("QRMine", 0.007716193),
                ("dissect", 0.0077070068),
                ("support", 0.0077060354),
            ],
        ),
        (
            2,
            [
                (",", 0.05126711),
                (".", 0.05125151),
                ("theory", 0.038604487),
                ("category", 0.03227912),
                ("GT", 0.032278605),
                ("\n", 0.029119665),
                ("comparison", 0.025947908),
                ("coding", 0.025941858),
                ("incident", 0.019622542),
                (")", 0.019619444),
            ],
        ),
        (
            3,
            [
                (".", 0.007849805),
                (",", 0.007837688),
                ("theory", 0.00781459),
                ("coding", 0.0078089647),
                ("category", 0.0077514737),
                ("GT", 0.0077493717),
                ("datum", 0.007742789),
                ("open", 0.0077355755),
                ("\n", 0.0077245855),
                ("researcher", 0.0077191954),
            ],
        ),
        (
            4,
            [
                (",", 0.007834569),
                (".", 0.007812336),
                ("coding", 0.0077863215),
                ("category", 0.007759207),
                ("theory", 0.0077459146),
                ("GT", 0.0077370973),
                ("code", 0.0077265715),
                ("datum", 0.007720947),
                ("open", 0.007720898),
                ("comparison", 0.007720567),
            ],
        ),
    ]

def test_frequency_distribution_of_words(v, capsys):
    v.plot_frequency_distribution_of_words(v.data, folder_path='/tmp/frequency_distribution.png')
    captured = capsys.readouterr()
    print(captured.out)

def test_distribution_by_topic(v, capsys):
    v.plot_distribution_by_topic(v.data, folder_path='/tmp/distribution_by_topic.png')
    captured = capsys.readouterr()
    print(captured.out)

def test_plot_wordcloud(v, topics, capsys):
    v.plot_wordcloud(topics, folder_path='/tmp/wordcloud.png')
    captured = capsys.readouterr()
    print(captured.out)
