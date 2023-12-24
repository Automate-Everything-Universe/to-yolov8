# to_yolov8
The 'to_yolov8' package facilitates the conversion of datasets from the YOLO format (exported from [Label Studio](https://labelstud.io/)) to the YOLOv8 format, which is compatible with [Ultralytics](https://www.ultralytics.com/) models. 
This utility is designed to streamline the process of preparing datasets for training and evaluating machine learning models in the YOLOv8 architecture.

## Overview
The tool is primarily aimed at addressing the specific data formatting and splitting requirements of the YOLOv8 model. 
It ensures that the dataset is appropriately organized and formatted, enabling seamless integration with Ultralytics' YOLOv8 implementations.

## Key Features
**Data Splitting:** Automatically divides the dataset into training, validation, and testing subsets. The default split is 70% for training, 20% for validation, and 10% for testing, but this can be customized.
**Format Conversion:** Converts classes.txt (YOLO format) to data.yaml (YOLOv8 format), ensuring compatibility with YOLOv8’s expected dataset structure.
**Directory Structure Adjustment:** Reorganizes image and label files into separate directories for training, testing, and validation, aligning with YOLOv8's directory requirements.
**Flexibility and Customization:** Supports custom splits and allows for additional files in the source directory, which are simply ignored during the conversion process.

## Installation
To install, run: 
```shell
pip install to_yolov8
```

## Usage
The 'to_yolov8' package can be used either through a command-line interface (CLI) or as part of a Python script.


### CLI
Run the following commands in your terminal:
```shell
to_yolov8 --source_dir <source_directory_path> [--dest_dir <destination_directory_path>] [--split <train_ratio,test_ratio,valid_ratio>]
```
**--source_dir:** Path to the source directory containing the YOLO formatted dataset.
**--dest_dir (optional):** Path to the destination directory where the YOLOv8 formatted dataset will be stored. If not specified, the source directory will be used.
**--split (optional):** Custom split ratios for training, testing, and validation sets. The default is 70% training, 20% testing, and 10% validation

### Script
Include and use the converter in your Python scripts as follows:
```
from to_yolov8 import YoloToYolov8Converter

converter = YoloToYolov8Converter()
converter.convert(source_dir=source_dir, dest_dir=dest_dir, train_ratio=0.7, val_ratio=0.2)
```

### Contributing
Contributions to the 'to_yolov8' package are welcome. If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request on our GitHub repository.


### License
This project is licensed under the [MIT License](https://github.com/Automate-Everything-Universe/to_yolo/blob/main/LICENSE.txt).
