from pathlib import Path
from uuid import uuid4


def generate_output_filename(original_filename, prefix="result"):
    original_path = Path(original_filename)
    stem = original_path.stem
    suffix = original_path.suffix or ".jpg"
    unique_id = uuid4().hex[:8]

    return f"{prefix}_{stem}_{unique_id}{suffix}"