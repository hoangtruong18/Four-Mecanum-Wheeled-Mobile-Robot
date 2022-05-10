import cv2
import os

cap = cv2.VideoCapture(1)
sampleNum = 0

while True:
    sampleNum += 1
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    if not os.path.exists("dataset"):
        os.makedirs('dataset')

    cv2.imwrite('dataset/sample' + str(sampleNum) + '.jpg', frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    if sampleNum >= 200:
        break

cap.release()
cv2.destroyAllWindows()