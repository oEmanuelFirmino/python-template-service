from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def build_temp_path(prefix: str, date: str, extension: str = "json") -> Path:
    tmp_dir = Path(os.getcwd()) / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    safe_date = date.replace('/', '-').replace('\\', '-')
    timestamp = int(datetime.now().timestamp())

    return tmp_dir / f"{prefix}_{safe_date}_{timestamp}.{extension}"


def cleanup_file(file_path: str | Path) -> None:
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
    except OSError as e:
        logger.error(f"Error deleting temporary file {file_path}: {e}")