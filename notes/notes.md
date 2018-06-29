# Notes

## Scaffolded with PyScaffold [Important](https://github.com/blue-yonder/pyscaffold)

## Setting up environment

* Install Anaconda / conda
* conda create --name spacy python=3
* source activate spacy
* pip install spacy
* pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-1.2.1/en_core_web_md-1.2.1.tar.gz
This installs the core model. Change version number if necessary.
* git clone https://beapen@bitbucket.org/beapen/nlp-qrmine.git

## Miscellaneous
* @property should come before @setter

## Starting a new python project with <template></template>
```
conda install sphinx

conda install setuptools

pip install pyscaffold

putup QRMine -l gpl3 -d "Qualitative Research Support Tools" -u http://canehealth.com --with-travis
```

## Versioning with Git

### Setup by PyScaffold

* [In code](https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script)
```python
import subprocess

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

```
* [In setup.py](https://logc.github.io/blog/2014/04/01/python-egg-tagged-with-git-commit-hash/)
```python
import shlex
from subprocess import check_output

GIT_HEAD_REV = check_output(shlex.split('git rev-parse --short HEAD')).strip()


setup(
    # ... other keys like project name, version, etc ...
    options = dict(egg_info = dict(tag_build = "dev_" + GIT_HEAD_REV)),
)
```