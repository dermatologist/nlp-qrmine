import re
import sys


class ReadData(object):
    def __init__(self):
        self._content = ''
        self._documents = ''
        self._titles = ''
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

    @property
    def titles(self):
        return self._titles

    @titles.setter
    def titles(self, titles):
        self._titles = titles

    def read_file(self):
        with open(sys.argv[1], 'r') as f:
            read_from_file = f.read()
            self._content = re.sub('<[^<]+?>', '', read_from_file)
            self._documents = re.split('<break>.*?</break>', read_from_file)
            pattern = r"<break>(.*?)</break>"
            self._titles = re.findall(pattern, read_from_file, flags=re.DOTALL)
        f.close()
