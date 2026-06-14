from botocore.exceptions import ClientError

from app.domain.repositories.file_storage_repository import FileStorageRepository
from app.domain.models.file import FileContent, FileMetadata
from app.infrastructure.aws.boto3_client_factory import AWSClientFactory


class AwsS3StorageService(FileStorageRepository):
    def __init__(self):
        self.client = AWSClientFactory.create("s3")

    def download(self, path: str) -> FileContent:
        bucket, key = self._parse_path(path)

        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
            data = response["Body"].read()

            if not data:
                raise ValueError(f"Empty content for {path}")

            return FileContent(
                data=data,
                name=key.split("/")[-1],
            )

        except ClientError as e:
            raise RuntimeError(f"Failed to download {path}: {e}")

    def delete(self, path: str) -> None:
        bucket, key = self._parse_path(path)

        try:
            self.client.delete_object(Bucket=bucket, Key=key)
        except ClientError as e:
            raise RuntimeError(f"Failed to delete {path}: {e}")

    def get_metadata(self, path: str) -> FileMetadata:
        bucket, key = self._parse_path(path)

        try:
            response = self.client.head_object(Bucket=bucket, Key=key)

            return FileMetadata(
                size=response.get("ContentLength"),
                content_type=response.get("ContentType"),
                extra=response.get("Metadata", {}),
            )

        except ClientError as e:
            raise RuntimeError(f"Failed to get metadata for {path}: {e}")

    def _parse_path(self, path: str) -> tuple[str, str]:
        """
        Espera formato: bucket/key ou bucket/folder/file.ext
        """
        try:
            bucket, key = path.split("/", 1)
            return bucket, key
        except ValueError:
            raise ValueError(f"Invalid path format: {path}")
