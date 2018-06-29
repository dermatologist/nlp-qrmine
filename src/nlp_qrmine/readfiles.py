import re
import sys


class ReadData(object):
    def __init__(self):
        self._content = ''
        self._documents = ''
        self.read_file()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def documents(self):
        return self._documents

    @documents.setter
    def documents(self, documents):
        self._documents = documents

    def read_file(self):
        with open(sys.argv[1], 'r') as f:
            self._content = f.read()
            self._documents = re.split('<break>', self._content)
        f.close()
