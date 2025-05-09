# 🔍 QRMine
*/ˈkärmīn/*

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)[![PyPI download total](https://img.shields.io/pypi/dm/qrmine.svg)](https://pypi.python.org/pypi/qrmine/)
![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/qrmine)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/dermatologist/nlp-qrmine)
[![Documentation](https://badgen.net/badge/icon/documentation?icon=libraries&label)](https://dermatologist.github.io/nlp-qrmine/)

Qualitative research involves the collection and analysis of textual data, such as interview transcripts, open-ended survey responses, and field notes. It is often used in social sciences, humanities, and health research to explore complex phenomena and understand human experiences. In addition to textual data, qualitative researchers may also collect quantitative data, such as survey responses or demographic information, to complement their qualitative findings.

Qualitative research is often characterized by its inductive approach, where researchers aim to generate theories or concepts from the data rather than testing pre-existing hypotheses. This process is known as Grounded Theory, which emphasizes the importance of data-driven analysis and theory development.

QRMine is a Python package for qualitative research and triangulation of textual and numeric data in Grounded Theory. It provides tools for Natural Language Processing (NLP) and Machine Learning (ML) to analyze qualitative data, such as interview transcripts, and quantitative data, such as survey responses for theorizing.

Version 4.0 is a major update with new features and bug fixes. It moves some of the ML dependencies to an optional install. Version 4.0 is a prelude to version 5.0 that will introduce large language models (LLMs) for qualitative research.

## ✨ Features

### 🔧 NLP
* Lists common categories for open coding.
* Create a coding dictionary with categories, properties and dimensions.
* Topic modelling.
* Arrange docs according to topics.
* Compare two documents/interviews.
* Select documents/interviews by sentiment, category or title for further analysis.
* Sentiment analysis
* Clusters documents and creates visualizations.
* Generate (non LLM) summary of documents/interviews.


### 🧠 ML
* Accuracy of a neural network model trained using the data
* Confusion matrix from an support vector machine classifier
* K nearest neighbours of a given record
* K-Means clustering
* Principal Component Analysis (PCA)
* Association rules

## 🛠️ How to install

* Requires Python 3.11
```text
pip install qrmine
python -m spacy download en_core_web_sm

```

* For ML functions (neural networks & SVM), install the optional packages
```text
pip install qrmine[ml]
```

### Mac users
* Mac users, please install *libomp* for XGBoost
```
brew install libomp
```

## 🚀 How to Use

* Input files are transcripts as txt/pdf files and (optionally) a single csv file with numeric data. The output txt file can be specified. All transcripts can be in a single file separated by a break tag as described below.

* The coding dictionary, topics and topic assignments can be created from the  entire corpus (all documents) using the respective command line options.

* Categories (concepts), summary and sentiment can be viewed for entire corpus or specific titles (documents) specified using the --titles switch. Sentence level sentiment output is possible with the --sentence flag.

* You can filter documents based on sentiment, titles or categories and do further analysis, using --filters or -f

* Many of the ML functions like neural network takes a second argument (-n) . In nnet -n signifies the number of epochs, number of clusters in kmeans, number of factors in pca, and number of neighbours in KNN. KNN also takes the --rec or -r argument to specify the record.

* Variables from csv can be selected using --titles (defaults to all). The first variable will be ignored (index) and the last will be the DV (dependant variable).


### Command-line options

```text
qrmine --help

```

| Command | Alternate | Description |
| --- | --- | --- |
| --inp | -i | Input file in the text format with <break> Topic </break> |
| --out | -o | Output file name |
| --csv |   | csv file name |
| --num | -n  | N (clusters/epochs etc depending on context) |
| --rec | -r  | Record (based on context) |
| --titles | -t | Document(s) title(s) to analyze/compare |
| --codedict |   | Generate coding dictionary |
| --topics |   | Generate topic model |
| --assign |   | Assign documents to topics |
| --cat |   | List categories of entire corpus or individual docs |
| --summary |   | Generate summary for entire corpus or individual docs |
| --sentiment |   | Generate sentiment score for entire corpus or individual docs |
| --nlp |   | Generate all NLP reports |
| --sentence |   | Generate sentence level scores when applicable |
| --nnet |   | Display accuracy of a neural network model -n epochs(3)|
| --svm |   | Display confusion matrix from an svm classifier |
| --knn |   | Display nearest neighbours -n neighbours (3)|
| --kmeans |   | Display KMeans clusters -n clusters (3)|
| --cart |   | Display Association Rules |
| --pca |   | Display PCA -n factors (3)|


## Use it in your code
```python
from qrmine import Content
from qrmine import Network
from qrmine import Qrmine
from qrmine import ReadData
from qrmine import Sentiment
from qrmine import MLQRMine
from qrmine import ClusterDocs
from qrmine import QRVisualize

```
* *More instructions and a jupyter notebook available [here.](https://nuchange.ca/2017/09/grounded-theory-qualitative-research-python.html)*

## Input file format

### NLP
Individual documents or interview transcripts in a single text file separated by <break>Topic</break>. Example below

```
Transcript of the first interview with John.
Any number of lines
<break>First_Interview_John</break>

Text of the second interview with Jane.
More text.
<break>Second_Interview_Jane</break>

....
```

Multiple files are suported, each having only one break tag at the bottom with the topic.
(The tag may be renamed in the future)

### ML

A single csv file with the following generic structure.

* Column 1 with identifier. If it is related to a text document as above, include the title.
* Last column has the dependent variable (DV). (NLP algorithms like the topic asignments may provide the DV)
* All independent variables (numerical) in between.

```
index, obesity, bmi, exercise, income, bp, fbs, has_diabetes
1, 0, 29, 1, 12, 120, 89, 1
2, 1, 32, 0, 9, 140, 92, 0
......

```

## Author

* [Bell Eapen](https://nuchange.ca) ([UIS](https://www.uis.edu/directory/bell-punneliparambil-eapen)) |  [Contact](https://nuchange.ca/contact) | [![Twitter Follow](https://img.shields.io/twitter/follow/beapen?style=social)](https://twitter.com/beapen)


## Citation

Please cite QRMine in your publications if it helped your research.
Citation information will be available soon.

## Give us a star ⭐️
If you find this project useful, give us a star. It helps others discover the project.


