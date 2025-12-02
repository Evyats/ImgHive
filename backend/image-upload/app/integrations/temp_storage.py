from .storage_mock.local_storage import LocalStorage

TEMP_STORAGE_PATH = "C:/Users/evyat/Desktop/imgur/s3/temp-storage"
TEMP_STORAGE = LocalStorage(TEMP_STORAGE_PATH)


def save(filename, data):
    TEMP_STORAGE.save(filename, data)


def open(filename):
    return TEMP_STORAGE.open(filename)


def delete(filename):
    TEMP_STORAGE.delete(filename)