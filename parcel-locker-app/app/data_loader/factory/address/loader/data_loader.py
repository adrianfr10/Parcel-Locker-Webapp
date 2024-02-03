from abc import ABC, abstractmethod
from typing import Any


class DataLoader(ABC):
    """
    This is an abstract class meant for implementation as a data loader.
    """
    @abstractmethod
    def get_data(self, filepath: str) -> list[dict[str, Any]]:
        """
        Abstract method to load data  from a certain file.
        Subclasses should implement this method.
        :param filepath: A filepath to the data source
        :return: A list of loaded data
        """
        pass
