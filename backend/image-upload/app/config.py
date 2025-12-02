import os
from dotenv import load_dotenv


load_dotenv()



class Settings:
    REDIS_QUEUE_IP: str
    IMAGE_DB_IP: str
    IMAGE_DB_DB_NAME: str
    IMAGE_DB_COLLECTION_NAME: str
    CONSUMER_DELAY_BEFORE_PROCESSING: int
    CONSUMER_DELAY_BEFORE_DONE: int
    IMAGE_STORAGE_PATH: str
    TEMP_STORAGE_PATH: str




def getSettings():
    settings = Settings()
    settings.REDIS_QUEUE_IP = os.getenv("REDIS_QUEUE_IP")
    settings.IMAGE_DB_IP = os.getenv("IMAGE_DB_IP")
    settings.IMAGE_DB_DB_NAME = os.getenv("IMAGE_DB_DB_NAME")
    settings.IMAGE_DB_COLLECTION_NAME = os.getenv("IMAGE_DB_COLLECTION_NAME")
    settings.CONSUMER_DELAY_BEFORE_PROCESSING = int(os.getenv("CONSUMER_DELAY_BEFORE_PROCESSING"))
    settings.CONSUMER_DELAY_BEFORE_DONE = int(os.getenv("CONSUMER_DELAY_BEFORE_DONE"))
    settings.IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH")
    settings.TEMP_STORAGE_PATH = os.getenv("TEMP_STORAGE_PATH")
    return settings