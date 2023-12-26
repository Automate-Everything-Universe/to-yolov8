"""
Main entry
"""
import argparse
from pathlib import Path
from typing import Tuple

from to_yolov8.yolo_to_yolov8_converter import YoloToYolov8Converter


def parse_arguments() -> argparse.Namespace:
    """
    Parses user arguments
    :return:
    """
    parser = argparse.ArgumentParser(
        prog="to_yolov8",
        description="to_yolov8 package can do the following conversion:\n"
        "- Takes an source_folder with the YOLO format (e.g. exported from Label Studio)\n"
        "- Creates the expected YOLOV8 folder structure and data.yaml file\n"
        "- Splits the original YOLO dataset into train test validation",
    )
    parser.add_argument(
        "--source_dir",
        required=True,
        help="Path to the source directory containing the YOLO formatted dataset.",
    )
    parser.add_argument(
        "--dest_dir",
        help="Path to the destination directory where the YOLOv8 formatted dataset will "
             "be stored.\n"
        "If not specified, the source directory will be used.",
    )
    parser.add_argument(
        "--split",
        help="Custom split ratios for training, testing, and validation sets. \n"
        "The default is 70% training, 10% testing, and 20% validation",
    )
    return parser.parse_args()


def validate_split(split: Tuple[float, ...]) -> bool:
    """
    Validates that the sum of the split values are under 100
    :param split: User given split valus in form '70,20,10'
    :return: bool
    """
    try:
        if sum(split) != 1:
            raise ValueError("Sum of split values must be 100 (e.g. 70, 10, 20")
        return True
    except ValueError as exc:
        raise ValueError("Given split values don't match expected 'int,int,int'") from exc


def main():
    """
    Main entry for the CLI
    :return: None
    """
    try:
        args = parse_arguments()
        source_dir = Path(args.source_dir)
        dest_dir = Path(args.dest_dir) if args.dest_dir else source_dir
        split = (
            tuple([int(i) / 100 for i in args.split.split(",")]) if args.split else (0.7, 0.1, 0.2)
        )

        if split:
            validate_split(split=split)
        train, _, valid = split

        converter = YoloToYolov8Converter()
        converter.convert(
            source_dir=source_dir, dest_dir=dest_dir, train_ratio=train, val_ratio=valid
        )

    except ValueError as exc:
        print(f"Invalid value provided: {exc}")
        return 1
    except FileNotFoundError as exc:
        print(f"The file was not found: {exc}")
        return 1
    except PermissionError as exc:
        print(f"Permission denied for file: {exc}")
        return 1
    except OSError as exc:
        print(f"An error occurred while opening the file: {exc}")
        return 1
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        return 1


if __name__ == "__main__":
    main()
