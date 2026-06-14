from pathlib import Path


class LocalFileStorage:
    def __init__(self, base_path: str = "/tmp"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, data: bytes) -> str:
        file_path = self.base_path / filename

        with open(file_path, "wb") as f:
            f.write(data)

        return str(file_path)
