import cv2 as cv
from time import sleep
from emailing import send_email
from threading import Thread


# Set video capture instance
video = cv.VideoCapture(0)

# Add 1 sleep second to allow the camera to initiate
sleep(1)

#Control variables
first_frame = None
status_list = []
max_rectangle = 0

while True:
    # Main loop
    status = 0
    rectangle_area = 0
    
    # Capture frame
    check, frame = video.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_gaus_frame = cv.GaussianBlur(gray_frame, (21,21), 0)
    
    if first_frame is None:
        # Set reference frame
        first_frame = gray_gaus_frame
    
    # Make transformation to the current frame
    delta_frame = cv.absdiff(first_frame, gray_gaus_frame)
    thresh_frame = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
    dil_frame = cv.dilate(thresh_frame, None, iterations=2)
    
    contours, check = cv.findContours(dil_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Set bounding box
        if cv.contourArea(contour) < 2000:
            continue
        x, y, w, h = cv.boundingRect(contour)
        rectangle = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        
        if rectangle.any():
            # Set status to 1 if there is an object detected
            status = 1
            rectangle_area = int(w * h / 100)
    
    status_list.append(status)
    status_list = status_list[-2:]
        
    if rectangle_area > max_rectangle:
        # Save the frame which have the biggest object area
        cv.imwrite("image.png", frame)
        max_rectangle = rectangle_area
            
    if status_list[0] == 1 and status_list[1] == 0:
        # When there is an objet detected, send emil and reset object rectangle
        email_thread = Thread(target=send_email)
        email_thread.daemon = True
        email_thread.start()
        max_rectangle = 0
        
    cv.imshow("video", frame)
    
    key = cv.waitKey(1)
    
    if key == ord("q"):
        break

video.release()