from flask import Flask, render_template, redirect, url_for
import os
import cv2
import csv
from datetime import datetime

app = Flask(__name__)

# Flag to control camera usage
USE_CAMERA = os.environ.get("USE_CAMERA", "0") == "1"

# Initialize video capture only if USE_CAMERA is enabled
cap = cv2.VideoCapture(0) if USE_CAMERA else None

# Simulated face recognition (replace with actual logic)
def recognize_face():
    if not USE_CAMERA or cap is None:
        return None

    ret, frame = cap.read()
    if not ret:
        return None

    # Simulate recognition
    recognized_name = "John Doe"
    log_attendance(recognized_name)
    return recognized_name

# Logs attendance into a CSV file
def log_attendance(name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("attendance_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, timestamp])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan")
def scan():
    name = recognize_face()
    if name:
        return f"✅ Attendance logged for {name}!"
    else:
        return "❌ Face not recognized or camera unavailable."

@app.route("/logs")
def logs():
    rows = []
    try:
        with open("attendance_log.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
    except FileNotFoundError:
        pass
    return render_template("logs.html", rows=rows)

# Only allow shutdown in local debug mode
# Commented out for Render
# @app.route("/shutdown")
# def shutdown():
#     os._exit(0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
