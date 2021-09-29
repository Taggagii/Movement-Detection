import cv2
import numpy as np
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("error opening file")

ret, previous = cap.read()

while cap.isOpened():
    ret, frame = cap.read()

    diff = cv2.absdiff(previous, frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=4)
    contours, hiers = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours != []:
        #cv2.drawContours(previous, contours, -1, (0, 255, 0), 2)
        for contour, hier in zip(contours, hiers[0]):
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900  or hier[3] != -1: #my attempt at keeping boxes out of boxes
                continue
            cv2.rectangle(previous, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(previous, "Status: Moving", (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)

    cv2.imshow('thing', previous)
    previous = frame


    if cv2.waitKey(60) == ord('`'):
        break

cv2.destroyAllWindows()

