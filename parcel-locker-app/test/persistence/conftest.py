import pytest

from app.parcel_locker.model import ParcelLocker
from app.persistence.crud_repo import CrudRepo


@pytest.fixture
def fake_repo(fake_connection) -> CrudRepo:
    return CrudRepo(fake_connection, ParcelLocker)


@pytest.fixture(autouse=True)
def before_each(fake_repo) -> None:
    fake_repo.delete_all()
