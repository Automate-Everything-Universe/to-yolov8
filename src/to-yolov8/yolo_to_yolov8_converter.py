"""
Module to handle yolov8 converter
"""
import random
import shutil
from pathlib import Path
from typing import Union, Tuple, List
import yaml

from converter import Converter


class YoloToYolov8Converter(Converter):
    """
    Yolo to Yolov8 specific converter.
    """

    def convert(self, source_dir: Path, dest_dir: Union[Path, None], test) -> None:
        self._validate_yolo_dir_structure(source_dir=source_dir)
        self._create_directory_structure(source_dir=source_dir, dest_dir=dest_dir)
        self._split_datasets(source_dir=source_dir)
        self._create_data_yaml(source_dir=source_dir)

    @staticmethod
    def _validate_yolo_dir_structure(source_dir: Path) -> bool:
        """
        Validates  that the YOLO folder structure is as expected
        :param source_dir:
        :return: bool
        """
        required_paths = {
            "images": source_dir / "images",
            "labels": source_dir / "labels",
            "classes.txt": source_dir / "classes.txt",
        }
        try:
            if not any((source_dir.is_dir(), source_dir.exists())):
                print(f"Could not find {source_dir}")
                return False
            for key, path in required_paths.items():
                if not path.exists():
                    print("Source directory doesn't match expected YOLO structure\n"
                          f"Missing: {path}")
                    return False
            return True
        except ValueError as exc:
            raise ValueError(f"Could not find {source_dir}") from exc
        except PermissionError as exc:
            raise PermissionError(f"Permission denied: {source_dir}") from exc
        except OSError as exc:
            raise OSError(f"An error occured while opening: {source_dir}") from exc

    def _create_directory_structure(self, source_dir: Path, dest_dir: Union[Path, None]) -> None:
        """
        Creates the yolov8 folder structure
        """
        work_dir = dest_dir if dest_dir else source_dir
        categories = ["train", "test", "valid"]
        categories = {
            "train": categories,
            "test": categories,
            "valid": categories
        }
        for cat, folders in categories.items():
            for folder in folders:
                path = work_dir / f"{cat}/{folder}"
                if path.exists():
                    raise FileExistsError("File already exists! Delete and retry.")
                else:
                    path.mkdir(parents=True, exist_ok=True)

    # Logic to create the directory structure for YOLOv8

    def _split_datasets(self, source_dir: Path, dest_dir: Union[Path, None], train_ratio: float = 0.7,
                        val_ratio: float = 0.2) -> None:
        yolo_images_dir = source_dir / "images"
        yolo_labels_dir = source_dir / "labels"

        if not any((yolo_images_dir.exists(), yolo_labels_dir.exists())):
            raise FileNotFoundError(f"Yolo specific folder not found: {yolo_images_dir,}")

        images = [image for image in yolo_images_dir.iterdir()]
        labels = [label for label in yolo_labels_dir.iterdir()]

        if any((len(images) == 0, len(labels) == 0)):
            raise FileNotFoundError(f"No images or labels found in the source directory: {source_dir}")

        random.shuffle(images)

        train_nr = int(int(len(images)) * train_ratio)
        valid_nr = train_nr + int(int(len(images)) * val_ratio)

        for i, img in enumerate(images):
            image_name = images[i].name
            label_name = images[i].name.replace(".jpg", ".txt")
            label = source_dir / "labels" / label_name
            if not label.exists():
                raise FileNotFoundError(f"Corresponding label nod found for img: {image_name}")

            if i < train_nr:
                subset = "train"
            elif i < valid_nr:
                subset = "valid"
            else:
                subset = "test"
            shutil.move(str(image_name), str(dest_dir / subset / "images" / image_name))
            shutil.move(str(label_name), str(dest_dir / subset / "labels" / label_name))

    def _create_data_yaml(self, dest_dir: Path, class_file: Path):
        with class_file.open() as f:
            classes = [line.strip() for line in f.readlines()]

        data = {
            'names': classes,
            'nc': len(classes),
            'train': str(dest_dir / 'train' / 'images'),
            'val': str(dest_dir / 'valid' / 'images'),
            'test': str(dest_dir / 'test' / 'images')
        }

        with open(dest_dir / 'data.yaml', 'w') as f:
            yaml.dump(data, f)
