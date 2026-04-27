from pathlib import Path

from flask import Blueprint, current_app, render_template, request, session, redirect
from werkzeug.utils import secure_filename

from app.services.detector import run_detection, save_annotated_image
from app.services.icon_library import load_icon_library
from app.services.message_service import attach_messages_to_detections
from app.services.preprocessing import run_preprocessing
from app.utils.file_helpers import generate_output_filename

from uuid import uuid4

main = Blueprint("main", __name__)


def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in {"png", "jpg", "jpeg", "webp"}


def run_detection_pipeline(saved_path, filename, preprocessing_result=None, bypass_warning=None):
    try:
        print("run_detection_pipeline started", flush=True)
        print("Detection image path:", saved_path, flush=True)

        print("Starting model detection", flush=True)
        detections = run_detection(str(saved_path))
        print("Detection complete", flush=True)
        print("Detections count:", len(detections), flush=True)

        if not detections:
            print("No detections found", flush=True)
            return render_template(
                "results.html",
                status="accepted",
                message="Image processed, but no dashboard icons were detected.",
                details=preprocessing_result,
                image_url=f"/static/uploads/{filename}",
                detections=[],
                bypass_warning=bypass_warning,
                show_detect_anyway=False,
                retry_image_filename=None,
            )

        print("Attaching messages to detections", flush=True)
        detections = attach_messages_to_detections(detections)
        print("Messages attached", flush=True)

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        annotated_filename = generate_output_filename(filename, prefix="annotated")
        annotated_path = upload_folder / annotated_filename

        print("Saving annotated image to:", annotated_path, flush=True)
        save_annotated_image(saved_path, detections, annotated_path)
        print("Annotated image saved", flush=True)

        annotated_image_url = f"/static/uploads/{annotated_filename}"
        print("Rendering detected results page", flush=True)

        return render_template(
            "results.html",
            status="detected",
            message="Detection completed successfully.",
            details=preprocessing_result,
            image_url=annotated_image_url,
            detections=detections,
            bypass_warning=bypass_warning,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    except Exception as e:
        print("run_detection_pipeline error:", repr(e), flush=True)
        return render_template(
            "results.html",
            status="error",
            message=f"Detection pipeline failed: {str(e)}",
            details=None,
            image_url=f"/static/uploads/{filename}",
            detections=[],
            bypass_warning=None,
            show_detect_anyway=False,
            retry_image_filename=None,
        )


@main.route("/")
def home():
    return render_template("index.html")

@main.route("/health")
def health():
    return "OK", 200

@main.route("/set-language/<language>")
def set_language(language):
    if language in current_app.config["LANGUAGES"]:
        session["language"] = language

    return redirect(request.referrer or "/")


@main.route("/detect", methods=["GET", "POST"])
def detect_page():
    if request.method == "GET":
        return render_template("detect.html")

    print("POST /detect reached", flush=True)

    if "image" not in request.files:
        print("No image in request.files", flush=True)
        return render_template(
            "results.html",
            status="error",
            message="No image was uploaded.",
            details=None,
            image_url=None,
            detections=[],
            bypass_warning=None,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    file = request.files["image"]
    print("Uploaded filename:", file.filename, flush=True)

    if file.filename == "":
        print("Empty filename received", flush=True)
        return render_template(
            "results.html",
            status="error",
            message="Please choose an image first.",
            details=None,
            image_url=None,
            detections=[],
            bypass_warning=None,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    if not allowed_file(file.filename):
        print("Unsupported file type", flush=True)
        return render_template(
            "results.html",
            status="error",
            message="Unsupported file type. Upload PNG, JPG, JPEG, or WEBP.",
            details=None,
            image_url=None,
            detections=[],
            bypass_warning=None,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    original_extension = file.filename.rsplit(".", 1)[1].lower()
    safe_stem = secure_filename(file.filename.rsplit(".", 1)[0])
    if not safe_stem:
        safe_stem = "uploaded_image"
    filename = f"{safe_stem}_{uuid4().hex[:8]}.{original_extension}"

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    saved_path = upload_folder / filename
    file.save(saved_path)

    print("Image saved at:", saved_path, flush=True)
    print("Starting preprocessing", flush=True)

    preprocessing_result = run_preprocessing(str(saved_path))
    print("Preprocessing result:", preprocessing_result, flush=True)

    image_url = f"/static/uploads/{filename}"

    if not preprocessing_result["passed"]:
        print("Image rejected by preprocessing", flush=True)
        return render_template(
            "results.html",
            status="rejected",
            message=preprocessing_result["reason"],
            details=preprocessing_result,
            image_url=image_url,
            detections=[],
            bypass_warning=None,
            show_detect_anyway=True,
            retry_image_filename=filename,
        )

    print("Passing to detection pipeline", flush=True)

    return run_detection_pipeline(
        saved_path=saved_path,
        filename=filename,
        preprocessing_result=preprocessing_result,
        bypass_warning=None,
    )


@main.route("/detect-anyway", methods=["POST"])
def detect_anyway():
    filename = request.form.get("filename", "").strip()

    if not filename:
        return render_template(
            "results.html",
            status="error",
            message="No image was found for retry.",
            details=None,
            image_url=None,
            detections=[],
            bypass_warning=None,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    saved_path = upload_folder / filename

    if not saved_path.exists():
        return render_template(
            "results.html",
            status="error",
            message="The uploaded image could not be found. Please upload it again.",
            details=None,
            image_url=None,
            detections=[],
            bypass_warning=None,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    bypass_warning = (
        "You chose to continue detection without retaking the image. "
        "Image quality issues such as blur or poor lighting may reduce detection accuracy."
    )

    return run_detection_pipeline(
        saved_path=saved_path,
        filename=filename,
        preprocessing_result=None,
        bypass_warning=bypass_warning,
    )


@main.route("/library")
def library_page():
    icons = load_icon_library()
    supported_icons = [icon for icon in icons if icon["category"] == "supported"]
    further_icons = [icon for icon in icons if icon["category"] == "further"]

    return render_template(
        "library.html",
        supported_icons=supported_icons,
        further_icons=further_icons,
    )


@main.route("/results")
def results_page():
    return render_template("results.html")

