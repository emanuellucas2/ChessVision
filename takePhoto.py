# program to capture single image from webcam in python
  
# importing OpenCV library
from cv2 import *
  
# initialize the camera
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that
cam_port = 0
cam = VideoCapture(cam_port)

while 1:

    input("Press enter bottom to take photo")

    # reading the input using the camera
    result, image = cam.read()
      
    # If image will detected without any error, 
    # show result
    if result:
      
        # showing result, it take frame name and image 
        # output
        focus = 100
        cam.set(28, focus)
        cam.set(CAP_PROP_AUTOFOCUS, 0) 
        imshow("Photo", image)
      
        imwrite("homog.png", image)

        # If keyboard interrupt occurs, destroy image 
        # window
        waitKey(0)
        destroyWindow("Photo")
      
    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")
