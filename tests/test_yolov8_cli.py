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


def test_yolov8_converter_instalation(source_dir, dest_dir):
    try:
        dist_folder = PROJECT_FOLDER / "dist"
        if dist_folder.exists():
            shutil.rmtree(dist_folder)
        # Install build module
        subprocess.run(["python", "-m", "pip", "install", "build"], check=True, cwd=PROJECT_FOLDER)

        # Build the package
        subprocess.run(["python", "-m", "build"], check=True, cwd=PROJECT_FOLDER)

        # Path to the built .whl file
        whl_file = PROJECT_FOLDER / "dist" / "to_yolov8-0.1.0-py3-none-any.whl"

        # Step 2: Install your library in the virtual environment
        subprocess.run(
            ["python", "-m", "pip", "install", str(whl_file)], check=True, cwd=PROJECT_FOLDER
        )

        # Step 3: Run your CLI script
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

        # Assertions
        assert result.returncode == 0, f"Script failed with errors: {result.stderr}"
        assert dest_dir.exists(), "Yolov8 folder doesn't exist"

        # Clean up
        shutil.rmtree(dest_dir)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.output.decode()}")  # Add this line