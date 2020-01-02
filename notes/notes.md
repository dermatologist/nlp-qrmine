# Notes

## Scaffolded with PyScaffold [Important](https://github.com/blue-yonder/pyscaffold)


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

## Command line

* https://pymbook.readthedocs.io/en/latest/click.html


## Getters and setters

class testDec(object):
* And one more thing that is not completely easy to spot at first, is the order: The getter must be defined first.