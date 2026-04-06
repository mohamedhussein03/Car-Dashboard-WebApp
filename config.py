from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_FOLDER = STATIC_DIR / "uploads"
ICONS_FOLDER = STATIC_DIR / "icons"
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"

MODEL_PATH = MODEL_DIR / "best.pt"
CLASSES_PATH = MODEL_DIR / "classes.txt"
ICON_MESSAGES_CSV = DATA_DIR / "icon_messages.csv"
ICON_LIBRARY_CSV = DATA_DIR / "icon_library.csv"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

SECRET_KEY = "change-this-later"