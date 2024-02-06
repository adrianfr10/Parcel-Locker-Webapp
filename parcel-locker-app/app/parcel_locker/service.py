from dataclasses import dataclass
from itertools import chain
from datetime import datetime

from app.address.service import AddressService
from app.parcel_locker.dto import CreateParcelWithLockersDto
from app.parcel_locker.model import ParcelLocker, Locker
from app.parcel_locker.repo import ParcelLockerRepo, LockerRepo
import logging

logging.basicConfig(level=logging.INFO)


@dataclass(eq=False)
class ParcelLockerService:
    """
    This class is uses for managing and performing operations on parcel lockers
    Attributes:
        address_service    -    Instance of AddressService with methods for managing addresses
        parcel_locker_repo -    Instance of ParcelLockerRepo with methods for parcel lockers
        locker_repo        -    Instance of LockerRepo with methods for lockers
    """
    address_service: AddressService
    parcel_locker_repo: ParcelLockerRepo
    locker_repo: LockerRepo

    # ---------------------------------------------------------------------------------------

    def add_parcel_locker(self, create_parcel_with_lockers: CreateParcelWithLockersDto) -> int:
        """
        Method performs adding parcel with check if the address with given id exists
        :param create_parcel_with_lockers:
        :return:
        """
        # Assuming that only one parcel locker is at given address

        # Step 1. Get data about address
        address_id = create_parcel_with_lockers.address_id
        address_for_parcel = self.address_service.get_address_by_id(address_id)

        # Step 2. Check if parcel locker is at given address
        if len(self.parcel_locker_repo.find_all_by_address_id([address_for_parcel.address_id])) > 0:
            raise ValueError('Address already occupied')

        # Step 3. Creating parcel locker, because its id is needed to assign it to lockers
        inserted_parcel_locker_id = self.parcel_locker_repo.insert(ParcelLocker(address_id=address_id))

        # Step 4. Creating specified lockers
        lockers = create_parcel_with_lockers.lockers
        lockers2 = [
            [Locker(category_id=int(category_id), parcel_locker_id=inserted_parcel_locker_id)] * quantity
            for category_id, quantity in lockers.items()
        ]
        lockers3 = list(chain.from_iterable(lockers2))
        inserted_lockers_id = self.locker_repo.insert_many(lockers3)
        return inserted_parcel_locker_id

    # ---------------------------------------------------------------------------------------

    def get_first_empty_locker_with_category(self, category_id: int, address_id: int) -> int:
        """
        Method is used to get an empty locker with given category id from a parcel locker.
        :param category_id:
        :param address_id:
        :return: Empty locker id
        """

        # Identifying parcel locker
        found_parcel_lockers = self.parcel_locker_repo.find_all_by_address_id([address_id])
        if len(found_parcel_lockers) != 1:
            raise ValueError('Parcel locker not found')
        found_parcel_locker = found_parcel_lockers[0]

        # Identifying all lockers from certain parcel locker and if lockers count is greater than 0
        # then we have empty lockers
        empty_lockers = [
            locker
            for locker in self.locker_repo.find_all()
            if locker.parcel_locker_id == found_parcel_locker._id and
            locker.category_id == category_id and
            not locker.is_empty
        ]
        logging.info(f"Found {len(empty_lockers)} empty lockers")  # Add this line

        # If there is no empty lockers throwing an exception
        if len(empty_lockers) == 0:
            raise ValueError('No empty locker with expected category')

        return empty_lockers[0]._id

    # ---------------------------------------------------------------------------------------

    def change_locker_state(self, locker_id: int, is_empty: bool) -> Locker:
        """
        Method changes the is_empty attribute of the locker with given id.
        :param locker_id:
        :param is_empty:
        :return:
        """
        locker_to_update = self.locker_repo.find_one(locker_id)

        updated_locker = (locker_to_update.change_state(is_empty)
                          .update_not_empty_start_date_time(None if not is_empty else datetime.now().timestamp()))

        # Save the updated locker to the repository
        updated_locker = self.locker_repo.update_locker(locker_id, updated_locker)
        return updated_locker

    # ---------------------------------------------------------------------------------------

    def remove_lockers_with_exceeded_time(self, limit_hours: int) -> list[int]:
        """
        Method removes content from the Lockers that have exceeded a certain number of hours
        :param limit_hours:
        :return:
        """
        occupied_lockers = [locker for locker in self.locker_repo.find_all() if locker.is_empty]
        lockers_to_update = []
        for locker in occupied_lockers:
            if locker.is_not_empty_too_long(limit_hours):
                updated_locker = self.change_locker_state(locker._id, False)
                lockers_to_update.append(updated_locker)

        for updated_locker in lockers_to_update:
            # Update the locker in your repository or database
            self.locker_repo.update_locker(updated_locker._id, updated_locker)

        return [locker._id for locker in lockers_to_update]

    # ---------------------------------------------------------------------------------------
    def fill_up_locker(self, category_id: int, address_id: int) -> Locker:
        """
        Method performs adding a parcel into a locker.
        :param category_id:
        :param address_id:
        :return:
        """
        # getting empty locker with specified category id
        locker_to_fill_up_id = self.get_first_empty_locker_with_category(category_id, address_id)
        # changing locker status to occupied
        return self.change_locker_state(locker_to_fill_up_id, True)

