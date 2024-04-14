import cv2 as cv
from time import sleep

video = cv.VideoCapture(0)
sleep(0.5)

first_frame = None

while True:
    check, frame = video.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_gaus_frame = cv.GaussianBlur(gray_frame, (21,21), 0)
    
    if first_frame is None:
        first_frame = gray_gaus_frame
    
    delta_frame = cv.absdiff(first_frame, gray_gaus_frame)
    thresh_frame = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
    dil_frame = cv.dilate(thresh_frame, None, iterations=2)
    
    contours, check = cv.findContours(dil_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    
    if key == ord("q"):
        break

video.release()