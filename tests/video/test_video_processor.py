import shutil
import tempfile
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch

from momentario.video.video_processor import VideoProcessor

@pytest.fixture
def temp_dirs():
    base = Path(tempfile.mkdtemp())
    origen = base / "origen"
    destino = base / "destino"
    originales = base / "originales"
    for d in (origen, destino, originales):
        d.mkdir()
    yield origen, destino, originales
    shutil.rmtree(base)

@patch("momentario.video.video_processor.ffmpeg.run")
def test_elimina_h265_y_h265av1_al_convertir_original(mock_ffmpeg, temp_dirs):
    origen, destino, originales = temp_dirs
    base = "video_test"
    ext = ".mp4"
    original = origen / f"{base}{ext}"
    h265 = originales / f"{base}_h265{ext}"
    h265_av1 = destino / f"{base}_h265_AV1{ext}"
    original.write_text("original")
    h265.write_text("h265")
    h265_av1.write_text("h265_av1")

    extractor = MagicMock()
    extractor.extract_date.return_value = None
    vp = VideoProcessor(date_extractor=extractor, original_videos_path=originales)

    # Simular que ffmpeg.run crea el AV1 en el destino
    def fake_ffmpeg_run(*args, **kwargs):
        av1 = destino / f"{base}_AV1{ext}"
        av1.write_text("av1")
        h265_av1 = destino / f"{base}_h265_AV1{ext}"
        if h265_av1.exists():
            h265_av1.unlink()
    mock_ffmpeg.side_effect = fake_ffmpeg_run

    vp.process(original, destino)

    av1 = destino / f"{base}_AV1{ext}"
    assert av1.exists(), "El AV1 convertido debe existir"
    assert not h265.exists(), "El _h265 debe eliminarse"
    assert not h265_av1.exists(), "El _h265_AV1 debe eliminarse"
