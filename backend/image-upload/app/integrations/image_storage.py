from .storage_mock.local_storage import LocalStorage

IMAGE_STORAGE_PATH = "C:/Users/evyat/Desktop/imgur/s3/image-storage"
IMAGE_STORAGE = LocalStorage(IMAGE_STORAGE_PATH)


def save(filename, data):
    IMAGE_STORAGE.save(filename, data)


def open(filename):
    return IMAGE_STORAGE.open(filename)


def delete(filename):
    IMAGE_STORAGE.delete(filename)