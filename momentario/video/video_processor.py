"""Video processing functionality."""
import multiprocessing
import shutil
from datetime import datetime
from pathlib import Path
import subprocess

import ffmpeg

from ..core.media_processor import MediaProcessor


def get_video_duration(path: Path) -> float:
    """Return duration in seconds, or None if error."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries",
                "format=duration", "-of",
                "default=noprint_wrappers=1:nokey=1", str(path)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except Exception:
        return None

class VideoProcessor(MediaProcessor):
    """Processor for video files with AV1 conversion."""
    
    def __init__(self, date_extractor, original_videos_path: Path):
        super().__init__(date_extractor)
        self.original_videos_path = original_videos_path
        
    def _get_base_name(self, file_path: Path) -> str:
        """Get the base name of a video file without _h265 or _AV1 suffixes."""
        name = file_path.stem
        for suffix in ['_h265', '_AV1']:
            if name.endswith(suffix):
                return name[:-len(suffix)]
        return name

    def _find_av1_version(self, base_name: str, dest_base_path: Path, date: datetime) -> Path | None:
        """Find if there's already an AV1 version of this video in the destination."""
        av1_name = f"{base_name}_AV1{'.mp4'}"
        potential_path = self._get_destination_path(Path(av1_name), dest_base_path, date)
        return potential_path if potential_path.exists() else None

    def _handle_h265_video(self, source_path: Path, backup_path: Path) -> None:
        """Handle a video file with _h265 suffix."""
        # Check if it has double _h265 suffix
        if source_path.stem.count('_h265') > 1:
            source_path.unlink()  # Delete file with double suffix
            return None

        # Move to original videos directory
        shutil.move(source_path, backup_path)

        # Check if original exists and remove _h265 version if it does
        base_name = self._get_base_name(source_path)
        original_path = backup_path.parent / f"{base_name}{source_path.suffix}"
        if original_path.exists():
            backup_path.unlink()

    def process(self, source_path: Path, dest_base_path: Path) -> Path:
        """
        Process a video file based on its suffix and existing files:
        1. If _AV1: Move to destination directly
        2. If original has _AV1 version: Move original to backup
        3. If _h265: Handle according to rules
        4. Otherwise: Convert to AV1
        
        Args:
            source_path: Path to source video
            dest_base_path: Base path for the organized collection
            
        Returns:
            Path to the processed video in its new location
        """
        date = self.date_extractor.extract_date(source_path)
        name = source_path.stem
        suffix = source_path.suffix
        base_name = self._get_base_name(source_path)

        # Caso 1: Archivo AV1 - mover directamente a destino
        if name.endswith('_AV1'):
            dest_path = self._get_destination_path(source_path, dest_base_path, date)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source_path, dest_path)
            self._set_file_dates(dest_path, date)
            return dest_path

        backup_path = self.original_videos_path / source_path.name
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        # Caso 2: Archivo original - verificar si ya existe versión AV1
        if not name.endswith('_h265'):
            av1_path = self._find_av1_version(base_name, dest_base_path, date)
            if av1_path and av1_path.exists():
                # Validate duration before accepting AV1
                orig_duration = get_video_duration(source_path)
                av1_duration = get_video_duration(av1_path)
                # Tolerance of 0.5 seconds
                if orig_duration and av1_duration and abs(orig_duration - av1_duration) < 0.5:
                    shutil.move(source_path, backup_path)
                    self._set_file_dates(backup_path, date)
                    return av1_path
                else:
                    # AV1 is corrupt or incomplete, remove and force reconversion
                    av1_path.unlink()

        # Caso 3: Archivo _h265
        if name.endswith('_h265'):
            self._handle_h265_video(source_path, backup_path)
            return backup_path

        # Caso 4: Archivo original sin versión AV1 - convertir
        dest_name = f"{base_name}_AV1{suffix}"
        dest_path = self._get_destination_path(Path(dest_name), dest_base_path, date)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Usar archivo temporal para evitar AV1 corruptos
        tmp_dest_path = dest_path.with_suffix(dest_path.suffix + '.tmp')
        if tmp_dest_path.exists():
            tmp_dest_path.unlink()

        # Eliminar _h265_AV1 en destino si existe
        h265_av1_name = f"{base_name}_h265_AV1{suffix}"
        h265_av1_path = self._get_destination_path(Path(h265_av1_name), dest_base_path, date)
        if h265_av1_path.exists():
            h265_av1_path.unlink()

        # Eliminar _h265 en carpeta de originales si existe
        h265_name = f"{base_name}_h265{suffix}"
        h265_path = self.original_videos_path / h265_name
        if h265_path.exists():
            h265_path.unlink()

        # Convertir a AV1 en archivo temporal
        stream = ffmpeg.input(str(source_path))
        stream = ffmpeg.output(
            stream,
            str(tmp_dest_path),
            format='mp4',
            **{
                'map_metadata': '0',
                'c:v': 'libsvtav1',  # Video codec
                'crf': '38',  # Quality (lower = better)
                'preset': '6',  # Speed preset (0-8, higher = faster)
                'threads': str(multiprocessing.cpu_count()),
                'pix_fmt': 'yuv420p',
                'c:a': 'copy',  # copy audio codec
                'movflags': '+faststart'
            }
        )

        try:
            ffmpeg.run(stream, overwrite_output=True)
        except Exception as e:
            print(f"Error en la conversión AV1: {e}")
            if tmp_dest_path.exists():
                tmp_dest_path.unlink()
            return

        # Si la conversión fue exitosa y el archivo temporal existe, renómbralo
        if tmp_dest_path.exists():
            tmp_dest_path.rename(dest_path)
            # Validate duration before accepting AV1
            orig_duration = get_video_duration(source_path)
            av1_duration = get_video_duration(dest_path)
            if orig_duration and av1_duration and abs(orig_duration - av1_duration) < 0.5:
                shutil.move(source_path, backup_path)
            else:
                print("Duration mismatch after conversion, AV1 file is invalid.")
                dest_path.unlink()
                return
        else:
            print(f"La conversión no generó el archivo AV1 esperado: {tmp_dest_path}")
            return

        # Set file dates based on extracted date
        self._set_file_dates(dest_path, date)

        return dest_path
