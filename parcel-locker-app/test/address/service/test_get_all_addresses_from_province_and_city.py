import pytest


class TestAddressServiceGetAllAddressesFromProvinceAndCityCorrect:

    def test_has_address_from_province_and_city(self, address_service) -> None:
        assert address_service.get_all_addresses_from_province_and_city("A", "C")

    def test_has_address_from_province_and_city_empty_return(self, address_service) -> None:
        assert address_service.get_all_addresses_from_province_and_city("B", "X") == []


class TestAddressServiceGetAllAddressesFromProvinceAndCityNotCorrect:

    def test_has_address_from_province_and_city_raises_exception(self, address_service) -> None:
        with pytest.raises(ValueError) as ve:
            address_service.get_all_addresses_from_province_and_city(1, 2)
        assert str(ve.value) == "Province and city must be strings"


class TestAddressServiceGetAllAddressesFromProvinceAndCityWithNoAddresses:

    def test_has_address_from_province_and_city(self, address_service_no_addresses) -> None:
        assert address_service_no_addresses.get_all_addresses_from_province_and_city("A", "C") == []

