import numpy as np
import cv2
import imutils
import math
import urllib.request
import threading

root_url = "http://192.168.1.10"


# ESP's url, ex: http://192.168.102 (Esp prints it to serial console when connected to wi-fi)


def dis(p, y):
    if y == 1:
        d = np.abs(p[1] - 100)
    elif y == 2:
        d = np.abs(p[1] - 400)
    elif y == 3:
        d = np.abs(p[0] - 120)
    else:
        d = np.abs(p[0] - 520)
    return int(d)


def distance(p1, p2):
    return math.sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))


def calculate_angle(pt1, pt2):
    if pt2[0] - pt1[0] > 0:
        if pt2[1] > pt1[1]:
            angle = math.atan((pt2[1] - pt1[1]) / (pt2[0] - pt1[0]))
        else:
            angle = 2 * math.pi - math.atan((pt1[1] - pt2[1]) / (pt2[0] - pt1[0]))
    elif pt2[0] - pt1[0] < 0:
        angle = math.pi - math.atan((pt2[1] - pt1[1]) / (pt1[0] - pt2[0]))
    else:
        if pt2[1] > pt1[1]:
            angle = math.pi / 2
        else:
            angle = math.pi * (3 / 2)
    return angle * 180 / math.pi


def new_point(trajectory, p):
    if trajectory == "Rectangle":
        d = []
        case = 0

        for i in range(4):
            d.append(dis(p, i + 1))
        w = 0
        for i in range(len(d)):
            if min(d) == d[i]:
                case = i + 1
                w = min(d)
        if case == 1:
            if w != 0:
                if p[0] < 100:
                    des_p = (120, 100)
                elif p[0] > 500:
                    des_p = (520, 100)
                else:
                    des_p = (p[0], 100)
            else:
                des_p = (120, 100)
        elif case == 2:
            if w != 0:
                if p[0] < 120:
                    des_p = (120, 400)
                elif p[0] > 520:
                    des_p = (520, 400)
                else:
                    des_p = (p[0], 400)
            else:
                des_p = (520, 400)
        elif case == 3:
            if w != 0:
                if p[1] < 100:
                    des_p = (120, 100)
                elif p[1] > 400:
                    des_p = (120, 400)
                else:
                    des_p = (120, p[1])
            else:
                if p[1] == 400:
                    des_p = (520, 400)
                else:
                    des_p = (120, 400)
        else:
            if w != 0:
                if p[1] < 100:
                    des_p = (520, 100)
                elif p[1] > 400:
                    des_p = (520, 400)
                else:
                    des_p = (520, p[1])
            else:
                if p[1] == 400:
                    des_p = (520, 100)
                elif p[1] == 100:
                    des_p = (120, 100)
                else:
                    des_p = (520, 100)

        return des_p

    if trajectory == "Circle":
        return None


def sendrequest(url):
    urllib.request.urlopen(url)


def get_mask_green(hsv_img):
    masks = []
    '''
    masks.append(cv2.inRange(hsv_img, np.array([52, 83, 172]), np.array([78, 122, 211])))
    masks.append(cv2.inRange(hsv_img, np.array([40, 84, 82]), np.array([82, 150, 205])))
    masks.append(cv2.inRange(hsv_img, np.array([49, 111, 138]), np.array([66, 171, 178])))
    masks.append(cv2.inRange(hsv_img, np.array([49, 102, 121]), np.array([66, 140, 196])))
    masks.append(cv2.inRange(hsv_img, np.array([55, 96, 143]), np.array([76, 138, 181])))
    masks.append(cv2.inRange(hsv_img, np.array([10, 91, 153]), np.array([83, 133, 194])))
    '''
    masks.append(cv2.inRange(hsv_img, np.array([79, 147, 156]), np.array([95, 206, 209])))
    masks.append(cv2.inRange(hsv_img, np.array([79, 132, 130]), np.array([91, 193, 191])))

    mask_green = masks[0]
    for mask in masks:
        mask_green += mask
    return mask_green


def get_mask_blue(hsv_img):
    masks = []
    '''
    masks.append(cv2.inRange(hsv_img, np.array([102, 134, 117]), np.array([137, 223, 248])))
    masks.append(cv2.inRange(hsv_img, np.array([105, 134, 158]), np.array([137, 200, 242])))
    masks.append(cv2.inRange(hsv_img, np.array([104, 163, 157]), np.array([129, 199, 196])))
    masks.append(cv2.inRange(hsv_img, np.array([104, 147, 185]), np.array([146, 193, 218])))
    masks.append(cv2.inRange(hsv_img, np.array([100, 89, 186]), np.array([148, 194, 222])))
    masks.append(cv2.inRange(hsv_img, np.array([101, 149, 177]), np.array([115, 185, 228])))
    '''
    masks.append(cv2.inRange(hsv_img, np.array([102, 179, 212]), np.array([109, 220, 253])))
    masks.append(cv2.inRange(hsv_img, np.array([101, 166, 186]), np.array([114, 213, 247])))

    mask_blue = masks[0]
    for mask in masks:
        mask_blue += mask
    return mask_blue


def handle(frame):
    point1 = []
    point2 = []

    enable = 50
    state = []

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, -1)
    frame_blur = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame_blur, cv2.COLOR_RGB2HSV)

    mask_blue = get_mask_blue(hsv)
    mask_green = get_mask_green(hsv)

    contours1 = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours1 = imutils.grab_contours(contours1)

    if len(contours1) != 0:
        c = max(contours1, key=cv2.contourArea)
        area1 = cv2.contourArea(c)
        if area1 > enable:
            cv2.drawContours(frame, [c], -1, (249, 240, 0), 2)
            m = cv2.moments(c)
            if m["m00"] != 0:
                cx1 = int(m["m10"] / m["m00"])
                cy1 = int(m["m01"] / m["m00"])
            else:
                cx1, cy1 = 0, 0

            cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1)
            point1 = (cx1, cy1)
            draw1 = True
        else:
            draw1 = False
    else:
        draw1 = False

    contours2 = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2 = imutils.grab_contours(contours2)

    if len(contours2) != 0:
        c = max(contours2, key=cv2.contourArea)
        area2 = cv2.contourArea(c)
        if area2 > enable:
            cv2.drawContours(frame, [c], -1, (91, 189, 43), 2)
            m = cv2.moments(c)
            if m["m00"] != 0:
                cx2 = int(m["m10"] / m["m00"])
                cy2 = int(m["m01"] / m["m00"])
            else:
                cx2, cy2 = 0, 0

            cv2.circle(frame, (cx2, cy2), 5, (255, 0, 0), -1)
            point2 = (cx2, cy2)
            draw2 = True
        else:
            draw2 = False
    else:
        draw2 = False

    if draw1 & draw2:
        angle = calculate_angle(point1, point2)
        state = (round(angle, 2), point1)
        frame = cv2.arrowedLine(frame, (point1[0], point1[1]), (point2[0], point2[1]), (0, 0, 255), 2)
    return frame, state


def control(trajectory, state_vector, mode, cmd_old):
    if trajectory == "Rectangle":
        ox = 120
        oy = 100
        length = 400
        width = 300

        '''The error of DISTANCE and ANGLE'''
        e_a = 10
        e_d = 150
        e_p = 10
        '''e_p must be less than e_d'''

        if len(state_vector) != 0:
            if (state_vector[1][0] <= ox + length - e_d) and (state_vector[1][1] > oy + width - e_d):
                if 90 < state_vector[0] < 270 - e_a:
                    cmd = "Rotate right"
                    if cmd_old != 4 and mode == "Auto":
                        if threading.activeCount() <= 1:
                            send = threading.Thread(target = sendrequest, args = (root_url+"/4/on", ))
                            send.start()
                    cmd_old = 4
                elif state_vector[0] <= 90 or state_vector[0] > 270 + e_a:
                    cmd = "Rotate left"
                    if cmd_old != 3 and mode == "Auto":
                        if threading.activeCount() <= 1:
                            send = threading.Thread(target = sendrequest, args = (root_url+"/3/on", ))
                            send.start()
                    cmd_old = 3
                else:
                    if state_vector[1][1] > oy + width + e_p:
                        cmd = "Go straight"
                        if cmd_old != 1 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/1/on", ))
                                send.start()
                        cmd_old = 1
                    elif state_vector[1][1] < oy + width - e_p:
                        cmd = "Go back"
                        if cmd_old != 2 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/2/on", ))
                                send.start()
                        cmd_old = 2
                    else:
                        cmd = "Go right"
                        if cmd_old != 6 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/6/on", ))
                                send.start()
                        cmd_old = 6

            elif (state_vector[1][0] > ox + length - e_d) and (state_vector[1][1] >= oy + e_d):
                if 90 < state_vector[0] < 270 - e_a:
                    cmd = "Rotate right"
                    if cmd_old != 4 and mode == "Auto":
                        if threading.activeCount() <= 1:
                            send = threading.Thread(target = sendrequest, args = (root_url+"/4/on", ))
                            send.start()
                    cmd_old = 4
                elif state_vector[0] <= 90 or state_vector[0] > 270 + e_a:
                    cmd = "Rotate left"
                    if cmd_old != 3 and mode == "Auto":
                        if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/3/on", ))
                                send.start()
                    cmd_old = 3
                else:
                    if state_vector[1][0] > ox + length + e_p:
                        cmd = "Go left"
                        if cmd_old != 5 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/5/on", ))
                                send.start()
                        cmd_old = 5
                    elif state_vector[1][0] < ox + length - e_p:
                        cmd = "Go right"
                        if cmd_old != 6 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/6/on", ))
                                send.start()
                        cmd_old = 6
                    else:
                        cmd = "Go straight"
                        if cmd_old != 1 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/1/on", ))
                                send.start()
                        cmd_old = 1

            elif (state_vector[1][0] >= ox + e_d) and (state_vector[1][1] < oy + e_d):
                if 90 < state_vector[0] < 270 - e_a:
                    cmd = "Rotate right"
                    if cmd_old != 4 and mode == "Auto":
                        if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/4/on", ))
                                send.start()
                    cmd_old = 4
                elif state_vector[0] <= 90 or state_vector[0] > 270 + e_a:
                    cmd = "Rotate left"
                    if cmd_old != 3 and mode == "Auto":
                        if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/3/on", ))
                                send.start()
                    cmd_old = 3
                else:
                    if state_vector[1][1] > oy + e_p:
                        cmd = "Go straight"
                        if cmd_old != 1 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/1/on", ))
                                send.start()
                        cmd_old = 1
                    elif state_vector[1][1] < oy - e_p:
                        cmd = "Go back"
                        if cmd_old != 2 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/2/on", ))
                                send.start()
                        cmd_old = 2
                    else:
                        cmd = "Go left"
                        if cmd_old != 5 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/5/on", ))
                                send.start()
                        cmd_old = 5

            elif (state_vector[1][0] < ox + e_d) and (state_vector[1][1] <= oy + width - e_d):
                if 90 < state_vector[0] < 270 - e_a:
                    cmd = "Rotate right"
                    if cmd_old != 4 and mode == "Auto":
                        if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/4/on", ))
                                send.start()
                    cmd_old = 4
                elif state_vector[0] <= 90 or state_vector[0] > 270 + e_a:
                    cmd = "Rotate left"
                    if cmd_old != 3 and mode == "Auto":
                        if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/3/on", ))
                                send.start()
                    cmd_old = 3
                else:
                    if state_vector[1][0] > ox + e_p:
                        cmd = "Go left"
                        if cmd_old != 5 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/5/on", ))
                                send.start()
                        cmd_old = 5
                    elif state_vector[1][0] < ox - e_p:
                        cmd = "Go right"
                        if cmd_old != 6 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/6/on", ))
                                send.start()
                        cmd_old = 6
                    else:
                        cmd = "Go back"
                        if cmd_old != 2 and mode == "Auto":
                            if threading.activeCount() <= 1:
                                send = threading.Thread(target = sendrequest, args = (root_url+"/2/on", ))
                                send.start()
                        cmd_old = 2

            else:
                cmd = "Stop"
                if mode == "Auto":
                    if threading.activeCount() <= 1:
                        send = threading.Thread(target = sendrequest, args = (root_url+"/0/off", ))
                        send.start()
                cmd_old = 0

        else:
            cmd = "Stop"
            if mode == "Auto":
                if threading.activeCount() <= 1:
                        send = threading.Thread(target = sendrequest, args = (root_url+"/0/off", ))
                        send.start()
            cmd_old = 0

        return ox, oy, length, width, cmd

    if trajectory == "Circle":
        center = (320, 240)
        radius = 200
        des_point = None

        if len(state_vector) != 0:
            des_point, line = new_point(trajectory, state_vector[1])
            destination_angle = calculate_angle(state_vector[1], des_point)
            error_angle = abs(state_vector[0] - destination_angle)

            if error_angle > 5:
                if destination_angle <= 180:
                    if destination_angle < state_vector[0] < destination_angle + 180:
                        cmd = "Turn left"
                        # if mode == "Auto":
                    else:
                        cmd = "Turn right"
                        # if mode == "Auto":
                else:
                    if destination_angle - 180 < state_vector[0] < destination_angle:
                        cmd = "Turn right"
                        # if mode == "Auto":
                    else:
                        cmd = "Turn left"
                        # if mode == "Auto":

            elif distance(state_vector[1], des_point) > 5:
                cmd = "Go straight"
                # if mode == "Auto":
            else:
                cmd = "Stop"
                # if mode == "Auto":

        else:
            cmd = "Stop"
            # if mode == "Auto":

        return center, radius, des_point, cmd
