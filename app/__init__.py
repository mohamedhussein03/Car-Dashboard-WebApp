from flask import Flask
from flask import render_template
from flask import session
from flask_babel import Babel
from ultralytics import YOLO

from config import (
    BASE_DIR,
    MAX_CONTENT_LENGTH,
    MODEL_PATH,
    SECRET_KEY,
    STATIC_DIR,
    TEMPLATES_DIR,
    UPLOAD_FOLDER,
)


babel = Babel()
MODEL = None


def get_locale():
    return session.get("language", "en")


def initialize_model():
    global MODEL

    if MODEL is None:
        print("Loading YOLO model at startup...", flush=True)
        MODEL = YOLO(str(MODEL_PATH))
        print("YOLO model loaded successfully", flush=True)


def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = str(BASE_DIR / "translations")
    app.config["LANGUAGES"] = {
        "en": "English",
        "ar": "العربية",
    }

    babel.init_app(app, locale_selector=get_locale)

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    initialize_model()

    from app.routes import main
    app.register_blueprint(main)

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template(
            "results.html",
            status="error",
            message="The uploaded image is too large. Please upload a smaller image.",
            details=None,
            image_url=None,
            detections=[],
            show_detect_anyway=False,
            retry_image_filename=None,
        ), 413

    return app