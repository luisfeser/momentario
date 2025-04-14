"""Video processing functionality."""
import multiprocessing
import shutil
from pathlib import Path

import ffmpeg

from ..core.media_processor import MediaProcessor

class VideoProcessor(MediaProcessor):
    """Processor for video files with AV1 conversion."""
    
    def __init__(self, date_extractor, original_videos_path: Path):
        super().__init__(date_extractor)
        self.original_videos_path = original_videos_path
        
    def process(self, source_path: Path, dest_base_path: Path) -> Path:
        """
        Process a video file by:
        1. Backing up original to original_videos_path
        2. Converting to AV1 in the organized collection
        
        Args:
            source_path: Path to source video
            dest_base_path: Base path for the organized collection
            
        Returns:
            Path to the processed video in its new location
        """
        date = self.date_extractor.extract_date(source_path)
        dest_path = self._get_destination_path(source_path, dest_base_path, date)
        backup_path = self.original_videos_path / source_path.name
        
        # Ensure directories exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup original
        shutil.copy2(source_path, backup_path)
        
        # Convert to AV1 with good quality settings
        stream = ffmpeg.input(str(source_path))
        stream = ffmpeg.output(
            stream,
            str(dest_path),
            **{
                'c:v': 'libsvtav1',  # Video codec
                'crf': '30',  # Quality (lower = better)
                'preset': '4',  # Speed preset (0-8, higher = faster)
                'threads': str(multiprocessing.cpu_count()),  # Use all available threads
                'c:a': 'libopus'  # Audio codec
            }
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        return dest_path
