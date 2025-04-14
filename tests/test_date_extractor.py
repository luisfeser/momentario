"""Tests for the date extractor module."""
from datetime import datetime
from pathlib import Path

import pytest

from momentario.utils.date_extractor import MediaDateExtractor

@pytest.fixture
def date_extractor():
    """Fixture that provides a MediaDateExtractor instance."""
    return MediaDateExtractor()

def test_extract_date_from_filename(date_extractor, tmp_path):
    """Test date extraction from filename."""
    test_file = tmp_path / "photo_2023-04-15.jpg"
    test_file.touch()
    
    date = date_extractor.extract_date(test_file)
    assert date == datetime(2023, 4, 15)

def test_extract_date_from_filename_alternate_format(date_extractor, tmp_path):
    """Test date extraction from filename with alternate format."""
    test_file = tmp_path / "15-04-2023_photo.jpg"
    test_file.touch()
    
    date = date_extractor.extract_date(test_file)
    assert date == datetime(2023, 4, 15)

def test_no_date_in_filename(date_extractor, tmp_path):
    """Test handling of files without date in name."""
    test_file = tmp_path / "photo.jpg"
    test_file.touch()
    
    date = date_extractor.extract_date(test_file)
    assert date is None
