"""Photo processing functionality."""
import shutil
from pathlib import Path
from typing import Optional

from ..core.media_processor import MediaProcessor, DateExtractor

class PhotoProcessor(MediaProcessor):
    """Processor for photo files."""
    
    async def process(self, source_path: Path, dest_base_path: Path) -> Path:
        """
        Process a photo file by copying it to the appropriate destination.
        
        Args:
            source_path: Path to source photo
            dest_base_path: Base path for the organized collection
            
        Returns:
            Path to the processed photo in its new location
        """
        date = self.date_extractor.extract_date(source_path)
        dest_path = self._get_destination_path(source_path, dest_base_path, date)
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file preserving metadata
        shutil.copy2(source_path, dest_path)
        
        return dest_path
