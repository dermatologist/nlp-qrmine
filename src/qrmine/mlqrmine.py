import numpy
from imblearn.over_sampling import RandomOverSampler
from pandas import read_csv
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neighbors import KDTree
from random import randint

from xgboost import XGBClassifier
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

import torch.nn as nn
import torch.optim as optim
import torch
from torch.utils.data import DataLoader, TensorDataset
class NeuralNet(nn.Module):
    def __init__(self, input_dim):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 12)
        self.fc2 = nn.Linear(12, 8)
        self.fc3 = nn.Linear(8, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x


class MLQRMine(object):

    def __init__(self):
        self._seed = randint(1, 9)
        self._csvfile = ""
        self._titles = None
        self._model = None
        self._dataset = None
        self._X = None
        self._y = None
        self._X_original = None
        self._y_original = None
        self._dataset_original = None
        self._sc = StandardScaler()
        self._vnum = 0  # Number of variables
        self._classifier = XGBClassifier()
        self._epochs = 10
        self._samplesize = 0
        self._clusters = None

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
    def model(self):
        return self._model

    @property
    def epochs(self):
        return self._epochs

    @property
    def X(self):
        return self._X

    @property
    def y(self):
        return self._y

    @property
    def titles(self):
        return self._titles

    @property
    def head(self):
        return self._dataset.head

    # Getters should be before setters*
    @epochs.setter
    def epochs(self, epochs):
        self._epochs = epochs

    @seed.setter
    def seed(self, seed):
        self._seed = seed

    @csvfile.setter
    def csvfile(self, csvfile):
        self._csvfile = csvfile

    @titles.setter
    def titles(self, titles):
        self._titles = titles

    # Functions
    def read_csv(self):
        if self._titles is not None:
            self._dataset = read_csv(self._csvfile, usecols=self._titles)
        else:
            self._dataset = read_csv(self._csvfile)

    def mark_missing(self):
        self._dataset_original = self._dataset
        self._dataset = self._dataset.replace('', numpy.nan)
        self._dataset.dropna(inplace=True)

    def restore_mark_missing(self):
        self._dataset = self._dataset_original

    def get_shape(self):
        return self._dataset.shape

    """
    The actual number of IVs is vnum -2 as first is the title and the last is the DV
    To seperate DV, use vnum -1 to indicate last column
    More details on np array splicing here:
    https://stackoverflow.com/questions/34007632/how-to-remove-a-column-in-a-numpy-array/34008274
    """

    def read_xy(self):
        (self._samplesize, vnum) = self._dataset.shape
        # Last column in the csv should be the DV and first one is title (So get the number of variables)
        self._vnum = vnum - 2
        # splice into IVs and DV
        values = self._dataset.values
        # self._X = values[:, 0:self._vnum]
        # First column ignored - (To be used for title)
        self._X = values[:, 1:vnum - 1]
        self._y = values[:, vnum - 1]

    def oversample(self):
        self._X_original = self._X
        self._y_original = self._y
        ros = RandomOverSampler(random_state=0)
        X, y = ros.fit_resample(self._X, self._y)
        self._X = X
        self._y = y

    def restore_oversample(self):
        self._X = self._X_original
        self._y = self._y_original

    def prepare_data(self, oversample=False):
        self.read_csv()
        self.mark_missing()
        self.read_xy()
        if oversample:
            self.oversample()

    def get_nnet_predictions(self):

        self._model = NeuralNet(self._vnum)
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self._model.parameters(), lr=0.001)

        # Convert data to PyTorch tensors
        X_tensor = torch.tensor(self._X, dtype=torch.float32)
        y_tensor = torch.tensor(self._y, dtype=torch.float32).view(-1, 1)

        # Create a dataset and data loader
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=10, shuffle=True)

        # Train the model
        for epoch in range(self._epochs):
            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                outputs = self._model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()

        # Calculate predictions
        with torch.no_grad():
            predictions = self._model(torch.tensor(self._X_original, dtype=torch.float32))
            rounded = [round(x.item()) for x in predictions]
        # print("Predictions: ", rounded)
        # Calculate accuracy
        correct = sum([1 for i in range(len(rounded)) if rounded[i] == self._y_original[i]])
        total = len(rounded)
        accuracy = correct / total
        print(f'Accuracy: {accuracy * 100:.2f}%')
        return rounded

    def get_nnet_scores(self):
        # evalute the pytorch model
        self._model.eval()
        X_tensor = torch.tensor(self._X, dtype=torch.float32)
        y_tensor = torch.tensor(self._y, dtype=torch.float32).view(-1, 1)
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=10, shuffle=True)
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_X, batch_y in dataloader:
                outputs = self._model(batch_X)
                predicted = (outputs > 0.5).float()
                total += batch_y.size(0)
                correct += (predicted == batch_y).sum().item()
        accuracy = correct / total
        print(f'Accuracy: {accuracy * 100:.2f}%')

    def svm_confusion_matrix(self):
        """Generate confusion matrix for SVM

        Returns:
            [list] -- [description]
        """
        X_train, X_test, y_train, y_test = train_test_split(self._X, self._y, test_size=0.25, random_state=0)
        # Issue #22
        y_test = y_test.astype('int')
        y_train = y_train.astype('int')
        X_train = self._sc.fit_transform(X_train)
        X_test = self._sc.transform(X_test)
        classifier = SVC(kernel='linear', random_state=0)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        # Issue #22
        y_pred = y_pred.astype('int')
        return confusion_matrix(y_test, y_pred)

    # https://stackoverflow.com/questions/45419203/python-numpy-extracting-a-row-from-an-array
    def knn_search(self, n=3, r=3):
        kdt = KDTree(self._X, leaf_size=2, metric='euclidean')
        dist, ind = kdt.query(self._X[r - 1:r, :], k=n)
        return ind

    def get_kmeans(self, c=5):
        kmeans = KMeans(n_clusters=c, init='k-means++', random_state=42)
        y_kmeans = kmeans.fit_predict(self._X)
        self._clusters = y_kmeans
        self.get_centroids(c)
        return y_kmeans

    def get_centroids(self, c=1):
        for x in range(0, c):
            print("Cluster: ", x)
            ct = 0
            cluster_list = []
            for cluster in self._clusters:
                if cluster == x:
                    cluster_list.append(ct)
                ct += 1
            print("Cluster Length: ", len(cluster_list))
            print("Cluster Members")
            print(self._dataset.iloc[cluster_list, :])
            print("Mean")
            print(self._dataset.iloc[cluster_list, :].mean(axis=0))

    """
    TODO: This is not working yet.
    use the ColumnTransformer instead of categorical_features
    """

    def encode_categorical(self):
        # labelencoder_X_1 = LabelEncoder()
        # self._X[:, 1] = labelencoder_X_1.fit_transform(self._X[:, 1])
        # labelencoder_X_2 = LabelEncoder()
        # self._X[:, 2] = labelencoder_X_2.fit_transform(self._X[:, 2])
        onehotencoder = OneHotEncoder(categorical_features=[1])
        X = onehotencoder.fit_transform(self._X).toarray()
        X = X[:, 1:]
        print(X)
        return X

    def get_association(self):
        X_train, X_test, y_train, y_test = train_test_split(self._X, self._y, test_size=0.25, random_state=0)
        self._classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = self._classifier.predict(X_test)
        return confusion_matrix(y_test, y_pred)

    def get_apriori(self):
        frequent_itemsets = apriori(self.encode_categorical(), min_support=0.07, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        return rules

    def get_pca(self, n=3):
        # https://plot.ly/~notebook_demo/264/about-the-author-some-of-sebastian-rasc/#/
        X_std = StandardScaler().fit_transform(self._X)
        (recs, factors) = X_std.shape
        print('Covariance matrix: \n%s' % numpy.cov(X_std.T))

        cov_mat = numpy.cov(X_std.T)

        eig_vals, eig_vecs = numpy.linalg.eig(cov_mat)

        print('Eigenvectors \n%s' % eig_vecs)
        print('\nEigenvalues \n%s' % eig_vals)

        # Make a list of (eigenvalue, eigenvector) tuples
        eig_pairs = [(numpy.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]

        # Sort the (eigenvalue, eigenvector) tuples from high to low
        eig_pairs.sort()
        eig_pairs.reverse()

        # Visually confirm that the list is correctly sorted by decreasing eigenvalues
        print('Eigenvalues in descending order:')
        for i in eig_pairs:
            print(i[0])

        # variance explained
        tot = sum(eig_vals)
        var_exp = [(i / tot) * 100 for i in sorted(eig_vals, reverse=True)]
        cum_var_exp = numpy.cumsum(var_exp)
        print("Variance explained: ", var_exp)
        print("Cumulative: ", cum_var_exp)

        if len(eig_vals) < n:
            n = len(eig_vals)

        # Adjust according to number of features chosen (default n=2)
        matrix_w = numpy.hstack((eig_pairs[0][1].reshape(factors, 1),
                                 eig_pairs[1][1].reshape(factors, 1)))

        if n == 3:
            matrix_w = numpy.hstack((eig_pairs[0][1].reshape(factors, 1),
                                     eig_pairs[1][1].reshape(factors, 1),
                                     eig_pairs[2][1].reshape(factors, 1)))

        if n == 4:
            matrix_w = numpy.hstack((eig_pairs[0][1].reshape(factors, 1),
                                     eig_pairs[1][1].reshape(factors, 1),
                                     eig_pairs[2][1].reshape(factors, 1),
                                     eig_pairs[3][1].reshape(factors, 1)))
        if n == 5:
            matrix_w = numpy.hstack((eig_pairs[0][1].reshape(factors, 1),
                                     eig_pairs[1][1].reshape(factors, 1),
                                     eig_pairs[2][1].reshape(factors, 1),
                                     eig_pairs[3][1].reshape(factors, 1),
                                     eig_pairs[4][1].reshape(factors, 1)))

        print('Matrix W:\n', matrix_w)
