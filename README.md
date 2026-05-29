# Car Dashboard Icon Detection Web App

## Overview
Web application that detects car dashboard warning icons using YOLOv11m and provides explanations, repair guidance, and AI-powered assistance.

## Features
- Image upload and camera capture
- Preprocessing checks (blur and lighting detection)
- YOLOv11m model detection
- Annotated output image with bounding boxes
- CSV-based message system for icon explanations
- Icon library with detailed descriptions
- Suggest new icons feature
- Find Repair page with geolocation to locate nearby mechanics
- Call tow truck button for Hatla2ee roadside assistance
- Dashly AI chatbot for dashboard warnings and repair guidance
- Professional, responsive UI design
- Mobile-first design approach

## Tech Stack
- Flask
- YOLOv11m (Ultralytics)
- OpenCV
- Google Gemini AI (Dashly chatbot)
- HTML/CSS/JavaScript
- Python 3.11+

## Setup

1. Clone the repo:
```bash
git clone <repo-url>
cd car-dashboard-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add model file:
   Place `best.pt` in the `model/` folder

4. Set up environment variables:
   Create a `.env` file in the project root:
