from logging import info
import sys
from google.cloud import storage


def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents, predefined_acl="publicRead")
    info(f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}.")


if __name__ == "__main__":
    upload_blob_from_memory(
        bucket_name=sys.argv[1],
        contents=sys.argv[2],
        destination_blob_name=sys.argv[3],
    )
