import datetime, base64
import json
from flask import Flask, render_template, request
import subprocess
import sys
sys.path.insert(0, 'commands')

import time
import cv2
import imutils
import datetime as dt

import io

app = Flask(__name__)


@app.before_first_request
def do_something_only_once():
    global camera, log
    log = io.open('log.txt', 'wb');

@app.route("/")
def main():
    # global cam
    # Create a template data dictionary to send any data to the template
    templateData = {
        'title' : 'Chiem Cam'
        }

    # Pass the template data into the template picam.html and return it to the user
    return render_template('index.html', **templateData)

@app.route("/cmd/")
@app.route("/cmd/<command>")
def test(command=None):
    print command
    return command

@app.route("/cmd/req_picture")
def take_picture():
    # img = cv2.imencode('.jpg', cam.sample_image())[1];
    # img = cv2.imread('test.jpg', cv2.IMREAD_COLOR);
    camera.

    # camera.annotate_background = True
    # camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %I:%M.%S %p')
    # camera.capture(rawCapture, format="bgr")
    # img = cv2.imencode('.png', rawCapture.array)[1];

    log.write('Took picture: ' + dt.datetime.now().strftime('%Y-%m-%d at %I.%M.%S %p') + '\n');
    log.flush()

    picture_obj = {
        'timestamp' : datetime.datetime.now().strftime("%Y-%m-%d at %I.%M.%S %p"),
        'picture' : base64.b64encode(img)
    }
    return json.dumps(picture_obj)

if __name__ == "__main__":
    # # allow the camera to warmup
    time.sleep(0.1)
    import cvcam as camera
    app.run(debug=True, host='0.0.0.0')