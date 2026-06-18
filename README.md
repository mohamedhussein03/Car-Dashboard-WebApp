# Car Dashboard Icon Detection Web App

Detect car dashboard warning indicators in real-time using YOLOv11m. Get instant explanations, repair guidance, and AI-powered assistance from Dashly chatbot.

## Features

- Real-time dashboard icon detection with YOLOv11m
- Instant warning explanations and safety information
- Find nearby mechanics using geolocation
- Call Hatla2ee roadside assistance directly from the app
- Dashly AI chatbot for repair guidance and cost estimates
- Professional, mobile-first UI
- Preprocessing checks for image quality
- CSV-based icon library system
- Suggest new icons feature

## Screenshots

### Home Screen
<img width="1395" height="908" alt="Screenshot 2026-06-18 104328" src="https://github.com/user-attachments/assets/f1518d6d-3fe4-44de-af12-695d9c669060" />


### Detection Results
<img width="1265" height="903" alt="Screenshot 2026-06-18 104623" src="https://github.com/user-attachments/assets/394996ab-e708-446a-be80-58a130d30289" />


### Find Repair Page
<img width="1232" height="895" alt="Screenshot 2026-06-18 104637" src="https://github.com/user-attachments/assets/a1eff934-85ec-4c06-bd80-f178780dc075" />


### Dashly AI Chatbot
<img width="916" height="903" alt="Screenshot 2026-06-18 104705" src="https://github.com/user-attachments/assets/f29c26ae-4b7e-4f85-99d9-25bb7d04611c" />


### Icon Library
<img width="1197" height="904" alt="Screenshot 2026-06-18 104731" src="https://github.com/user-attachments/assets/a7c93678-676c-4f58-8370-254447c47cff" />


## Tech Stack

- **Backend**: Flask
- **AI/ML**: YOLOv11m (Ultralytics), Google Gemini API
- **Computer Vision**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: CSV
- **Deployment**: Railway
- **Python**: 3.11+

## Quick Start

### Prerequisites
- Python 3.11+
- Git
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/car-dashboard-detection.git
cd car-dashboard-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add the YOLOv11m model:
   Place `best.pt` in the `model/` folder

4. Set up environment variables:
   Create `.env` in the project root:

5. Run locally:
```bash
python app.py
```
Access at `https://localhost:10000`

## Features in Detail

### Dashboard Detection
Upload a car dashboard image or use your camera. The app instantly detects warning indicators and provides clear explanations of each warning.

### Smart Preprocessing
Automatic checks for image blur and lighting issues. Ensures detection accuracy with quality feedback.

### Find Repair
Locate nearby mechanics using your device location. Or call Hatla2ee for immediate roadside assistance and tow truck service in Egypt.

### Dashly AI Assistant
Ask Dashly questions about any dashboard warning. Get step-by-step repair guides, learn when to DIY vs. call a mechanic, and receive cost estimates.

### Icon Library
Browse all supported dashboard indicators. View explanations, severity levels, and recommended actions for each icon.

## Project Structure   
├── app.py                 # Main Flask entry point

├── app/

│   ├── init.py       # App factory

│   ├── routes/           # Flask routes

│   ├── templates/        # HTML templates

│   └── static/           # CSS, JS, uploads

├── model/

│   └── best.pt           # YOLOv11m model (not in repo)

├── requirements.txt      # Python dependencies

├── mise.toml            # Python version config

└── README.md

## Usage

1. Open the web app
2. Upload a dashboard image or capture with camera
3. View detection results with explanations
4. Ask Dashly questions about warnings
5. Find nearby repair shops or call for tow truck assistance

## API Keys

Get your free Google Gemini API key:
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Create new API key
4. Add to `.env` file

## Notes

- Uploaded images stored in `static/uploads/`
- Model file included in repository
- `.env` file never pushed to GitHub (security)
- Geolocation requires HTTPS
- Works on desktop and mobile browsers

## Future Enhancements

- Multi-language support
- Video detection stream
- Parts marketplace integration
- Insurance claim assistance
- Repair history tracking
- Fleet management features
- Mobile app (iOS/Android)

## Support

Need help? Contact me through my Email.
