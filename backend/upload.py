import gzip
from logging import info
import sys
from typing import Optional
from google.cloud import storage
from google.cloud.storage.blob import os


def upload_blob_from_memory(
    bucket_name,
    destination_blob_name,
    content_type: str = "text/plain",
    gzip_data: bytes = b"",
    text_data: str = "",
):
    """Uploads a file to the bucket."""
    data = None
    if gzip_data:
        data = gzip_data
    elif text_data:
        data = gzip.compress(text_data.encode())
    else:
        raise Exception("either gzip_data or text_data should be present.")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.content_encoding = "gzip"
    blob.upload_from_string(
        data,
        predefined_acl="publicRead",
        content_type=content_type,
    )
    blob.metadata = {"Access-Control-Allow-Origin": os.environ["ACCESS_CONTROL_ORIGIN"]}
    info(
        f"{destination_blob_name} with contents {text_data} uploaded to {bucket_name}."
    )


if __name__ == "__main__":
    print(sys.argv)
    upload_blob_from_memory(
        bucket_name=sys.argv[1],
        text_data=sys.argv[2],
        destination_blob_name=sys.argv[3],
        content_type=sys.argv[4],
    )
