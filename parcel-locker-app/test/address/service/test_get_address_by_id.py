import pytest


class TestAddressServiceGetAddressByIdCorrect:

    @pytest.fixture
    def expected_id(self) -> int:
        return 1

    def test_has_address_with_id(self, address_service, expected_id) -> None:
        assert address_service.get_address_by_id(expected_id).address_id == expected_id


class TestAddressServiceGetAddressByIdNotCorrect:

    @pytest.fixture
    def not_expected_id(self) -> int:
        return 2

    def test_has_not_address_with_id(self, address_service, not_expected_id) -> None:
        with pytest.raises(ValueError) as ex:
            address_service.get_address_by_id(not_expected_id)
        assert str(ex.value) == f'No unique address with id: {not_expected_id}'


class TestAddressServiceGetAddressByIdWithNoAddresses:

    def test_has_address_with_id_no_addresses_in_service(self, address_service_no_addresses) -> None:
        with pytest.raises(ValueError) as ex:
            address_service_no_addresses.get_address_by_id(1)
        assert str(ex.value) == f'No unique address with id: {1}'
