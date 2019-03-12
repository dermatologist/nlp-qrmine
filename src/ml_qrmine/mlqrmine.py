# This is for oversampling
from pandas import read_csv


class MLQRMine(object):

    def __init__(self):
        self._seed = 7
        self._csvfile = ""
        self._dataset = None

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed

    @property
    def csvfile(self):
        return self._csvfile

    @csvfile.setter
    def csvfile(self, csvfile):
        self._csvfile = csvfile

    def read_csv(self):
        self._dataset = read_csv(self._csvfile, header=1)
