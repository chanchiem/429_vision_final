import datetime, base64
import json
from flask import Flask, render_template, request, Response
import subprocess
import sys

sys.path.insert(0, 'commands')

import time
import datetime as dt

import io

app = Flask(__name__)

## USEFUL VALUES ##

OUTPUT_IMG_SCALE    =   0.5

###################


@app.before_first_request
def do_something_only_once():
    global camera, log
    log = io.open('log.txt', 'wb');


@app.route("/")
def main():
    # global cam
    # Create a template data dictionary to send any data to the template
    templateData = {
        'title': 'Chiem Cam'
    }

    # Pass the template data into the template picam.html and return it to the user
    return render_template('index.html', **templateData)


@app.route("/cmd/<command>")
def test(command=None):
    print "Received invalid command: " + command
    return "Received invalid command: " + command


## DOESN"T WORK RIGHT NOW
## This is to implement a multipart image stream (more efficient because doesn't require constant
## re-requests of frames. It's just a single stream.
# Generator function for the camera feed
def gen():
    frame = base64.b64encode(camera.sample_image());
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + "data:image/jpeg;base64," + frame + b'\r\n')


@app.route("/cmd/video_feed")
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

##########################


@app.route("/cmd/req_picture")
def take_picture():
    img = camera.sample_image_from_operation()

    log.write('Took picture: ' + dt.datetime.now().strftime('%Y-%m-%d at %I.%M.%S %p') + '\n');
    log.flush()

    picture_obj = {
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d at %I.%M.%S %p"),
        'encoded_picture': base64.b64encode(img)
    }

    return json.dumps(picture_obj)

@app.route("/cmd/clicked_picture")
def click_picture():
    x_pos = request.args.get('x')
    y_pos = request.args.get('y')
    client_img_width = request.args.get('width')
    client_img_height = request.args.get('height')

    # camera.start_cv_operation(camera.RAW_VIDEO)
    camera.cv_thread.operation = camera.RAW_VIDEO

    return "x: " + str(x_pos) + " - y: " + str(y_pos) + " - width: " + client_img_width + " - height: " + client_img_height;


if __name__ == "__main__":
    # # allow the camera to warmup
    time.sleep(0.1)
    import cvcam as camera
    camera.set_image_scale(OUTPUT_IMG_SCALE)
    camera.start_cv_operation(camera.FACE_DETECTION)

    app.run(debug=True, host='0.0.0.0')