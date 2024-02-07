import unittest

from app.data_loader.factory.address.converter.to_address_converter import ToAddressConverter
from app.data_loader.factory.address.factory.json_address_factory import JsonAddressFactory
from app.data_loader.factory.address.loader.json_data_loader import JsonDataLoader
from app.data_loader.factory.address.validator.regex_validator import RegexValidator


class TestJsonAddressFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.json_car_factory = JsonAddressFactory()

    def test_if_type_of_create_data_loader_is_correct(self) -> None:
        self.assertIsInstance(self.json_car_factory.create_data_loader(), JsonDataLoader)

    def test_if_type_of_create_validator_is_correct(self) -> None:
        self.assertIsInstance(self.json_car_factory.create_validator(), RegexValidator)

    def test_if_type_of_create_converter_is_correct(self) -> None:
        self.assertIsInstance(self.json_car_factory.create_converter(), ToAddressConverter)


if __name__ == '__main__':
    unittest.main()
