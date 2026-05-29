import os
from pathlib import Path

from flask import Blueprint, current_app, jsonify, render_template, request, session, redirect
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
        detections = run_detection(str(saved_path))

        if not detections:
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

        detections = attach_messages_to_detections(detections)

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
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
            bypass_warning=bypass_warning,
            show_detect_anyway=False,
            retry_image_filename=None,
        )

    except Exception as e:
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

    if "image" not in request.files:
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

    if file.filename == "":
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
            bypass_warning=None,
            show_detect_anyway=True,
            retry_image_filename=filename,
        )

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


@main.route("/find-repair")
def find_repair_page():
    return render_template("find_repair.html")


_DASHLY_SYSTEM_PROMPT = """
You are Dashly, a casual and friendly AI mechanic assistant.
You specialise exclusively in car dashboard warning lights and vehicle issues.

Personality: speak like a knowledgeable friend who happens to be a mechanic — clear,
practical, and reassuring. Avoid unnecessary jargon; explain any technical terms you use.

What you help with:
- Explaining what dashboard warning lights mean and their severity
- Step-by-step repair guides for common car problems
- When a problem is safe to DIY vs when to see a professional mechanic
- Rough cost ranges for repairs (never exact prices — always give a range)
- Safety warnings and when to stop driving immediately
- Emergency roadside advice

Rules:
- Stay focused on car dashboard warnings and automotive topics only.
- If asked about anything unrelated, politely redirect to car questions.
- Always lead with safety when a warning could be dangerous.
- Use bullet points or numbered steps when giving instructions.
- When uncertain about severity, advise consulting a mechanic in person.
- Keep responses concise but complete — avoid very long walls of text.
""".strip()


@main.route("/chatbot", methods=["GET", "POST"])
def chatbot_page():
    if request.method == "GET":
        return render_template("chatbot.html")

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request body."}), 400

    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return jsonify({"error": "Chatbot is not configured (missing API key)."}), 503

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # Build the contents list: prior history + current user message
        contents = []
        for msg in history:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=msg["content"])])
            )
        contents.append(
            types.Content(role="user", parts=[types.Part(text=user_message)])
        )

        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=_DASHLY_SYSTEM_PROMPT,
            ),
        )

        return jsonify({"response": response.text})

    except Exception:
        return jsonify({"error": "Failed to get a response. Please try again."}), 500



@main.route("/results")
def results_page():
    return render_template("results.html")

