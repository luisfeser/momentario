"""Date extraction utilities."""
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import exifread
from dateutil import parser

class MediaDateExtractor:
    """Extracts dates from media files using multiple strategies."""
    
    def extract_date(self, file_path: Path) -> Optional[datetime]:
        """
        Extract date from a media file using multiple strategies:
        1. EXIF metadata
        2. Filename patterns
        
        Args:
            file_path: Path to the media file
            
        Returns:
            Extracted datetime or None if no date could be found
        """
        # Try EXIF first
        date = self._extract_from_exif(file_path)
        if date:
            return date
            
        # Fall back to filename
        return self._extract_from_filename(file_path)
    
    def _extract_from_exif(self, file_path: Path) -> Optional[datetime]:
        """Extract date from EXIF metadata."""
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
                
            if 'EXIF DateTimeOriginal' in tags:
                return datetime.strptime(str(tags['EXIF DateTimeOriginal']), 
                                      '%Y:%m:%d %H:%M:%S')
        except Exception:
            return None
            
        return None
    
    def _extract_from_filename(self, file_path: Path) -> Optional[datetime]:
        """Extract date from filename using common patterns."""
        patterns = [
            r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})',  # YYYY-MM-DD, YYYYMMDD
            r'(\d{2})[-_]?(\d{2})[-_]?(\d{4})',  # DD-MM-YYYY, DDMMYYYY
        ]
        
        name = file_path.stem
        
        for pattern in patterns:
            match = re.search(pattern, name)
            if match:
                try:
                    # Try to parse the matched date
                    date_str = ' '.join(match.groups())
                    return parser.parse(date_str)
                except ValueError:
                    continue
                    
        return None
