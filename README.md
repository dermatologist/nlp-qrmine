# QRMine

[![QRMine](https://raw.github.com/dermatologist/nlp-qrmine/master/notes/QR.jpg)](http://canehealth.com)

QRMine is a suite of qualitative research (QR) support tools in Python
using NLP. Currently QRMine include:

  - gtdict : Generates a coding dictionary based on available data
    (Grounded Theory)
  - nnet : Evaluate the accuracy of an ANN with the given set of IV and
    one DV (Theory Building)
  - sentiment : Create the CNN model for sentiment analysis.
  - run\_sentiment : Use the CNN model created by sentiment module for
    prediction.

\* cocite: Find the cocitation frequency for biomedical literature using
NCBI's EUtils. And More to come. (work in progress)

## How to Install: 

checkout this repo and

```
python setup.py sdist

OR

python setup.py bdist

OR 

python setup.py bdist_wheel

```


## How to use:

[Read](https://stackoverflow.com/questions/6292652/what-is-the-difference-between-an-sdist-tar-gz-distribution-and-an-python-egg)

## Using Docker

TBD

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
