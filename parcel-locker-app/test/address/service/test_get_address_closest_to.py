import pytest

from app.address.model import Address


@pytest.fixture
def correct_address_from_service():
    return Address(
        address_id=1,
        province="A",
        city="C",
        postal_code="24-100",
        street="S",
        coord_x=12.232332,
        coord_y=13.232332
    )


class TestAddressServiceGetAddressClosestToCorrect:

    def test_get_address_closest_to_correct(self, address_service, correct_address_from_service) -> None:
        assert address_service.get_address_closest_to(correct_address_from_service) == correct_address_from_service


class TestAddressServiceGetAddressClosestToWithNoAddresses:

    def test_get_address_closest_to_with_no_addresses_in_service(self, address_service_no_addresses,
                                                                 correct_address_from_service) -> None:
        assert address_service_no_addresses.get_address_closest_to(correct_address_from_service) is None
