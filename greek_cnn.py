from dataset_hasy import load_dataset, get_symbol_from_index

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D


def train(model_name):
    (x_train, y_train), (x_test, y_test) = load_dataset("dataset/HASYv2/hasy-data-labels.csv")


    # Reshape images -> color value in array -> x_train is array of 3D Arrays
    x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
    input_shape = (x_train.shape[1], x_train.shape[2], 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # Normalize color values
    x_train /= 255
    x_test /= 255

    # Model
    model = Sequential()
    model.add(Conv2D(128, kernel_size=(3, 3), input_shape=input_shape))
    model.add(Conv2D(32, kernel_size=(3, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.4))
    model.add(Dense(29, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=x_train, y=y_train, epochs=20)

    model.evaluate(x_test, y_test)
    model.save(model_name)


def predict(pixels):
    try:
        model = tf.keras.models.load_model("model.h5")
    except OSError:
        train("model.h5")
        predict(pixels)
    pixels = np.array(pixels)
    pixels = pixels.reshape(pixels.shape[0], pixels.shape[1], 1)
    pixels = pixels.astype('float32')

    pixels /= 255
    pred = model.predict(pixels.reshape(1, pixels.shape[0], pixels.shape[1], 1))[0]

    symbol = get_symbol_from_index(pred.argmax())

    return symbol


train("hasy.h5")