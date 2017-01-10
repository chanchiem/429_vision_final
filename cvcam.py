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
# import thread
import threading

## ENUMERATIONS ##
RAW_VIDEO = 0
FACE_DETECTION = 1
MOTION_DETECTION = 2
###################

## Singleton Variables ##
face_cascade = cv2.CascadeClassifier(
    '/Users/ChiemSaeteurn/PycharmProjects/Cos429_Final/haarcascade_frontalface_default.xml')
image_out_scale = .5  # Used for output image resizing

print "Starting up camera..."
cam = cv2.VideoCapture(1)
time.sleep(.5)
ret, img = cam.read()

current_operation = RAW_VIDEO
cv_thread = None  # CVThread(RAW_VIDEO)


############################

def get_current_cv_operation():
    return current_operation


# Define a function for the thread
def start_face_detection():
    while True:
        global img
        grabbed, raw_img = cam.read()
        height = len(raw_img)
        width = len(raw_img[0])
        face_detect_scale = .25  # resizing factor before we apply HAAR Cascade
        # This is the one used for face detection. Full resolution is not necessary.
        img_for_faces = imutils.resize(raw_img, width=int(width * face_detect_scale),
                                       height=int(height * face_detect_scale))
        out_img = imutils.resize(raw_img, width=int(width * image_out_scale), height=int(height * image_out_scale))

        if not grabbed:
            break

        gray = cv2.cvtColor(img_for_faces, cv2.COLOR_BGR2GRAY)
        extrapolate_scale = image_out_scale / face_detect_scale
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(out_img, (int(x * extrapolate_scale), int(y * extrapolate_scale)), (
                int(x * extrapolate_scale + w * extrapolate_scale), int(y * extrapolate_scale + h * extrapolate_scale)),
                                  (255, 0, 0), 2)
        img = out_img


# Create two threads as follows
# try:
#     thread.start_new_thread(start_face_detection, ())
# except:
#     print "Error: unable to start thread"

# Create a thread
class CVThread(threading.Thread):
    def __init__(self, operation):
        threading.Thread.__init__(self)
        self.operation = operation
        self.running = False

    def run(self):
        while self.operation == FACE_DETECTION:
            global img
            grabbed, raw_img = cam.read()
            height = len(raw_img)
            width = len(raw_img[0])
            face_detect_scale = .25  # resizing factor before we apply HAAR Cascade
            # This is the one used for face detection. Full resolution is not necessary.
            img_for_faces = imutils.resize(raw_img, width=int(width * face_detect_scale),
                                           height=int(height * face_detect_scale))
            out_img = imutils.resize(raw_img, width=int(width * image_out_scale), height=int(height * image_out_scale))

            if not grabbed:
                break

            gray = cv2.cvtColor(img_for_faces, cv2.COLOR_BGR2GRAY)
            extrapolate_scale = image_out_scale / face_detect_scale
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                frame = cv2.rectangle(out_img, (int(x * extrapolate_scale), int(y * extrapolate_scale)), (
                    int(x * extrapolate_scale + w * extrapolate_scale), int(y * extrapolate_scale + h * extrapolate_scale)),
                                      (255, 0, 0), 2)
            img = out_img
        print "Not face detection. Terminating thread"
        # DO RAW VIDEO
        # start_face_detection()


def sample_image_from_operation():
    global img
    ret, jpg_img = cv2.imencode('.jpg', img);

    return jpg_img


# Returns an image directly from the camera (Without any CV operations)
def get_raw_image():
    image = cam.read()
    ret, jpg_img = cv2.imencode('.jpg', image);
    return jpg_img


def set_image_scale(scale):
    global image_out_scale
    image_out_scale = scale


def start_cv_operation(operation=RAW_VIDEO):
    global current_operation, cv_thread
    current_operation = operation
    cv_thread = CVThread(current_operation)
    cv_thread.start()


def stop():
    cam.release()

    # cv2.destroyAllWindows()
    # stop()
