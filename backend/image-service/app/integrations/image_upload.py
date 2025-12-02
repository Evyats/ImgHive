import requests




class ImageUpload():
# (url always first), headers, params, json, timeout, files

    def __init__(self, ip):
        self.ip = ip
        self.url = f"http://{self.ip}"


    def health_check(self):
        endpoint = "/health"
        response = requests.get(
            f"{self.url}{endpoint}"
        )
        response.raise_for_status()
        return response

    def enqueue_image(self, id, file, filename, filetype):
        endpoint = f"/api/images/{id}/file"
        files = {"file": (filename, file, filetype)}
        response = requests.post(
            f"{self.url}{endpoint}", files=files
        )
        response.raise_for_status()
        return response
        