import csv
from pathlib import Path
from flask import session

from config import ICON_MESSAGES_CSV, ICON_LIBRARY_CSV


def get_language():
    return session.get("language", "en")


def load_icon_messages():
    csv_path = Path(ICON_MESSAGES_CSV)

    if not csv_path.exists():
        raise FileNotFoundError(f"Icon messages CSV not found: {csv_path}")

    messages = {}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            class_name = row["class_name"].strip()

            messages[class_name] = {
                "class_name": class_name,
                "display_name": row["display_name"].strip(),
                "display_name_ar": row.get("display_name_ar", "").strip(),
                "message": row["message"].strip(),
                "message_ar": row.get("message_ar", "").strip(),
                "action": row["action"].strip(),
                "action_ar": row.get("action_ar", "").strip(),
            }

    return messages


def load_icon_filename_map():
    csv_path = Path(ICON_LIBRARY_CSV)

    if not csv_path.exists():
        raise FileNotFoundError(f"Icon library CSV not found: {csv_path}")

    icon_map = {}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            class_name = row["class_name"].strip()
            icon_map[class_name] = row["icon_filename"].strip()

    return icon_map


def get_icon_message(class_name):
    messages = load_icon_messages()
    language = get_language()

    default_display = class_name.replace("_", " ").strip()

    data = messages.get(
        class_name,
        {
            "class_name": class_name,
            "display_name": default_display,
            "display_name_ar": "",
            "message": "This dashboard icon was detected.",
            "message_ar": "تم اكتشاف رمز في لوحة القيادة.",
            "action": "Check your vehicle manual or inspect the car for more details.",
            "action_ar": "راجع دليل السيارة أو افحص السيارة لمزيد من التفاصيل.",
        },
    )

    if language == "ar":
        return {
            "class_name": class_name,
            "display_name": data.get("display_name_ar") or data["display_name"],
            "message": data.get("message_ar") or data["message"],
            "action": data.get("action_ar") or data["action"],
        }

    return {
        "class_name": class_name,
        "display_name": data["display_name"],
        "message": data["message"],
        "action": data["action"],
    }


def attach_messages_to_detections(detections):
    enriched_detections = []
    icon_filename_map = load_icon_filename_map()

    for detection in detections:
        message_data = get_icon_message(detection["class_name"])

        enriched_detection = {
            **detection,
            "display_name": message_data["display_name"],
            "message": message_data["message"],
            "action": message_data["action"],
            "icon_filename": icon_filename_map.get(detection["class_name"]),
        }

        enriched_detections.append(enriched_detection)

    return enriched_detections