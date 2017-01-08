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
import thread

face_cascade = cv2.CascadeClassifier(
    '/Users/ChiemSaeteurn/PycharmProjects/Cos429_Final/haarcascade_frontalface_default.xml')

print "Starting up camera..."
cam = cv2.VideoCapture(1)
time.sleep(.5)
ret, img = cam.read()


# Define a function for the thread
def start_face_detection(output_scale=.5):
    while True:
        global img
        grabbed, raw_img = cam.read()
        height = len(raw_img)
        width = len(raw_img[0])
        face_detect_scale = .25
        # This is the one used for face detection. Full resolution is not necessary.
        img_for_faces = imutils.resize(raw_img, width=int(width * face_detect_scale), height=int(height * face_detect_scale))
        out_img = imutils.resize(raw_img, width=int(width * output_scale), height=int(height * output_scale))

        if not grabbed:
            break

        gray = cv2.cvtColor(img_for_faces, cv2.COLOR_BGR2GRAY)
        extrapolate_scale = output_scale/face_detect_scale
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(out_img, (int(x * extrapolate_scale), int(y * extrapolate_scale)), (int(x * extrapolate_scale + w * extrapolate_scale), int(y * extrapolate_scale + h * extrapolate_scale)), (255, 0, 0), 2)

        img = out_img

# Create two threads as follows
try:
    thread.start_new_thread(start_face_detection, ())
except:
    print "Error: unable to start thread"

def sample_image(scale=1):
    global img
    # ret, img = cam.read()

    # Resize the scale of the image
    # height = len(img)
    # width = len(img[0])
    # img = imutils.resize(img, width=int(width*scale), height=int(height*scale));

    ret, jpg_img = cv2.imencode('.jpg', img);

    return jpg_img


def stop():
    cam.release()

    # cv2.destroyAllWindows()
    # stop()
