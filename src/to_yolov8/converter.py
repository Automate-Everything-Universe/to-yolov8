"""
Interface for the converter pater.
"""
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Union


class Converter(ABC):
    """
    Interface for converter
    """

    @abstractmethod
    def convert(self, source_dir: Path, dest_dir: Union[None, Path] = None) -> None:
        """
        Method which converts to yolov8 format.
        :return:
        """
