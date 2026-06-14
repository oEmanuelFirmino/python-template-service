from app.domain.repositories.file_storage_repository import FileStorageRepository
from app.domain.models.file import FileMetadata
from app.infrastructure.storage.local_file_storage import LocalFileStorage


class FileService:
    def __init__(
        self,
        storage: FileStorageRepository,
        file_storage: LocalFileStorage,
    ):
        self.storage = storage
        self.file_storage = file_storage

    def download_file(self, path: str) -> str:
        file = self.storage.download(path)

        local_path = self.file_storage.save(file.name, file.data)

        return local_path

    def delete_file(self, path: str) -> None:
        self.storage.delete(path)

    def get_metadata(self, path: str) -> FileMetadata:
        return self.storage.get_metadata(path)
