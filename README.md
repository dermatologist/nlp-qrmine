# :flashlight: QRMine

QRMine is a suite of qualitative research (QR) support tools in Python using NLP. QRMine is still work in progress and is not ready for use.

## What it does

* Finds common categories for open coding.
* Create a coding dictionary with categories, properties and dimensions.
* Find topics.
* Arrange docs according to topics.
* Compare two documents/interviews.
* Sentiment analysis
* Co-citation finder

## How to Use

* Download/clone this repository
* pip install -r requirements.txt
* python qrmine.py ( --help to display all command line options)

## Input file format
Individual documents or interview transcripts in a single text file separated by <break>Topic</break>. Example below

```
Text of the first interview
<break> First interview with student 1 </break>
Text of the second interview
<break> Second interview with tutor 1 </break>
```

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
