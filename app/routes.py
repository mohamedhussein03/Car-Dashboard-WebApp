from pathlib import Path

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename

from app.services.detector import run_detection, save_annotated_image
from app.services.icon_library import load_icon_library
from app.services.message_service import attach_messages_to_detections
from app.services.preprocessing import run_preprocessing
from app.utils.file_helpers import generate_output_filename


main = Blueprint("main", __name__)


def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in {"png", "jpg", "jpeg", "webp"}


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/detect", methods=["GET", "POST"])
def detect_page():
    if request.method == "GET":
        return render_template("detect.html")

    if "image" not in request.files:
        return render_template(
            "results.html",
            status="error",
            message="No image was uploaded.",
            details=None,
            image_url=None,
            detections=[],
        )

    file = request.files["image"]

    if file.filename == "":
        return render_template(
            "results.html",
            status="error",
            message="Please choose an image first.",
            details=None,
            image_url=None,
            detections=[],
        )

    if not allowed_file(file.filename):
        return render_template(
            "results.html",
            status="error",
            message="Unsupported file type. Upload PNG, JPG, JPEG, or WEBP.",
            details=None,
            image_url=None,
            detections=[],
        )

    filename = secure_filename(file.filename)
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    saved_path = upload_folder / filename
    file.save(saved_path)

    preprocessing_result = run_preprocessing(str(saved_path))
    image_url = f"/static/uploads/{filename}"

    if not preprocessing_result["passed"]:
        return render_template(
            "results.html",
            status="rejected",
            message=preprocessing_result["reason"],
            details=preprocessing_result,
            image_url=image_url,
            detections=[],
        )

    detections = run_detection(str(saved_path))

    if not detections:
        return render_template(
            "results.html",
            status="accepted",
            message="Image passed preprocessing, but no dashboard icons were detected.",
            details=preprocessing_result,
            image_url=image_url,
            detections=[],
        )

    detections = attach_messages_to_detections(detections)

    annotated_filename = generate_output_filename(filename, prefix="annotated")
    annotated_path = upload_folder / annotated_filename
    save_annotated_image(saved_path, detections, annotated_path)

    annotated_image_url = f"/static/uploads/{annotated_filename}"

    return render_template(
        "results.html",
        status="detected",
        message="Detection completed successfully.",
        details=preprocessing_result,
        image_url=annotated_image_url,
        detections=detections,
    )


@main.route("/library")
def library_page():
    icons = load_icon_library()
    return render_template("library.html", icons=icons)


@main.route("/results")
def results_page():
    return render_template("results.html")