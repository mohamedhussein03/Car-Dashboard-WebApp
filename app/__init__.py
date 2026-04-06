from flask import Flask

from config import (
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    STATIC_DIR,
    TEMPLATES_DIR,
    UPLOAD_FOLDER,
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

    from app.routes import main
    app.register_blueprint(main)

    return app