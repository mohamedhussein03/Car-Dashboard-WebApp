from pathlib import Path

import cv2

from config import CLASSES_PATH, MODEL_PATH


_model = None
_class_names = []


def load_class_names():
    global _class_names

    if _class_names:
        return _class_names

    classes_file = Path(CLASSES_PATH)

    if not classes_file.exists():
        raise FileNotFoundError(f"Classes file not found: {classes_file}")

    with classes_file.open("r", encoding="utf-8") as file:
        _class_names = [line.strip() for line in file if line.strip()]

    return _class_names





def draw_detections(image, detections):
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection["bbox"])
        class_name = detection["class_name"]
        confidence = detection["confidence"]

        label = f"{class_name} {confidence:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(image, (x1, max(y1 - 30, 0)), (x2, y1), (0, 255, 0), -1)
        cv2.putText(
            image,
            label,
            (x1, max(y1 - 8, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

    return image


def run_detection(image_path, conf_threshold=0.25):
    from app import MODEL

    if MODEL is None:
        raise RuntimeError("YOLO model was not initialized at startup.")

    class_names = load_class_names()

    results = MODEL.predict(
    source=image_path,
    conf=0.33,
    imgsz=640,
    max_det=20,
    device="cpu",
    verbose=True,
    )   

    detections = []

    print("YOLO results:", results, flush=True)

    for result in results:
        print("Boxes:", result.boxes, flush=True)

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            xyxy = box.xyxy[0].tolist()

            class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"

            detections.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": round(confidence, 4),
                "bbox": [round(value, 2) for value in xyxy],
            })

    return detections

def save_annotated_image(image_path, detections, output_path):
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("Could not read image for annotation.")

    annotated_image = draw_detections(image, detections)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    success = cv2.imwrite(str(output_file), annotated_image)

    if not success:
        raise ValueError("Could not save annotated image.")

    return output_file
