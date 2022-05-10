import cv2
import numpy as np


def get_mask_green(hsv_img):
    mask1 = cv2.inRange(hsv_img, np.array([37, 139, 126]), np.array([83, 255, 227]))
    mask = mask1
    return mask
