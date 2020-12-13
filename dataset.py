import image_utils
from point import Point

import os
import csv
import json

import cv2
import numpy as np

greek_symbol_ids = ["81", "82", "87", "88", "89", "116", "117", "151", "153", "154", "155",
                        "157",
                        "158", "159", "160", "161", "162", "164," "165", "166", "169", "170",
                        "171",
                        "172", "173", "174", "176", "177", "178", "180"]


# https://arxiv.org/pdf/1701.08380.pdf
def read_csv(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        line_count = 0

        dataset = []
        columns = []

        for row in csv_reader:
            if line_count == 0:
                columns = row
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                obj = {}
                for i, col in enumerate(columns):
                    if i == 2:
                        data = json.loads(row[i])
                        total_points = []
                        for date in data:
                            for point in date:
                                point = Point(int(point["x"]), int(point["y"]))
                                total_points.append(point)
                        obj[col] = total_points
                    elif i == 0:
                        obj[col] = row[i]
                dataset.append(obj)
                line_count += 1
    return dataset


def generate_images_from_dataset(dataset_path, path_out):
    dataset = read_csv(dataset_path)

    count = 0
    for obj in dataset:
        if obj["symbol_id"] in greek_symbol_ids:
            image = image_utils.generate_images_from_points(obj["data"], -90, True)
            try:
                image = image_utils.resize_and_pad(image, 64)
            except AttributeError:
                print(f"Error on image {count}")
                continue
            image_utils.save_image(f'{path_out}{count}_{obj["symbol_id"]}.jpg', image)
            count += 1


def load_dataset(path_to_train_images, path_to_test_images):
    files_train = os.listdir(path_to_train_images)
    files_test = os.listdir(path_to_test_images)

    x_train = np.zeros((len(files_train), 64, 64))
    x_test = np.zeros((len(files_test), 64, 64))

    y_train = np.zeros((len(files_train),))
    y_test = np.zeros((len(files_test),))

    for i, file in enumerate(files_train):
        image = cv2.imread(path_to_train_images + file, cv2.IMREAD_GRAYSCALE)
        x_train[i] = image
        label = int(file.split(".")[0].split("_")[1])
        y_train[i] = label

    for i, file in enumerate(files_test):
        image = cv2.imread(path_to_test_images + file, cv2.IMREAD_GRAYSCALE)
        x_test[i] = image
        label = int(file.split(".")[0].split("_")[1])
        y_test[i] = label

    x_train = x_train.astype("int32")
    x_test = x_test.astype("int32")
    y_train = y_train.astype("int32")
    y_test = y_test.astype("int32")

    y_train = map_labels(y_train)
    y_test = map_labels(y_test)

    return (x_train, y_train), (x_test, y_test)


def map_labels(labels):
    labels = [greek_symbol_ids.index(str(x)) for x in labels]
    labels = np.array(labels)
    return labels