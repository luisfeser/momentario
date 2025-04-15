"""Photo processing functionality."""
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..core.media_processor import MediaProcessor, DateExtractor

class PhotoProcessor(MediaProcessor):
    """Processor for photo files."""
    
    def _calculate_md5(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file."""
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def _get_unique_destination_path(self, dest_path: Path) -> Path:
        """Get a unique destination path by appending a number if needed."""
        if not dest_path.exists():
            return dest_path

        stem = dest_path.stem
        suffix = dest_path.suffix
        parent = dest_path.parent
        counter = 1

        while True:
            new_path = parent / f"{stem}-{counter}{suffix}"
            if not new_path.exists():
                return new_path
            counter += 1

    def process(self, source_path: Path, dest_base_path: Path) -> Path:
        """
        Process a photo file by moving it to the appropriate destination.
        Handles duplicate files by comparing MD5 hashes.
        
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
        
        if dest_path.exists():
            # Calculate MD5 hashes
            source_md5 = self._calculate_md5(source_path)
            dest_md5 = self._calculate_md5(dest_path)
            
            if source_md5 == dest_md5:
                # Files are identical, overwrite the destination
                shutil.move(source_path, dest_path)
            else:
                # Files are different, find a unique name
                dest_path = self._get_unique_destination_path(dest_path)
                shutil.move(source_path, dest_path)
        else:
            # No existing file, simple move
            shutil.move(source_path, dest_path)
        
        # Set file dates based on extracted date
        self._set_file_dates(dest_path, date)
        
        return dest_path
