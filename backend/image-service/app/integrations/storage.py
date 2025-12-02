from abc import ABC, abstractmethod
import os


class Storage(ABC):
    @abstractmethod
    def save(self, filename: str, data: bytes) -> None: pass

    @abstractmethod
    def open(self, filename: str) -> bytes: pass

    @abstractmethod
    def delete(self, filename: str) -> None: pass



class LocalStorage(Storage):
    def __init__(self, base_path):
        self.base_path = base_path
    
    def _full_path(self, filename):
        full_path = os.path.join(self.base_path, filename)
        return full_path

    def save(self, filename, data):
        path = self._full_path(filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            file.write(data)

    def open(self, filename):
        path = self._full_path(filename)
        with open(path, "rb") as file:
            data = file.read()
        return data

    def delete(self, filename):
        path = self._full_path(filename)
        os.remove(path)
