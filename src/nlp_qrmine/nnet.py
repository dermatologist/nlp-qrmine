# Import Keras Library
import sys

import numpy
# This is for oversampling
from imblearn.over_sampling import RandomOverSampler
from keras.layers import Dense
from keras.models import Sequential
from pandas import read_csv

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# import dataset from the first argument in the commandline
dataset = read_csv(sys.argv[1], header=1)

# mark missing as NaN
dataset = dataset.replace('', numpy.NaN)

# Summarize the number of rows and columns in the dataset before listwise drop
print(dataset.shape)

# Drop missing listwise
dataset.dropna(inplace=True)

# summarize the number of rows and columns in the dataset after listwise drop
(sample, vnum) = dataset.shape
print(sample, vnum)

# Get the number of variables
vnum = vnum - 1

# splice into IVs and DV
values = dataset.values
X = values[:, 0:vnum]
y = values[:, vnum]

# Oversampling
ros = RandomOverSampler(random_state=0)
X_R, y_R = ros.fit_sample(X, y)

# create model
model = Sequential()
model.add(Dense(12, input_dim=vnum, kernel_initializer='uniform', activation='relu'))
model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X_R, y_R, epochs=150, batch_size=10, verbose=2)

# calculate predictions
predictions = model.predict(X)
# round predictions
rounded = [round(x[0]) for x in predictions]
print("\n Model")
print("\n")
print(rounded)
print("\n --------------------------------------------------")

# evaluate the model
scores = model.evaluate(X_R, y_R)
print("\n")
print("\n Accuracy of the model")
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
print("\n --------------------------------------------------")
