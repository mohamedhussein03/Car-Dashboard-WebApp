from flask import Flask
from flask import render_template

from config import (
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    STATIC_DIR,
    TEMPLATES_DIR,
    UPLOAD_FOLDER,
    SUGGESTIONS_FOLDER,
)


def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    SUGGESTIONS_FOLDER.mkdir(parents=True, exist_ok=True)

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