from typing import List
import boto3

from FileManager.RemoteManagerABC import RemoteManagerABC


class BackBlazeManager(RemoteManagerABC):
    """
    BackBlaze B2 implementation of RemoteManager using the S3-compatible API.
    """

    def __init__(self, endpoint_url: str, access_key_id: str, secret_access_key: str, bucket_name: str):
        """Init the file system. Probably need authentication args."""
        self.s3 = boto3.resource(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self.bucket = self.s3.Bucket(bucket_name)

    def _exists_sync(self, file_name: str) -> bool:
        """Return a bool if the file exists. Do not raise errors."""
        objects = list(self.bucket.objects.filter(Prefix=file_name))
        return any(obj.key == file_name for obj in objects)

    def _read_sync(self, file_name: str) -> str:
        """Returns the entire file's contents as a string."""
        obj = self.bucket.Object(file_name)
        return obj.get()['Body'].read().decode('utf-8')

    def _create_sync(self, file_name: str) -> None:
        """Creates a file with the name "file_name" """
        self.bucket.put_object(Key=file_name, Body=b'')

    def _write_sync(self, file_name: str, file_contents: str) -> None:
        """Writes to a file that is already created. DO NOT CREATE A FILE IN THIS IMPLEMENTATION."""
        self.bucket.Object(file_name).put(Body=file_contents.encode('utf-8'))

    def _delete_sync(self, file_name: str) -> None:
        """Deletes an already-made file."""
        self.bucket.Object(file_name).delete()

    def _list_files_sync(self) -> List[str]:
        """Lists all files as names in strings."""
        return [obj.key for obj in self.bucket.objects.all()]
