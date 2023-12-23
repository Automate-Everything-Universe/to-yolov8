"""
Interface for the converter pater.
"""
from abc import ABC, abstractmethod
from ctypes import Union
from pathlib import Path


class Converter(ABC):
    """
    Interface for converter
    """

    @abstractmethod
    def convert(self, source_dir: Path, dest_dir: Union[None, Path]) -> None:
        """
        Method which converts to yolov8 format.
        :return:
        """
