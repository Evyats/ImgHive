from pydantic import BaseModel


class EnqueueImageResponse(BaseModel):
    status: str
    image_id: str