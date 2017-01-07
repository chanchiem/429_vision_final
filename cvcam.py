########################################################################
########################################################################
## This is the universal implementation of a singleton camera class.
## This  will allow clients to sample
## live images from the camera and live video feeds.
## One unique property of this class is that it maintains a circular
## buffer of video data with a size of about 15 seconds. This will allow
## users to acquire video feed 15 seconds before.
########################################################################
########################################################################
import cv2
import datetime
import time
import imutils
import numpy

print "Starting up camera..."
cam = cv2.VideoCapture(1)
time.sleep(.5)


def sample_image(scale=1):
    ret, img = cam.read()

    # Resize the scale of the image
    height = len(img)
    width = len(img[0])
    img = imutils.resize(img, width=int(width*scale), height=int(height*scale));

    ret, jpg_img = cv2.imencode('.jpg', img);

    return jpg_img


def stop():
    cam.release()

    # cv2.destroyAllWindows()
    # stop()
