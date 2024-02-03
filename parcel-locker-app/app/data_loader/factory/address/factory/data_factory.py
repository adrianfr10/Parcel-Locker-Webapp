from abc import ABC, abstractmethod
from typing import Any


class DataFactory(ABC):
    """
    This is an abstract class meant for implementation as a data factory -
    containing methods to create different components related to data handling.
    """

    @abstractmethod
    def create_data_loader(self) -> Any:
        """
        Abstract method to create a data loader object.
        Subclasses should implement this method.
        :return: An object responsible for loading data.
        """
        pass

    @abstractmethod
    def create_validator(self) -> Any:
        """
         Abstract method to create a validator object.
         Subclasses should implement this method.
         :return: An object responsible for validating data.
         """
        pass

    @abstractmethod
    def create_converter(self) -> Any:
        """
        Abstract method to create a converter object.
        Subclasses should implement this method.
        :return: An object responsible for validating data.
        """
        pass
