# Car Dashboard Icon Detection Web App

## Overview
Web application that detects car dashboard warning icons using YOLOv11m and provides explanations and actions.

## Features
- Image upload and camera capture
- Preprocessing checks (blur and lighting)
- YOLOv11 detection
- Annotated output image
- CSV-based message system
- Icon library with explanations
- Suggest new icons feature

## Tech Stack
- Flask
- YOLO (Ultralytics)
- OpenCV
- HTML/CSS/JS

## Setup

1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt

3. Add model:
   Place best.pt in model/

4. Run:
   python app.py

## Notes
- Uploaded images are stored in static/uploads
