import numpy as np
import cv2


def add_border(image_path, output_path, low, high):
    top = np.random.randint(low, high)
    bottom = np.random.randint(low, high)
    left = np.random.randint(low, high)
    right = np.random.randint(low, high)

    image = cv2.imread(image_path)
    original_width, original_height = image.shape[1], image.shape[0]

    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_REPLICATE)

    image = cv2.resize(image, (original_width, original_height))
    cv2.imwrite(output_path, image)


add_border(r"C:\Users\Admin\PycharmProjects\Tracking_Object\dataset",
           r"C:\Users\Admin\PycharmProjects\Tracking_Object\data_augmentation", 50, 100)
