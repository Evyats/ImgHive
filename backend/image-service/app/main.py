from contextlib import asynccontextmanager
import math
from fastapi import Depends, FastAPI, File, HTTPException, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests
from . import config, schemas
from .integrations.image_db import MongoCollection
from .integrations.image_upload import ImageUpload
from .integrations.storage import LocalStorage
from datetime import datetime, timezone
import ulid
from pathlib import PurePosixPath



settings = None
mongo = None
image_upload = None
image_storage = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global settings, mongo, image_upload, image_storage
    print("Runs once on startup")
    settings = config.getSettings()
    mongo = MongoCollection(
        settings.IMAGE_DB_IP,
        settings.IMAGE_DB_DB_NAME,
        settings.IMAGE_DB_COLLECTION_NAME,
    )
    image_upload = ImageUpload(settings.IMAGE_UPLOAD_IP)
    image_storage = LocalStorage(settings.IMAGE_STORAGE_PATH)
    yield
    print("Runs once on shutdown")
    mongo.close_client()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def middleware(request: Request, call_next):
    """logging the whole request:
    body = await request.body()
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Body: {body.decode(errors='ignore')}")
    """
    response = await call_next(request)
    return response





# / health

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "image-service"}

@app.get("/integrations_health")
async def integrations_health_check():
    integrations_tested = ["image-upload service"]
    try:
        response = image_upload.health_check()
    except requests.HTTPError as error:
        raise HTTPException(status_code=error.response.status_code, detail=error.response.text)
    except requests.exceptions.ConnectionError as error:
        raise HTTPException(status_code=503, detail="service unreachable")
    return {"status": "healthy", "integrations tested": integrations_tested}





# / api / images

@app.get("/api/images", response_model=schemas.GetImagesResponse)
async def get_images(params: schemas.GetImagesRequest = Depends()):
    documents = mongo.get_images(params.status, params.page, params.page_size, params.limit)
    num_documents = mongo.size(params.status)
    num_pages = math.ceil(num_documents / params.page_size)
    return {
        "items": documents,
        "page": params.page,
        "page_size": params.page_size,
        "total_items": num_documents,
        "total_pages": num_pages,
    }

@app.post("/api/images", response_model=schemas.UploadImageResponse)
async def upload_image(file: UploadFile = File(...)):
    id = generate_id()
    time = datetime.now(timezone.utc)
    time_formatted = time.strftime("%d/%m/%y %H:%M:%S")
    mongo.add_image(id, time, "queued", None, None)

    data = await file.read()
    filename = file.filename
    filetype = file.content_type
    try:
        response = image_upload.enqueue_image(id, data, filename, filetype)
    except requests.HTTPError as error:
        raise HTTPException(status_code=error.response.status_code, detail=error.response.text)

    return {
        "status": "image upload added to queue",
        "id": id,
        "creation_time": time_formatted,
        "polling": f"/api/images/{id}/status",
    }


def generate_id():
    uid = str(ulid.new())
    while mongo.id_exists(uid):
        uid = str(ulid.new())
    return uid




# / api / images / {id}

@app.get("/api/images/{id}", response_model=schemas.ImageDocument)
async def get_image(id: str):
    document = mongo.get_image(id)
    if not document: raise HTTPException(status_code=404, detail="image id doesn't exists")
    return document

@app.get("/api/images/{id}/status", response_model=schemas.GetImageStatusResponse)
async def get_image_status(id: str):
    document = await get_image(id)
    return {"image_id": id, "status": document["status"]}

@app.get("/api/images/{id}/image_file")
async def download_image(id: str):
    raw = mongo.get_image_path(id)
    image_path = str(PurePosixPath(raw.replace("\\", "/")))
    image_bytes = image_storage.open(image_path)
    return Response(content=image_bytes, media_type="image/jpeg")

@app.get("/api/images/{id}/thumbnail_file")
async def download_thumbnail(id: str):
    raw = mongo.get_thumbnail_path(id)
    thumbnail_path = str(PurePosixPath(raw.replace("\\", "/")))
    print(thumbnail_path)
    image_bytes = image_storage.open(thumbnail_path)
    return Response(content=image_bytes, media_type="image/jpeg")
