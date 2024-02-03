from abc import ABC, abstractmethod
from typing import Any


class Converter(ABC):
    """
    This is an abstract class meant for implementation as a data converter.
    """
    @abstractmethod
    def convert(self, data: dict[str, Any]) -> Any:
        """
        Abstract method to convert data  from a certain format into another.
        Subclasses should implement this method.
        :param data: Data for conversion
        :return:
        """
        pass
