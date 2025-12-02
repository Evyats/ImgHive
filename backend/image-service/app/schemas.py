from typing import List
from pydantic import BaseModel, Field
from app.enums import Status



class ImageDocument(BaseModel):
    id: str
    created_at: str
    status: Status
    image_file_path: str | None
    thumbnail_file_path: str | None



class GetImagesResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    items: List[ImageDocument]



class UploadImageResponse(BaseModel):
    status: str
    id: str
    creation_time: str
    polling: str


class GetImageStatusResponse(BaseModel):
    image_id: str
    status: Status



class GetImagesRequest(BaseModel):
    status: Status | None = Field(None)
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=20)
    limit: int = Field(10, ge=1, le=20)
