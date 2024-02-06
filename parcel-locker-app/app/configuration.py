from typing import Final

from app.address.service import AddressService
from app.data_loader.factory.address.factory.json_address_factory import JsonAddressFactory
from app.data_loader.factory.address.factory.processor.data_processor import DataProcessor
from app.parcel_locker.repo import CategoryRepo
from app.parcel_locker.repo import ParcelLockerRepo, LockerRepo
from app.parcel_locker.service import ParcelLockerService
from app.persistence.connection import connection
from dotenv import load_dotenv
import os

load_dotenv()
# ------------------------------------------------------------------------------------------------------
# PURE SQL DIALECT REPOS
# ------------------------------------------------------------------------------------------------------
FILENAME: Final[str] = os.getenv('FILENAME')
addresses = DataProcessor(JsonAddressFactory()).process(FILENAME)
address_service = AddressService(addresses)
parcel_locker_repo = ParcelLockerRepo(connection)
locker_repo = LockerRepo(connection)
parcel_locker_service = ParcelLockerService(address_service, parcel_locker_repo, locker_repo)
category_repo = CategoryRepo(connection)
