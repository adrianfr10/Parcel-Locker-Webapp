from app.data_loader.factory.address.factory.data_factory import DataFactory
from app.data_loader.factory.address.loader.json_data_loader import JsonDataLoader
from app.data_loader.factory.address.validator.regex_validator import RegexValidator
from app.data_loader.factory.address.converter.to_address_converter import ToAddressConverter


class JsonAddressFactory(DataFactory):
    """
    Particular implementation of DataFactory for handling address data from JSON.
    """
    def create_data_loader(self) -> JsonDataLoader:
        """
         Creates a JSON data loader object specific to address data.
        :return: An object responsible for loading address data from JSON.
        """
        return JsonDataLoader()

    def create_validator(self) -> RegexValidator:
        """
        Creates a regex validator object specific to address validation.
        :return: An object responsible for validating address data using regex.
        """
        return RegexValidator(r'^\d{2}-\d{3}$')

    def create_converter(self) -> ToAddressConverter:
        """
        Creates an address converter object specific to address conversion.
        :return: An object responsible for converting address data.
        """
        return ToAddressConverter()
