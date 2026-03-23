"""JSON file I/O abstraction for persisting data to disk."""

import json
from pathlib import Path
from typing import Any


class JSONFileIO:
    """Handles loading and persisting data to a JSON file on disk.

    Attributes:
        _data_path: Path to a persistence file on disk.
    """

    _data_path: Path

    def __init__(self, data_path: Path):
        """Initialize the JSON file I/O handler.

        Args:
            data_path: Path for persisted storage on disk.
        """
        self._data_path = data_path

    def load(self) -> Any:
        """Load persisted data from disk if data path exists.

        Returns:
            Data loaded from the file, or None if no data file exists.
        """
        if not self._data_path.exists():
            return None

        with self._data_path.open("r") as f:
            data = json.load(f)

        return data

    def persist(self, data: Any) -> None:
        """Persist data to disk as JSON (non-atomic).

        Ensures the parent directory exists and writes JSON directly to the target file.
        This approach may risk partial/corrupt files if the process crashes during write.

        (If you would like a challenge, try implementing an atomic write. First,
        create a temporary file, flush it and fsync it, then atomically replace
        the target file with the temporary file.)

        Args:
            data: Data to persist to the file.
        """
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        with self._data_path.open("w") as f:
            json.dump(data, f)
