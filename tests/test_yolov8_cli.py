import shutil
import subprocess
from pathlib import Path

import pytest

TEST_FOLDER = Path(__file__).parents[0]
PROJECT_FOLDER = Path(__file__).parents[1]

MAIN = Path(__file__).parents[1] / "src/cli.py"

SPLIT_RATIO = "70,10,20"


@pytest.fixture
def source_dir() -> Path:
    return TEST_FOLDER / "yolo_format"


@pytest.fixture
def empty_dir() -> Path:
    return TEST_FOLDER / "no_pic_dir"


@pytest.fixture
def dest_dir() -> Path:
    return TEST_FOLDER / "yolov8_format"


def test_yolov8_converter_class(source_dir, dest_dir):
    command = [
        "python",
        str(MAIN),
        "--source_dir",
        str(source_dir),
        "--dest_dir",
        str(dest_dir),
        "--split",
        SPLIT_RATIO,
    ]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert dest_dir.exists(), "Yolov8 folder doesn't exist"

    # Clean up
    shutil.rmtree(dest_dir)


def test_yolov8_empty_dir(empty_dir):
    command = [
        "python",
        str(MAIN),
        "--source_dir",
        str(empty_dir),
    ]

    result = subprocess.run(command, capture_output=True, check=False, text=True, timeout=180)
    assert (
        result.returncode == 1
    ), "Expected a non-zero return code for invalid directory structure."

    # Check that the expected error message is in stderr
    expected_error_message = "The file/directory was not found"
    assert (
        expected_error_message in result.stderr
    ), f"Expected error message '{expected_error_message}' not found in stderr."
