# Imports the Google Cloud client library
from google.cloud import storage
from dotenv import load_dotenv
import urllib.request
from PIL import Image
from io import BytesIO
import requests
from nudenet import NudeDetector, NudeClassifier
import numpy as np

load_dotenv()

def create_bucket_class_location(bucket_name):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def upload_blob(bucket_name, source_file_name, destination_blob_name, content_type):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    image = source_file_name
    if not isinstance(source_file_name, bytes):
      print("NOT A BYTE IMAGE")
      file = requests.get(source_file_name)
      image = file.content
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # blob.upload_from_filename(source_file_name)
    blob.upload_from_string(image, content_type=content_type)

    # print(
    #     "File {} uploaded to {}.".format(
    #         source_file_name, destination_blob_name
    #     )
    # )

def download_blob(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    byte_data = blob.download_as_bytes()

    print(
        "Downloaded storage object {} from bucket {}.".format(
            source_blob_name, bucket_name
        )
    )
    return byte_data

if __name__ == "__main__":
  # THIS IS JUST FOR TESTING

  # create_bucket_class_location("image_paths") -> already created the bucket at image_paths
  bucket_name = "image_paths"
  byte_image =  requests.get("https://i.pinimg.com/564x/da/16/e9/da16e9a548b5bf5de60dc49c5e4c7395.jpg").content
  # source_file_name = "https://i.pinimg.com/564x/8f/46/7e/8f467e23d45c75fca9d7aa0ea4e20545.jpg"
  source_file_name = byte_image
  # source_file_name = "./cat.png"
  destination_blob_name = "nsfw"
  content_type = "image/png"
  upload_blob(bucket_name, source_file_name, destination_blob_name, content_type)

  result = download_blob(bucket_name, "sfw_image")
  img =  Image.open(BytesIO(result))
  img.save("sfw-bytes.png")

  # nude net code 
  # detector = NudeDetector() # detector = NudeDetector('base') for the "base" version of detector.
  # classifier = NudeClassifier()

  # # Detect single image
  # file = requests.get(source_file_name)
  # img =  Image.open(BytesIO(file.content))
  # result = classifier.classify(np.array(img))
  # img1 = Image.open(BytesIO(file.content))
  # print(result)