import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")

class StorageClass():

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(BUCKET_NAME)

    def upload(self, data, destination_blob_name):

        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(data)

        print(
        "File uploaded to {}.".format(
               destination_blob_name
        ))

    def uploadFromFile(self, source_file_name, destination_blob_name):

        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source)

        print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        ))


    def load(self, source_blob_name):
        
        blob = self.bucket.blob(source_blob_name)
        
        return blob.download_as_string()



Storage = StorageClass()

