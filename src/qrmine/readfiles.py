import re
import requests
from pypdf import PdfReader


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

    def read_file(self, input):
        # if input is a file name
        if input.endswith(".txt"):
            with open(input, "r") as f:
                read_from_file = f.read()
                self._content = re.sub("<[^<]+?>", "", read_from_file)
                self._documents = re.split("<break>.*?</break>", read_from_file)
                # Delete the last blank record
                del self._documents[-1]
                pattern = r"<break>(.*?)</break>"
                self._titles = re.findall(pattern, read_from_file, flags=re.DOTALL)
        # if input is a folder name
        elif input.endswith("/"):
            import os

            for file_name in os.listdir(input):
                if file_name.endswith(".txt"):
                    with open(os.path.join(input, file_name), "r") as f:
                        read_from_file = f.read()
                        self._content += read_from_file
                        self._documents.append(read_from_file)
                        self.titles.append(file_name)
                if file_name.endswith(".pdf"):
                    with open(os.path.join(input, file_name), "rb") as f:
                        reader = PdfReader(f)
                        read_from_file = ""
                        for page in reader.pages:
                            read_from_file += page.extract_text()
                        self._content += read_from_file
                        self._documents.append(read_from_file)
                        self.titles.append(file_name)
        # if input is a url
        elif input.startswith("http://") or input.startswith("https://"):
            response = requests.get(input)
            if response.status_code == 200:
                read_from_file = response.text
                self._content = read_from_file
                self._documents.append(read_from_file)
                self.titles.append(input)
        else:
            raise ValueError("Input must be a file name, folder name or url.")

        """
        Combine duplicate topics using Dict
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
