import re


class ReadData(object):
    def __init__(self):
        self._content = None
        self._documents = None
        self._titles = None

    # Getter must be defined first
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

    def read_file(self, file_names):
        if isinstance(file_names, (list,)):
            for file_name in file_names:
                with open(file_name, 'r') as f:
                    read_from_file = f.read()
                    self._content = re.sub('<[^<]+?>', '', read_from_file)
                    self._documents = re.split('<break>.*?</break>', read_from_file)
                    # Delete the last blank record
                    del self._documents[-1]
                    pattern = r"<break>(.*?)</break>"
                    self._titles = re.findall(pattern, read_from_file, flags=re.DOTALL)
                f.close()
        else:
            with open(file_names, 'r') as f:
                read_from_file = f.read()
                self._content = re.sub('<[^<]+?>', '', read_from_file)
                self._documents = re.split('<break>.*?</break>', read_from_file)
                # Delete the last blank record
                del self._documents[-1]
                pattern = r"<break>(.*?)</break>"
                self._titles = re.findall(pattern, read_from_file, flags=re.DOTALL)
            f.close()
