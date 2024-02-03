from app.data_loader.factory.address.converter.converter import Converter
from app.address.model import Address
from typing import Any


class ToAddressConverter(Converter):
    """
    This is an implementation of an abstract class Converter, containing methods
    for conversion into Address
    """

    def convert(self, data: dict[str, Any]) -> Address:
        """
        This method converts the data given as a dict into an Address object
        :param data: Dict data for conversion.
        :return: A result of conversion - an Address object.
        """
        return Address.from_dict(data)
