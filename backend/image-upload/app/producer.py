from contextlib import asynccontextmanager
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.integrations.image_db import MongoCollection
from . import config
from . import schemas
from .integrations.storage import LocalStorage
from . import consumer



MAX_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_TYPES = {"image/jpeg", "image/png"}

settings = None
temp_storage = None
mongo = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global settings, temp_storage, mongo
    print("Runs once on startup")
    settings = config.getSettings()
    temp_storage = LocalStorage(settings.TEMP_STORAGE_PATH)
    mongo = MongoCollection(
        settings.IMAGE_DB_IP,
        settings.IMAGE_DB_DB_NAME,
        settings.IMAGE_DB_COLLECTION_NAME,
    )
    yield
    print("Runs once on shutdown")
    mongo.close_client()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] while dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# / health

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "image-upload"}




# / api / images

@app.post("/api/images/{id}/file", response_model=schemas.EnqueueImageResponse)
async def enqueue_image(id: str, file: UploadFile = File(...)):

    if not mongo.id_exists(id): raise HTTPException(404, detail="the image id doesnt exists in the db")
    if file.content_type not in ALLOWED_TYPES: raise HTTPException(400, "Invalid file type (must be an image)")
    data = await file.read()
    if len(data) > MAX_SIZE: raise HTTPException(413, "File too large")

    filename = f"{id}_RAW"
    temp_storage.save(filename, data)
    consumer.process_image.delay(filename, id)

    return schemas.EnqueueImageResponse(
        status="enqueued successfully",
        image_id=id
    )
