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
                ret, img = get_raw_image()
            # FACE DETECTION
            elif self.operation == CVEnumerations.FACE_DETECTION:
                grabbed, raw_img = get_raw_image()
                height = len(raw_img)
                width = len(raw_img[0])
                face_detect_scale = .25  # resizing factor before we apply HAAR Cascade
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
            elif self.operation == CVEnumerations.MOTION_DETECTION:
                i = 1
            elif self.operation == CVEnumerations.CANNY_EDGE_DETECTION:
                grabbed, raw_img = get_raw_image()
                img = cv2.Canny(raw_img, 100, 200)

        print "end thread"


###

## Singleton Variables ##
face_cascade = cv2.CascadeClassifier(
    '/Users/ChiemSaeteurn/PycharmProjects/Cos429_Final/haarcascade_frontalface_default.xml')
image_out_scale = .5  # Used for output image resizing

print "Starting up camera..."
cam = cv2.VideoCapture(1)
time.sleep(.5)
ret, img = cam.read()
height = len(img)
width = len(img[0])
img = imutils.resize(img, width=int(width * image_out_scale), height=int(height * image_out_scale))

cv_thread = CVThread(CVEnumerations.RAW_IMAGE)


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
