from abc import ABC, abstractmethod
from typing import Type

from FileManager.FileFormatABC import FileFormatABC


class FileInterpreterABC(ABC):
    """Assume the files exist"""
    @property
    @abstractmethod
    def extension(self) -> str:
        """Just a property to get the expected file extension"""
        pass

    @abstractmethod
    def write(self, formatted: Type[FileFormatABC]) -> str:
        """
        :param formatted: the implemented FileFormat
        :return: a string to directly write to the file
        """
        pass

    @abstractmethod
    def read(self, file_contents: str) -> Type[FileFormatABC]:
        """
        :param file_contents: the raw contents of the written file
        :return: the expected implementation of FileFormatABC
        """
        pass