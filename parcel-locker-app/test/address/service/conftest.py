import pytest

from app.address.service import AddressService


@pytest.fixture
def address_service_no_addresses() -> AddressService:
    return AddressService([])
