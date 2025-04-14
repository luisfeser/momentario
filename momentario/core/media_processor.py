"""Core media processing functionality."""
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional, Protocol

class DateExtractor(Protocol):
    """Protocol for date extraction from media files."""
    
    def extract_date(self, file_path: Path) -> Optional[datetime]:
        """Extract date from a media file."""
        ...

class MediaProcessor(ABC):
    """Base class for media processors."""
    
    def __init__(self, date_extractor: DateExtractor):
        self.date_extractor = date_extractor
        
    @abstractmethod
    def process(self, source_path: Path, dest_base_path: Path) -> Path:
        """Process a media file and return the destination path."""
        pass
    
    def _get_destination_path(self, source_path: Path, dest_base_path: Path, 
                            date: Optional[datetime]) -> Path:
        """Calculate destination path based on date."""
        if not date:
            return dest_base_path / "SIN_FECHA" / source_path.name
            
        return dest_base_path / str(date.year) / f"{date.month:02d}" / source_path.name
