import cv2
import numpy as np
import keyboard
import time
from mylib import distance, calculate_angle
import random
import math


def set_color(rgb):
    img = np.full((480, 640, 3), 0, dtype=np.uint8)
    height = img.shape[0]
    width = img.shape[1]

    for i in range(height):
        for j in range(width):
            img[i][j][0] = rgb[2]

    for i in range(height):
        for j in range(width):
            img[i][j][1] = rgb[1]

    for i in range(height):
        for j in range(width):
            img[i][j][2] = rgb[0]
    return img


def update_des(sta, des):
    #list_rec = ((170, 400), (220, 400), (270, 400), (320, 400), (370, 400), (420, 400),
    #            (470, 400), (520, 400),
    #            (520, 350), (520, 300), (520, 250), (520, 200), (520, 150), (520, 100),
    #            (470, 100), (420, 100), (370, 100), (320, 100), (270, 100), (220, 100),
    #            (170, 100), (120, 100),
    #            (120, 150), (120, 200), (120, 250), (120, 300), (120, 350), (120, 400))
    list_rec = ((120, 400), (520, 400), (520, 100), (120, 100))
    if distance(sta, des) < 20:
        for i in range(len(list_rec)):
            if list_rec[i] == des:
                if i != len(list_rec)-1:
                    des = list_rec[i+1]
                    break
                else:
                    des = list_rec[0]
                    break
    return des


def update_sta(sta, ang, im):
    cv2.circle(im, sta, 5000, (0, 0, 0), -1)

    if keyboard.is_pressed('r'):
        ang -= 0.01
        if ang < 0:
            ang = ang + 2*math.pi

    if keyboard.is_pressed('e'):
        ang += 0.01
        if ang > 2*math.pi:
            ang = ang - 2*math.pi

    dire = (int(sta[0] + 30 * math.cos(ang)), int(sta[1] + 30 * math.sin(ang)))

    if keyboard.is_pressed('a'):
        my_state = list(sta)
        if my_state[0] > 0:
            my_state[0] += -1
        sta = tuple(my_state)

    if keyboard.is_pressed('d'):
        my_state = list(sta)
        if my_state[0] < img.shape[1]:
            my_state[0] += 1
        sta = tuple(my_state)

    if keyboard.is_pressed('w'):
        my_state = list(sta)
        if my_state[1] > 0:
            my_state[1] += -1
        sta = tuple(my_state)

    if keyboard.is_pressed('s'):
        my_state = list(sta)
        if my_state[1] < img.shape[0]:
            my_state[1] += 1

        sta = tuple(my_state)

    return sta, ang, dire


#Initialize parameters --------------------------------------------------------------------------------------------


state_vector = (math.pi/4, (random.randint(0, 479), random.randint(0, 479)))
angle = state_vector[0]
state = (random.randint(0, 479), random.randint(0, 479))
destination = (120, 400)
color = (0, 0, 0)
x, y, w, h = 120, 100, 400, 300
img = set_color(color)
direction = (int(state[0] + 30 * math.cos(angle)), int(state[1] + 30 * math.sin(angle)))


#Start the virtual robot ------------------------------------------------------------------------------------------

while True:
    cv2.imshow("Image", img)
    state, angle, direction = update_sta(state, angle, img)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.arrowedLine(img, state, destination, (0, 0, 255), 2)
    cv2.arrowedLine(img, state, direction, (0, 255, 255), 2)
    cv2.circle(img, state, 5, (255, 255, 255), -1)
    destination = update_des(state, destination)
    time.sleep(0.008)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
