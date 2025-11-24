from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import time

app = Flask(__name__)
latest_frame = None

@app.route("/phone")
def phone():
    return render_template("stream.html")

@app.route("/")
def index():
    return render_template("view.html")

@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    global latest_frame
    data = request.files['frame'].read()
    np_arr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    latest_frame = frame
    return "OK"

def generate_mjpeg():
    global latest_frame
    while True:
        if latest_frame is None:
            time.sleep(0.1)
            continue
        ret, jpeg = cv2.imencode('.jpg', latest_frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@app.route("/video_feed")
def video_feed():
    return Response(generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("Server running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)
