import logging
import boto3

logging = logging.getLogger(__name__)


class StorageAdapter:
    def __init__(self, access_id, secret_key) -> None:
        super().__init__()
        self.s3 = boto3.client('s3',
                                 endpoint_url='https://s3.us-west-1.wasabisys.com',
                                 aws_access_key_id=access_id,
                                 aws_secret_access_key=secret_key
                                 )

    def download(self, bucket_name, path, path_to_save):
        try:
            self.s3.download_file(bucket_name, path, path_to_save)
        except Exception as e:
            raise Exception(f"Error downloading data: {e}")

