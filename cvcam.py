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

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print "Starting up camera..."
camera = cv2.VideoCapture(0)
time.sleep(.5)

while True:
	(grabbed, frame) = camera.read()
	
	if not grabbed: 
		break
		
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
	
	cv2.imshow('frame', frame)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cv2.destroyAllWindows()

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
