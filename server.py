from flask import Flask, render_template, request, send_file
import cv2
import numpy as np

app = Flask(__name__)
latest_frame = None

@app.route("/")
def index():
    return render_template("view.html")

@app.route("/phone")
def phone():
    return render_template("phone.html")

@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    global latest_frame
    file = request.files['frame']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    _, jpeg = cv2.imencode('.jpg', img)
    latest_frame = jpeg.tobytes()
    return "OK"

@app.route("/latest.jpg")
def latest():
    global latest_frame
    if latest_frame is None:
        return "No Image", 404
    return latest_frame, 200, {"Content-Type": "image/jpeg"}

app.run(host="0.0.0.0", port=5000)
