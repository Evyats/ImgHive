import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    IMAGE_UPLOAD_IP: str
    IMAGE_DB_IP: str
    IMAGE_DB_DB_NAME: str
    IMAGE_DB_COLLECTION_NAME: str
    IMAGE_STORAGE_PATH: str



def getSettings():
    settings = Settings()
    settings.IMAGE_UPLOAD_IP = os.getenv("IMAGE_UPLOAD_IP")
    settings.IMAGE_DB_IP = os.getenv("IMAGE_DB_IP")
    settings.IMAGE_DB_DB_NAME = os.getenv("IMAGE_DB_DB_NAME")
    settings.IMAGE_DB_COLLECTION_NAME = os.getenv("IMAGE_DB_COLLECTION_NAME")
    settings.IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH")
    return settings


if __name__ == "__main__":
    pass
    settings = getSettings()
    print(settings.IMAGE_UPLOAD_IP)
