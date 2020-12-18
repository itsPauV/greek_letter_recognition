import csv
import cv2
import numpy as np
import random

greek_symbol_ids = ["81", "82", "87", "89", "116", "117", "151", "153", "154", "155",
                    "157", "158", "159", "160", "161", "162", "164," "165", "166", "169", "170",
                    "171", "172", "173", "174", "176", "177", "178", "180"]


def read_csv(filepath):
    with open(filepath) as fp:
        csv_reader = csv.reader(fp, delimiter=",")

        base_path = "/".join(filepath.split("/")[:-1])
        paths = []

        for row in csv_reader:
            obj = {}
            if row[1] in greek_symbol_ids:
                obj["path"] = base_path + "/" + row[0]
                obj["symbol"] = row[1]
                paths.append(obj)
    fp.close()
    return paths


def load_dataset(filepath):
    paths = read_csv(filepath)

    x = np.zeros((len(paths), 32, 32))
    y = np.zeros((len(paths),))

    for i, obj in enumerate(paths):
        image = cv2.imread(obj["path"], cv2.IMREAD_GRAYSCALE)
        x[i] = image
        y[i] = greek_symbol_ids.index(obj["symbol"])

    train_size = int(len(paths) * 0.7)

    zipped = list(zip(x, y))
    random.shuffle(zipped)
    x, y = zip(*zipped)

    x_train = np.array(x[:train_size])
    y_train = np.array(y[:train_size])
    x_test = np.array(x[train_size:])
    y_test = np.array(y[train_size:])

    return (x_train, y_train), (x_test, y_test)


def get_symbol_from_index(index, symbols_path):
    with open(symbols_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        symbol_id = greek_symbol_ids[index]
        for row in csv_reader:
            if row[0] == str(symbol_id):
                return row[1]
    csv_file.close()
    return None
