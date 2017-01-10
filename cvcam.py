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
import time
import imutils
import CVEnumerations
import threading
import numpy as np
import datetime


## SUBSIDIARY CLASSES ##
class CVThread(threading.Thread):
    def __init__(self, operation):
        threading.Thread.__init__(self)
        self.operation = operation
        self.isRunning = False

    def run(self):
        while self.isRunning:
            # RAW IMAGE OUTPUT
            if self.operation == CVEnumerations.RAW_IMAGE:
                global img
                grabbed, img = get_raw_image()
            # FACE DETECTION
            elif self.operation == CVEnumerations.FACE_DETECTION:
                grabbed, raw_img = get_raw_image()
                height = len(raw_img)
                width = len(raw_img[0])
                face_detect_scale = 1  # resizing factor before we apply HAAR Cascade
                # This is the one used for face detection. Full resolution is not necessary.
                img_for_faces = imutils.resize(raw_img, width=int(width * face_detect_scale),
                                               height=int(height * face_detect_scale))
                if not grabbed:
                    return

                gray = cv2.cvtColor(img_for_faces, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    frame = cv2.rectangle(raw_img, (int(x / face_detect_scale), int(y / face_detect_scale)), (
                        int(x / face_detect_scale + w / face_detect_scale),
                        int(y / face_detect_scale + h / face_detect_scale)),
                                          (255, 0, 0), 2)
                img = raw_img
            # MOTION DETECTION
            # This code was modified from code found on the follow website:
            # http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
            elif self.operation == CVEnumerations.MOTION_DETECTION:
            	global compFrame
            	global start
            	#global frameDeltaSumPrev
            	#global frameDeltaSumCurr
            	#global frameDelta
                grabbed, frame = get_raw_image()
                
                if not grabbed:
                	break
                
                # Converts the image from rgb to gray and blurs the gray image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21,21), 0)
                
                # Sets the comparison frame to gray during the first run through this loop
                if compFrame is None:
                	compFrame = gray
                	continue
                
                # Resets the comparison frame every five seconds
                timeElapsed = time.time() - start
                if timeElapsed > 5:
					start = time.time()
					firstFrame = gray
                	
                # Resets timeElapsed counter if camera detects movement
                #if frameDelta is not None:
	            #   frameDeltaSumPrev = np.sum(np.sum(frameDelta))
				#	frameDeltaSumCurr = np.sum(np.sum(cv2.absdiff(firstFrame, gray)))
				#	if abs(int(frameDeltaSumPrev) - int(frameDeltaSumCurr)) > 20000:
				#		start = time.time()
                
                # Computes the absolute difference in pixel values of the comparison
                # frame and the current frame
                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                	cv2.CHAIN_APPROX_SIMPLE)
                	
                # Draws rectangles around the areas where motion was detected
                for c in cnts:
                	if cv2.contourArea(c) < 500:
                		continue
                	(x, y, w, h) = cv2.boundingRect(c)
                	cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                	
                img = frame
            # CANNY EDGE DETECTION
            elif self.operation == CVEnumerations.CANNY_EDGE_DETECTION:
                grabbed, raw_img = get_raw_image()
                img = cv2.Canny(raw_img, 100, 200)

        print "end thread"

############################

def get_current_cv_operation():
    return cv_thread.operation


def sample_image_from_operation():
    global img
    ret, jpg_img = cv2.imencode('.jpg', img);

    return jpg_img


def set_image_scale(scale):
    global image_out_scale
    image_out_scale = scale


def get_raw_image():
    ret, raw_img = cam.read()
    height = len(raw_img)
    width = len(raw_img[0])
    res_img = imutils.resize(raw_img, width=int(width * image_out_scale), height=int(height * image_out_scale))
    return ret, res_img


def switch_cv_operation(operation=CVEnumerations.RAW_IMAGE):
    global cv_thread
    cv_thread.operation = operation


def start_cv_operation():
    if cv_thread is not None:
        if not cv_thread.isRunning:
            cv_thread.isRunning = True
            cv_thread.start()


def stop():
    cv_thread.isRunning = False
    cam.release()
    # cv2.destroyAllWindows()
    # stop()


######################
## Start Everything ##
######################

#face_cascade = cv2.CascadeClassifier(
#    '/Users/ChiemSaeteurn/PycharmProjects/Cos429_Final/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    
image_out_scale = .5  # Used for output image resizing

print "Starting up camera..."
cam = cv2.VideoCapture(0)
time.sleep(.5)
ret, img = get_raw_image()

cv_thread = CVThread(CVEnumerations.RAW_IMAGE)

compFrame = None
start = time.time()
#frameDeltaSumPrev = 0
#frameDeltaSumCurr = 0
#frameDelta = None