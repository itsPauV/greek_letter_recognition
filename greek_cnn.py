from dataset import load_dataset
from dataset import greek_symbol_ids

import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D

try:
    model = tf.keras.models.load_model("model.h5")
except OSError:
    (x_train, y_train), (x_test, y_test) = load_dataset("dataset/images_train/", "dataset/images_test/")

    # Reshape images -> color value in array -> x_train is array of 3D Arrays
    x_train = x_train.reshape(x_train.shape[0], 64, 64, 1)
    x_test = x_test.reshape(x_test.shape[0], 64, 64, 1)
    input_shape = (64, 64, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # Normalize color values
    x_train /= 255
    x_test /= 255

    # Model
    model = Sequential()
    model.add(Conv2D(128, kernel_size=(3, 3), input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.4))
    model.add(Dense(29, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=x_train, y=y_train, epochs=10)

    model.evaluate(x_test, y_test)

    model.save("model.h5")

    image_index = 1
    print(y_train[image_index])

    imgplot = plt.imshow(x_train[image_index])
    plt.show()
    pred = model.predict(x_train[image_index].reshape(1, 64, 64, 1))
    print(pred.argmax())
    print(greek_symbol_ids[y_train[image_index]])
    print(greek_symbol_ids[pred.argmax()])