import shutil
import json
from pathlib import Path
from typing import Union

PATH_TO_DUMMY_FILES = Path(__file__).parents[1] / "yolo_format"


def create_dummy_img(file_path: Path) -> None:
    """
    Creates a dummy PNG file at the specified path.

    Args:
    file_path (Path): The path where the dummy PNG file will be created.
    """
    with open(file_path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')


def crete_dummy_label(file_path: Path) -> None:
    """
    Creates a dummy TXT file at the specified path.

    Args:
    file_path (Path): The path where the dummy PNG file will be created.
    """
    with open(file_path, 'w') as f:
        f.write("This is a dummy label file")


def create_dummy_classes_file(file_path: Path) -> None:
    """
    Creates a dummy yolo specific classes.txt file at the specified path.
    Args:
    file_path (Path): The path where the dummy PNG file will be created
    """
    content = "ElectricalOutlet\n" \
              ""
    classes_file = file_path / "classes.txt"
    with open(classes_file, 'w') as f:
        f.write(content)


def create_dummy_notes_file(file_path: Path) -> None:
    """
    Creates a dummy yolo specific notes.json file at the specified path.
    Args:
    file_path (Path): The path where the dummy PNG file will be created
    """
    content = {
        "categories": [
            {
                "id": 0,
                "name": "ElectricalOutlet"
            }
        ],
        "info": {
            "year": 2023,
            "version": "1.0",
            "contributor": "Label Studio"
        }
    }

    notes_file = file_path / "notes.json"

    with open(notes_file, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4)


def setup_dummy_files(folder_path: Union[Path, str], number_of_files: int = 100) -> None:
    """
    Creates a specified number of dummy PNG files in the given folder.

    Args:
    folder_path (str): The folder in which to create the files.
    number_of_files (int): The number of dummy files to create.
    """
    if not isinstance(folder_path, Path):
        folder_path = Path(folder_path)

    if folder_path.exists:
        shutil.rmtree(folder_path)

    images_path = folder_path / "images"
    labels_path = folder_path / "labels"
    images_path.mkdir(parents=True, exist_ok=True)
    labels_path.mkdir(parents=True, exist_ok=True)

    for i in range(1, number_of_files, 1):
        file_path = folder_path / "images" / f"dummy_{i}.png"
        label_path = folder_path / "labels" / f"dummy_{i}.txt"
        create_dummy_img(file_path)
        crete_dummy_label(label_path)

    create_dummy_classes_file(folder_path)
    create_dummy_notes_file(folder_path)


def main() -> None:
    """
    Main entry to the script
    :return: None
    """
    setup_dummy_files(PATH_TO_DUMMY_FILES)  # repalce with actual path


if __name__ == "__main__":
    main()
