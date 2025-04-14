"""Command line interface for Momentario."""
import asyncio
import mimetypes
from pathlib import Path
from typing import List

from .core.media_processor import MediaProcessor
from .photo.photo_processor import PhotoProcessor
from .utils.date_extractor import MediaDateExtractor
from .video.video_processor import VideoProcessor

async def process_media_files(
    source_dir: Path,
    dest_dir: Path,
    original_videos_dir: Path
) -> None:
    """Process all media files in the source directory."""
    date_extractor = MediaDateExtractor()
    photo_processor = PhotoProcessor(date_extractor)
    video_processor = VideoProcessor(date_extractor, original_videos_dir)
    
    # Get all files recursively
    files = [f for f in source_dir.rglob('*') if f.is_file()]
    
    for file in files:
        mime_type, _ = mimetypes.guess_type(str(file))
        if not mime_type:
            continue
            
        try:
            if mime_type.startswith('image/'):
                await photo_processor.process(file, dest_dir)
            elif mime_type.startswith('video/'):
                await video_processor.process(file, dest_dir)
        except Exception as e:
            print(f"Error processing {file}: {e}")

def main() -> None:
    """Entry point for the CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Organiza fotos y videos por fecha desde metadatos.'
    )
    parser.add_argument(
        'source_dir',
        type=Path,
        help='Directorio con los archivos originales'
    )
    parser.add_argument(
        'dest_dir',
        type=Path,
        help='Directorio destino para la colección organizada'
    )
    parser.add_argument(
        'original_videos_dir',
        type=Path,
        help='Directorio para guardar los videos originales'
    )
    
    args = parser.parse_args()
    
    # Validate paths
    if not args.source_dir.is_dir():
        print(f"Error: El directorio origen '{args.source_dir}' no existe")
        return
        
    # Create destination directories if they don't exist
    args.dest_dir.mkdir(parents=True, exist_ok=True)
    args.original_videos_dir.mkdir(parents=True, exist_ok=True)
    
    # Run the processor
    asyncio.run(process_media_files(
        args.source_dir,
        args.dest_dir,
        args.original_videos_dir
    ))

if __name__ == '__main__':
    main()
