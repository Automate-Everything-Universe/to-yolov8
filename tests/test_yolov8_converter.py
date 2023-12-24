import shutil
from pathlib import Path

import pytest
from src.to_yolov8.yolo_to_yolov8_converter import YoloToYolov8Converter

TEST_FOLDER = Path(__file__).parents[0]


@pytest.fixture
def source_dir() -> Path:
    return TEST_FOLDER / "yolo_format"


@pytest.fixture
def dest_dir() -> Path:
    return TEST_FOLDER / "yolov8_format"


def test_yolov8_converter_class(source_dir, dest_dir):
    converter = YoloToYolov8Converter()
    converter.convert(source_dir=source_dir, dest_dir=dest_dir)
    assert dest_dir.exists(), "Yolov8 folder doesn't exist"
    shutil.rmtree(dest_dir)
