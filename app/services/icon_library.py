import csv
from pathlib import Path

from flask import session

from config import ICON_LIBRARY_CSV
from app.services.message_service import get_icon_message


def load_icon_library():
    csv_path = Path(ICON_LIBRARY_CSV)

    if not csv_path.exists():
        raise FileNotFoundError(f"Icon library CSV not found: {csv_path}")

    icons = []
    language = session.get("language", "en")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            class_name = row["class_name"].strip()
            message_data = get_icon_message(class_name)

            display_name = row["display_name"].strip()
            display_name_ar = row.get("display_name_ar", "").strip()

            if language == "ar" and display_name_ar:
                display_name = display_name_ar

            icons.append({
                "class_name": class_name,
                "display_name": display_name,
                "icon_filename": row["icon_filename"].strip(),
                "category": row.get("category", "supported").strip().lower(),
                "message": message_data["message"],
                "action": message_data["action"],
            })

    return icons