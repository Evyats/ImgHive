from datetime import datetime, timezone
from pymongo import MongoClient


class MongoCollection:
    '''
    - SCHEMA
    id (str) (unique, indexed)
    created_at (datetime)
    status (str) (queued, processing, failed, done)
    image_file_path (str)
    thumbnail_file_path (str)
    '''

    def __init__(self, ip, db_name, collection_name):
        self.client = MongoClient(f"mongodb://{ip}")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("id", unique=True)

    def close_client(self):
        self.client.close()

    def id_exists(self, id):
        id_occurences = self.collection.count_documents({"id": id})
        return id_occurences > 0

    def update_status(self, id, status):
        self.collection.update_one({"id": id}, {"$set": {"status": status}})


    def update_image_file_path(self, id, path):
        self.collection.update_one({"id": id}, {"$set": {"image_file_path": path}})


    def update_thumbnail_file_path(self, id, path):
        self.collection.update_one({"id": id}, {"$set": {"thumbnail_file_path": path}})






def test_add_image():
    pass
    some_new_id = "a5419"
    col = MongoCollection("localhost:27017", "imgur_clone_db_1", "images")
    col.add_image(some_new_id, datetime.now(timezone.utc), "queued", "some/image/path", "some/thumbnail/path")
    print(col.get_images(5))
    print(col.get_image(some_new_id))
    print(col.get_image("a326"))

def test_id_doesnt_exists():
    col = MongoCollection("localhost:27017", "imgur_clone_db_1", "images")
    print(col.id_exists("dshiu"))
    col.update_image_file_path("dshiu","jskdf")

def main():
    pass
    # test_add_image()
    # test_id_doesnt_exists()

if __name__ == "__main__": main()