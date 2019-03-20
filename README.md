# :flashlight: QRMine

QRMine is a suite of qualitative research (QR) support tools in Python using Natural Language Processing (NLP) and Machine Learning (ML). QRMine is still work in progress and is not ready for use.

## What it does

### NLP
* [x] Lists common categories for open coding.
* [x] Create a coding dictionary with categories, properties and dimensions.
* [x] Topic modelling.
* [x] Arrange docs according to topics.
* [x] Compare two documents/interviews.
* [x] Sentiment analysis
* [ ] Network analysis
* [ ] Co-citation finder

### ML
* [x] Accuracy of a neural network model trained using the data.
* [x] Confusion matrix from an support vector machine classifier
* [x] K nearest neighbours of a given record.
* [x] K-Means clustering
* [ ] Association rules.
* [ ] Principal Component Analysis (PCA)

## How to use

* Download/clone this repository
* pip install -r requirements.txt
* python qrmine.py ( --help to display all command line options)

### Command-line options

| Command | Alternate | Description |
| --- | --- | --- |
| --inp | -i | Input file in the text format with <break> Topic </break> |
| --out | -o | Output file name |
| --csv |   | csv file name |


## Input file format

### NLP
Individual documents or interview transcripts in a single text file separated by <break>Topic</break>. Example below

```
Text of the first interview
<break> First interview with student 1 </break>
Text of the second interview
<break> Second interview with tutor 1 </break>
```

Multiple files are suported, each having only one break tag at the bottom with the topic.
(The tag may be renamed in the future)

### ML

A single csv file with the following generic structure.

* Column 1 with identifier. If it is related to a text document as above, include the title.
* Last column has the dependent variable (DV). (NLP algorithms like the topic asignments may be able to create DV)
* All independent variables (numerical) in between.


## Author

Bell Eapen (McMaster U)

## Citation

Please cite QRMine in your publications if it helped your research. Here
is an example BibTeX entry:

```

@misc{eapenbr2016,
  title={QRMine -Qualitative Research Tools in Python.},
  author={Eapen, Bell Raj and contributors},
  year={2016},
  publisher={GitHub},
  journal = {GitHub repository},
  howpublished={\url{https://github.com/dermatologist/nlp-qrmine}}
}

```

Publication with the theoretical foundations of this tool is being worked on. QRMine is inspired by [this work](https://github.com/lknelson/computational-grounded-theory) and the associated [paper](https://journals.sagepub.com/doi/abs/10.1177/0049124117729703).
