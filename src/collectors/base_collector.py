
from abc import ABC, abstractmethod
from pathlib import Path


class BaseCollector(ABC):
    """Base class for all data collectors."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    @abstractmethod
    def collect(self):
        """Collect raw listing data."""
        pass
