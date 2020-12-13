from operator import attrgetter

import cv2
import numpy as np
from scipy import ndimage


def save_image(path, image):
    cv2.imwrite(path, image)


def generate_images_from_points(points_data, rotation=0, flip=False):
    # 1000 x 1000 some images exceed 1000s -> 2000 may be to big?
    min_x = min(points_data, key=attrgetter("x")).x
    max_x = max(points_data, key=attrgetter("x")).x
    min_y = min(points_data, key=attrgetter("y")).y
    max_y = max(points_data, key=attrgetter("y")).y

    width = max_x - min_x
    height = max_y - min_y

    image = np.full((width, height), 0)
    for point in points_data:
        try:
            image[point.x - min_x][point.y - min_y] = 255
        except IndexError:
            continue
    image = ndimage.rotate(image, rotation)
    if flip:
        image = cv2.flip(image, 1)
    return image


def resize(image, new_height, new_width):
    width = image.shape[1]
    height = image.shape[0]

    image = image.reshape((height, width)).astype("float32")

    dim = None
    # If height > width of image
    if height > width:
        # dim = (int(width*(new_height/height)), new_height)
        dim = (new_height, int(width*(new_height/height)))
    else:
        # dim = (new_width, int(height * (new_width / width)))
        dim = (int(height*(new_width/width)), new_width)
    image = cv2.resize(image, dim)
    image[image > 1] = 255

    return image


def resize_and_pad(image, a):
    image = resize(image, a, a)
    width = image.shape[1]
    height = image.shape[0]

    padded_image = np.full((a, a), 0)
    # // -> floor division -> result roundend down
    offset_x = (a - width) // 2
    offset_y = (a - height) // 2

    padded_image[offset_y:offset_y+height, offset_x:offset_x+width] = image
    padded_image = padded_image.reshape((padded_image.shape[1], padded_image.shape[0])).astype("int32")

    return padded_image


