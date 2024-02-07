from typing import Any

import pytest

from app.address.model import Address
from app.data_loader.factory.address.converter.to_address_converter import ToAddressConverter


class TestToAddressConverter:

    @pytest.fixture
    def data_before_convert(self) -> dict[str, Any]:
        return {
            "address_id": 1,
            "province": "Mazowieckie",
            "city": "Warszawa",
            "street": "Zielona",
            "postal_code": "24-200",
            "coord_x": 12.232332,
            "coord_y": 13.232332
        }

    @pytest.fixture
    def data_after_convert(self) -> Address:
        return Address(address_id=1,
                       province="Mazowieckie",
                       city="Warszawa",
                       street="Zielona",
                       postal_code="24-200",
                       coord_x=12.232332,
                       coord_y=13.232332
                       )

    def test_when_converter_works_correctly(self, data_before_convert, data_after_convert) -> None:
        to_address_converter = ToAddressConverter()
        assert data_after_convert == to_address_converter.convert(data_before_convert)

    @pytest.fixture
    def invalid_data_before_convert(self) -> dict[str, Any]:
        return {
            "address_id": "1",
            "city": 123,
            "street": "Zielona",
            "postal_code": "00-007",
            "coord_x": 1.0,
            "coord_y": 2.0
        }

    def test_when_converter_does_not_work(self, invalid_data_before_convert) -> None:
        with pytest.raises(Exception):
            converter = ToAddressConverter()
            converter.convert(invalid_data_before_convert)
