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
import numpy

print "Starting up camera..."
cam = cv2.VideoCapture(1)
time.sleep(.5)

def sample_image():
	ret, img = cam.read()
	return img

def stop():
	cam.release()

# cv2.destroyAllWindows()
# stop()