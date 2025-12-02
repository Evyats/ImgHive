import os
from celery import Celery
import time

from . import config
from .integrations.storage import LocalStorage
from PIL import Image
from io import BytesIO
from datetime import datetime, timezone
from .integrations.image_db import MongoCollection


settings = config.getSettings()
mongo = MongoCollection(settings.IMAGE_DB_IP, settings.IMAGE_DB_DB_NAME, settings.IMAGE_DB_COLLECTION_NAME)
temp_storage = LocalStorage(settings.TEMP_STORAGE_PATH)
image_storage = LocalStorage(settings.IMAGE_STORAGE_PATH)


app = Celery(
    "worker",
    broker=f"redis://{settings.REDIS_QUEUE_IP}/0",
    backend=f"redis://{settings.REDIS_QUEUE_IP}/1"
)



@app.task
def add(x, y):
    print(f"Running add({x}, {y})")
    time.sleep(1)
    return x + y



@app.task
def process_image(filename, id):

    time.sleep(settings.CONSUMER_DELAY_BEFORE_PROCESSING)
    mongo.update_status(id, "processing")

    MAX_SIZE = 2048
    THUMBNAIL_SIZE = 256

    image_bytes = temp_storage.open(filename)
    resized_image_bytes = limit_aspect_ratio(image_bytes, MAX_SIZE, MAX_SIZE, 90)
    thumbnail_image_bytes = limit_aspect_ratio(image_bytes, THUMBNAIL_SIZE, THUMBNAIL_SIZE, 80)

    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    original_path = os.path.join(day, "original", f"{id}_ORIGINAL.jpg")
    thumbnail_path = os.path.join(day, "thumbnail", f"{id}_THUMBNAIL.jpg")
    image_storage.save(original_path, resized_image_bytes)
    image_storage.save(thumbnail_path, thumbnail_image_bytes)

    temp_storage.delete(filename)

    mongo.update_image_file_path(id, original_path)
    mongo.update_thumbnail_file_path(id, thumbnail_path)

    time.sleep(settings.CONSUMER_DELAY_BEFORE_DONE)
    mongo.update_status(id, "done")
    
    print(f"Finished task for file id: {id}")




def limit_aspect_ratio(image_bytes, max_width, max_height, quality):
    pil_image = Image.open(BytesIO(image_bytes))

    max_ratio = (max_width, max_height)
    pil_image.thumbnail(max_ratio)

    # drop alpha for JPEG:
    if pil_image.mode in ("RGBA", "LA"): pil_image = pil_image.convert("RGB")

    resized_buffer = BytesIO()
    pil_image.save(resized_buffer, format="JPEG", quality=quality)

    resized_bytes = resized_buffer.getvalue()
    return resized_bytes
