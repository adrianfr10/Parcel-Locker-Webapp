from abc import ABC, abstractmethod
from typing import Any
import re


class Validator(ABC):
    """
    Abstract base class defining the structure for data validation.
    """
    @abstractmethod
    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Abstract method to validate input data.
        :param data: Data to be validated.
        :return: Validated data.
        """
        pass

    @staticmethod
    def matches_regex(regex: str, text: str) -> bool:
        """
        Checks if the given text matches the provided regex pattern.
        :param regex: Regular expression pattern.
        :param text: Text to be checked.
        :return: True if the text matches the regex pattern, False otherwise.
        """
        return re.match(regex, text) is not None

    @staticmethod
    def is_greater_than(limit: int, value: int) -> bool:
        """
        Checks if the given value is greater than the specified limit.
        :param limit:  The comparison limit.
        :param value: Value to be compared.
        :return: True if the value is greater than the limit, False otherwise.
        """
        return value > limit
