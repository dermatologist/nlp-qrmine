from pandas import read_csv
import numpy
from imblearn.over_sampling import RandomOverSampler
from keras.layers import Dense
from keras.models import Sequential

class MLQRMine(object):

    def __init__(self):
        self._seed = 7
        self._csvfile = ""
        self._dataset = None
        self._X = None
        self._y = None
        self._X_original = None
        self._y_original = None
        self._dataset_original = None

    @property
    def seed(self):
        return self._seed

    @property
    def csvfile(self):
        return self._csvfile

    @property
    def dataset(self):
        return self._dataset

    @property
    def X(self):
        return self._X

    @property
    def y(self):
        return self._y

    # Getters should be before setters*
    @seed.setter
    def seed(self, seed):
        self._seed = seed

    @csvfile.setter
    def csvfile(self, csvfile):
        self._csvfile = csvfile

    # Functions
    def read_csv(self):
        self._dataset = read_csv(self._csvfile, header=1)

    def mark_missing(self):
        self._dataset_original = self._dataset
        self._dataset = self._dataset.replace('', numpy.NaN)

    def restore_mark_missing(self):
        self._dataset = self._dataset_original

    def get_shape(self):
        return self._dataset.shape

    def read_xy(self):
        read_csv()
        (sample, vnum) = self._dataset.shape
        # Last column in the csv should be the DV (So get the number of variables)
        vnum = vnum - 1
        # splice into IVs and DV
        values = self._dataset.values
        self._X = values[:, 0:vnum]
        self._y = values[:, vnum]

    def oversample(self):
        self._X_original = self._X
        self._y_original = self._y
        ros = RandomOverSampler(random_state=0)
        X, y = ros.fit_sample(X, y)

    def restore_oversample(self):
        self._X = self._X_original
        self._y = self._y_original
