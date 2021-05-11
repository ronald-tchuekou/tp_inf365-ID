import cv2
import numpy as np

""" Function that detect cars in the video. """
cascade_car = cv2.CascadeClassifier('./cars.xml')
cap = cv2.VideoCapture('video2.avi')
is_opened = False;
while cap.isOpened():
    is_opened = True
    ret, img = cap.read()
    if ret == True: # When the image is reading well.
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        tickmark = cv2.getTickCount()
        car = cascade_car.detectMultiScale(gray_img, scaleFactor=1.15, minNeighbors=3)
        for x, y, w, h in car:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 200), 2)
            cv2.putText(img, "car", (x+5, y-2), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 200), 2)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tickmark)
        cv2.putText(img, "FPS: {:05.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 200, 0), 2)
        cv2.imshow('Detect face in video', img)
        if(cv2.waitKey(1) == ord('q')):
            break
    else:
        print('Error has provide.')
        break

if not is_opened:
    print ('The element is not read.')
print('Operation about detection is finish.')
cap.release()
cv2.destroyAllWindows()