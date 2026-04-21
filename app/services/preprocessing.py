import cv2
import numpy as np


# =========================
# BLUR THRESHOLD
# =========================
BLUR_THRESHOLD = 95


# =========================
# LIGHTING THRESHOLDS
# =========================
MIN_BRIGHTNESS = 72
MAX_CONTRAST = 65
MAX_GLARE_RATIO = 0.02


# =========================
# BLUR CHECK
# =========================
def compute_blur_metric(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return float(np.var(laplacian))


def check_blur(image):
    score = compute_blur_metric(image)
    passed = score >= BLUR_THRESHOLD

    return {
        "passed": passed,
        "score": score,
        "reason": None if passed else "Image is too blurry. Please retake the photo."
    }


# =========================
# LIGHTING CHECK
# =========================
def compute_lighting_metrics(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    contrast = float(np.std(gray))
    brightness = float(np.mean(gray))
    glare_ratio = float(np.sum(gray > 245) / gray.size)

    return {
        "contrast": contrast,
        "brightness": brightness,
        "glare_ratio": glare_ratio,
    }


def check_lighting(image):
    metrics = compute_lighting_metrics(image)

    if metrics["brightness"] < MIN_BRIGHTNESS:
        return {
            "passed": False,
            "metrics": metrics,
            "reason": "Image is too dark. Increase lighting."
        }

    if metrics["contrast"] > MAX_CONTRAST:
        return {
            "passed": False,
            "metrics": metrics,
            "reason": "Image has too much noise. Try a clearer shot."
        }

    if metrics["glare_ratio"] > MAX_GLARE_RATIO:
        return {
            "passed": False,
            "metrics": metrics,
            "reason": "Image has glare. Avoid reflections."
        }

    return {
        "passed": True,
        "metrics": metrics,
        "reason": None
    }


# =========================
# MAIN PIPELINE
# =========================
def run_preprocessing(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return {
            "passed": False,
            "reason": "Invalid image file."
        }

    lighting = check_lighting(image)
    if not lighting["passed"]:
        return lighting

    blur = check_blur(image)
    if not blur["passed"]:
        return blur

    return {
        "passed": True,
        "reason": None
    }