import re


class ReadData(object):
    def __init__(self):
        self._content = ""
        self._documents = []
        self._titles = []

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

    def append(self, title, document):
        self._titles.append(title)
        self._documents.append(document)
        self._content += document

    def read_file(self, file_names):
        if len(file_names) > 1:
            for file_name in file_names:
                with open(file_name, 'r') as f:
                    read_from_file = f.read()
                    self._content = re.sub('<[^<]+?>', '', read_from_file)
                    self._documents = re.split('<break>.*?</break>', read_from_file)
                    # Delete the last blank record
                    del self._documents[-1]
                    pattern = r"<break>(.*?)</break>"
                    _title = re.findall(pattern, read_from_file, flags=re.DOTALL)[0]
                    self._titles.append(_title)
                f.close()
        else:
            file_name = file_names[0]
            with open(file_name, 'r') as f:
                read_from_file = f.read()
                self._content = re.sub('<[^<]+?>', '', read_from_file)
                self._documents = re.split('<break>.*?</break>', read_from_file)
                # Delete the last blank record
                del self._documents[-1]
                pattern = r"<break>(.*?)</break>"
                self._titles = re.findall(pattern, read_from_file, flags=re.DOTALL)

                """
                Combine duplicate topics using Dict
                Currently supported only for single file.
                """

                doc_dict = {}
                ct3 = 0
                for t in self._titles:
                    doc = doc_dict.get(t)
                    if doc:
                        doc_dict[t] = doc + self._documents[ct3]
                    else:
                        doc_dict[t] = self._documents[ct3]
                    ct3 += 1
                self._titles.clear()
                self._documents.clear()
                for t in doc_dict.keys():
                    self._documents.append(doc_dict.get(t))
                    self._titles.append(t)

                f.close()
