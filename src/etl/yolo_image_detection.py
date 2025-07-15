import os
import torch
from psycopg2.extras import execute_values
import psycopg2
from ultralytics import YOLO
from PIL import Image

# Monkey patch PyTorch to avoid safe-unpickling errors
orig_load = torch.load


def patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return orig_load(*args, **kwargs)


torch.load = patched_load

model = YOLO("yolov8n.pt")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "telegram_dw")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def is_image(path):
    """
    Check if the file is a valid image (not a disguised video or corrupt file).
    """
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def detect_objects(image_path):
    results = model(image_path)
    detections = []
    for result in results:
        for box in result.boxes.data.tolist():
            confidence = box[4]
            class_id = int(box[5])
            class_name = model.names[class_id]
            detections.append((class_name, confidence))
    return detections


def batch(iterable, n=1):
    length = len(iterable)
    for ndx in range(0, length, n):
        yield iterable[ndx : min(ndx + n, length)]


images_dir = "data/raw/telegram_images/2025-07-13"


def main():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    records_to_insert = []

    for root, _, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".png")):
                image_path = os.path.join(root, file)

                # ✅ Check if the file is a real image
                if not is_image(image_path):
                    print(f"❌ Skipping non-image file: {image_path}")
                    continue

                message_id_str = os.path.splitext(file)[0]
                try:
                    message_id = int(message_id_str)
                except ValueError:
                    print(f"Skipping file with non-numeric message_id: {file}")
                    continue

                detections = detect_objects(image_path)

                for detected_class, confidence_score in detections:
                    records_to_insert.append(
                        (message_id, detected_class, confidence_score)
                    )

    insert_sql = (
        "INSERT INTO public.fct_image_detections "
        "(message_id, detected_object_class, confidence_score) "
        "VALUES %s "
        "ON CONFLICT (message_id, detected_object_class) DO NOTHING"
    )

    if records_to_insert:
        for chunk in batch(records_to_insert, 1000):
            execute_values(cur, insert_sql, chunk)
        conn.commit()
        print(f"Inserted {len(records_to_insert)} image detection records.")
    else:
        print("No detections to insert.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
