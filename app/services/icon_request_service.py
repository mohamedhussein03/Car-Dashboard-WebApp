import csv
from datetime import datetime
from pathlib import Path

from werkzeug.utils import secure_filename

from config import ICON_REQUESTS_CSV, SUGGESTIONS_FOLDER


def save_icon_request(name, email, icon_name, notes, image_file=None):
    csv_path = Path(ICON_REQUESTS_CSV)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    image_filename = ""

    if image_file and image_file.filename:
        safe_name = secure_filename(image_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{timestamp}_{safe_name}"
        image_path = Path(SUGGESTIONS_FOLDER) / image_filename
        image_file.save(image_path)

    row = {
        "name": name.strip(),
        "email": email.strip(),
        "icon_name": icon_name.strip() if icon_name else "",
        "image_filename": image_filename,
        "notes": notes.strip() if notes else "",
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    file_exists = csv_path.exists()

    with csv_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "name",
                "email",
                "icon_name",
                "image_filename",
                "notes",
                "submitted_at",
            ],
        )

        if not file_exists or csv_path.stat().st_size == 0:
            writer.writeheader()

        writer.writerow(row)