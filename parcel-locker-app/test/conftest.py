import pytest

from app.address.model import Address
from app.address.service import AddressService
from app.parcel_locker.repo import ParcelLockerRepo, LockerRepo, CategoryRepo
from app.parcel_locker.service import ParcelLockerService
from app.persistence.connection import MySQLConnectionPoolBuilder


@pytest.fixture
def fake_connection() -> MySQLConnectionPoolBuilder:
    return MySQLConnectionPoolBuilder().set_port(3308).set_host("mysql-test").build()


@pytest.fixture
def test_parcel_locker_repo(fake_connection) -> ParcelLockerRepo:
    return ParcelLockerRepo(fake_connection)


@pytest.fixture
def test_locker_repo(fake_connection) -> LockerRepo:
    return LockerRepo(fake_connection)


@pytest.fixture
def test_category_repo(fake_connection) -> CategoryRepo:
    return CategoryRepo(fake_connection)


@pytest.fixture
def addresses() -> list[Address]:
    return (
        [
            Address(
                address_id=1,
                province="A",
                city="C",
                postal_code="24-100",
                street="S",
                coord_x=12.232332,
                coord_y=13.232332
            )
        ]
    )


@pytest.fixture
def address_service(addresses) -> AddressService:
    return AddressService(addresses)


@pytest.fixture
def parcel_locker_service(address_service, test_parcel_locker_repo, test_locker_repo) -> ParcelLockerService:
    return ParcelLockerService(address_service, test_parcel_locker_repo, test_locker_repo)


@pytest.fixture(autouse=True)
def before_each(test_parcel_locker_repo, test_locker_repo, test_category_repo) -> None:
    test_category_repo.delete_all()
    test_parcel_locker_repo.delete_all()
