# Webcam monitoring app with email alert

This project takes live video from the webcam and detects objects that were not in the original first frame, meaning that the first frame taken by the camera will be used as a reference to detect other objects.

This is done through the opencv library, which is used to make some transformations on the frames and detect new objects by substracting the current frame and the first frame. Once an object enters the frame, it will be detected and a bounding box will be drawn around the object, tracking it until it leaves the frame. When the object leaves the frame, the program will send an email with an image of the object as an attachment.

After the object leaves the frame, the program will continue execution, repeating the same pattern of detecting objects and sending an email when the object leaves.
