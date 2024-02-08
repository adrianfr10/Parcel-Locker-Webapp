import pytest
import logging

from app.parcel_locker.model import Locker
from app.parcel_locker.dto import CreateParcelWithLockersDto
from app.parcel_locker.model import Category

logging.basicConfig(level=logging.INFO)


class TestWhenParcelLockerServiceMethodsWorkGood:

    @pytest.fixture(autouse=True, scope='function')
    def inserted_category_id(self, test_category_repo):
        category_id = test_category_repo.insert(Category(name="test_category", height=25.0, weight=5.0, dept=10.0))
        return category_id

    @pytest.fixture(autouse=True, scope='function')
    def inserted_parcel_locker_id(self, parcel_locker_service, inserted_category_id):
        parcel_with_lockers_dto = CreateParcelWithLockersDto(address_id=1, lockers={str(inserted_category_id): 3})
        parcel_locker_id = parcel_locker_service.add_parcel_locker(parcel_with_lockers_dto)
        return parcel_locker_id

    def test_when_add_parcel_locker_works_good(self, parcel_locker_service) -> None:
        found_lockers = parcel_locker_service.locker_repo.find_all()
        found_parcel_lockers = parcel_locker_service.parcel_locker_repo.find_all()
        assert len(found_lockers) == 3
        assert len(found_parcel_lockers) == 1

    def test_when_get_first_empty_locker_with_category_works_good(self, parcel_locker_service,
                                                                  inserted_category_id) -> None:
        inserted_category_id = inserted_category_id
        found_parcel_locker = parcel_locker_service.parcel_locker_repo.find_all_by_address_id(address_ids=[1])
        parcel_locker_service.locker_repo.insert(Locker(is_empty=False,
                                                        parcel_locker_id=found_parcel_locker[0]._id,
                                                        category_id=inserted_category_id))
        res = parcel_locker_service.get_first_empty_locker_with_category(category_id=inserted_category_id, address_id=1)
        assert res is not None

    def test_if_change_locker_state_works_good(self, parcel_locker_service) -> None:
        found_locker = parcel_locker_service.locker_repo.find_n_last(2)[0]
        changed_locker = parcel_locker_service.change_locker_state(found_locker._id, True)
        assert changed_locker.is_empty == 1

    def test_if_fill_up_locker_works_good(self, parcel_locker_service, test_locker_repo,
                                          inserted_category_id, inserted_parcel_locker_id) -> None:
        inserted_category_id = inserted_category_id
        inserted_pl_id = inserted_parcel_locker_id
        found_pl = parcel_locker_service.parcel_locker_repo.find_one(inserted_pl_id)
        inserted_locker_id = test_locker_repo.insert(Locker(is_empty=False, parcel_locker_id=inserted_pl_id, category_id=inserted_category_id))
        found_locker = parcel_locker_service.locker_repo.find_one(inserted_locker_id)
        filled_locker = parcel_locker_service.fill_up_locker(found_locker.category_id, found_pl.address_id)
        assert filled_locker._id is not None

    def test_if_remove_lockers_with_exceeded_time_works_good(self, parcel_locker_service,
                                                             inserted_category_id, inserted_parcel_locker_id) -> None:
        inserted_category_id = inserted_category_id
        added_pl = parcel_locker_service.parcel_locker_repo.find_one(inserted_parcel_locker_id)
        parcel_locker_service.fill_up_locker(inserted_category_id, added_pl.address_id)
        removed_lockers_ids = parcel_locker_service.remove_lockers_with_exceeded_time(1)
        assert len(removed_lockers_ids) == 0
