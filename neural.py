import csv
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from sklearn import model_selection
import numpy
from random import shuffle

# seed
seed_ = 5
numpy.random.seed(seed_)


def ANN():
    dataset = numpy.loadtxt('train_data.csv', delimiter=',')
    Xtrain = dataset[:, :8]
    Ytrain = dataset[:, 8]
    model = Sequential()
    model.add(Dense(8, input_dim=8, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    model.add(Dense(8, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    model.add(Dense(4, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    model.add(Dense(1, activation='relu'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(Xtrain, Ytrain, epochs=5, batch_size=16, verbose=1)


# print(model.predict(Xtrain))
# print(Ytrain)

if __name__ == '__main__':
    ANN()
