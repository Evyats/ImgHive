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
        self.collection.create_index("status")
        self.collection.create_index([("created_at", -1)])

    def close_client(self):
        self.client.close()


    def add_image(self, id, created_at, status, image_file_path, thumbnail_file_path):
        document = {
            "id": id,
            "created_at": created_at,
            "status": status,
            "image_file_path": image_file_path,
            "thumbnail_file_path": thumbnail_file_path,
        }
        self.collection.insert_one(document)

    
    
    def _format_date(self, date):
        return date.strftime("%d/%m/%y %H:%M:%S")
    
    
    def get_images(self, status, page, page_size, limit):

        filter = {"status": status} if status else dict()        
        page_indexed = page - 1
        start_at_index = page_indexed * page_size
        
        cursor = (
            self.collection
            .find(filter, {"_id": 0})
            .sort("created_at", -1)
            .skip(start_at_index)
            .limit(min(page_size, limit))
        )

        documents = list(cursor)
        for document in documents:
            document["created_at"] = self._format_date(document["created_at"])
        return documents
    

    
    def size(self, status):
        filter = {"status": status} if status else dict()        
        num_documents = self.collection.count_documents(filter)
        return num_documents



    def get_image(self, id):
        document = self.collection.find_one({"id": id}, {"_id": 0})
        if document: document["created_at"] = self._format_date(document["created_at"])
        return document
    


    def id_exists(self, id):
        id_occurences = self.collection.count_documents({"id": id})
        return id_occurences > 0
    

    def get_image_path(self, id):
        document = self.collection.find_one({"id": id})
        if document: return document["image_file_path"]
        return None

    def get_thumbnail_path(self, id):
        document = self.collection.find_one({"id": id})
        if document: return document["thumbnail_file_path"]
        return None



def test_add_document():
    some_new_id = "a32835"
    col = MongoCollection("localhost:27017", "imgur_clone_db_1", "images")
    col.add_image(some_new_id, datetime.now(timezone.utc), "queued", "some/image/path", "some/thumbnail/path")
    print(col.get_images(5))
    print(col.get_image(some_new_id))
    print(col.get_image("a326"))



def main():
    pass
    # test_add_document()
    col = MongoCollection("localhost:27017", "imgur_clone_db_1", "images")
    print(col.get_image("01KATEWNVJDR1FWC7X6NYVW5MJ"))
    


if __name__ == "__main__": main()