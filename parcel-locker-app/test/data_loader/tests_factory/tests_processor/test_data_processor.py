from unittest.mock import MagicMock

import pytest

from app.address.model import Address
from app.data_loader.factory.address.converter.converter import Converter
from app.data_loader.factory.address.converter.to_address_converter import ToAddressConverter
from app.data_loader.factory.address.factory.data_factory import DataFactory
from app.data_loader.factory.address.factory.processor.data_processor import DataProcessor
from app.data_loader.factory.address.loader.data_loader import DataLoader
from app.data_loader.factory.address.loader.json_data_loader import JsonDataLoader
from app.data_loader.factory.address.validator.regex_validator import RegexValidator
from app.data_loader.factory.address.validator.validator import Validator


class MockDataFactory(DataFactory):

    def create_data_loader(self) -> DataLoader:
        json_data_loader = JsonDataLoader()

        return_value = [{
            "address_id": 1,
            "province": "Mazowieckie",
            "city": "Warszawa",
            "street": "Zielona",
            "postal_code": "00-007",
            "coord_x": 12.232332,
            "coord_y": 13.232332
        }
        ]

        json_data_loader.get_data = MagicMock(return_value=return_value)
        return json_data_loader

    def create_validator(self) -> Validator:
        regex_validator = RegexValidator(r'^\d{2}-\d{3}$')
        validated_return_value = {
            "address_id": 1,
            "province": "Mazowieckie",
            "city": "Warszawa",
            "street": "Zielona",
            "postal_code": "00-007",
            "coord_x": 12.232332,
            "coord_y": 13.232332
        }

        regex_validator.validate = MagicMock(return_value=validated_return_value)
        return regex_validator

    def create_converter(self) -> Converter:
        to_address_converter = ToAddressConverter()

        converted_return_value = Address(address_id=1,
                                         province="Mazowieckie",
                                         city="Warszawa",
                                         street="Zielona",
                                         postal_code="00-007",
                                         coord_x=12.232332,
                                         coord_y=13.232332
                                         )

        to_address_converter.convert = MagicMock(return_value=converted_return_value)
        return to_address_converter


@pytest.fixture
def processed_return_value() -> list[Address]:
    return [Address(address_id=1,
                    province="Mazowieckie",
                    city="Warszawa",
                    street="Zielona",
                    postal_code="00-007",
                    coord_x=12.232332,
                    coord_y=13.232332
                    )]


def test_when_data_processor_works_correct(processed_return_value) -> None:
    data_processor = DataProcessor(MockDataFactory())
    assert processed_return_value == data_processor.process(None)
