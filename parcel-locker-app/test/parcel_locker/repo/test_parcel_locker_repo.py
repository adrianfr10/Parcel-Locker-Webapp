from app.parcel_locker.model import ParcelLocker, Locker, Category
import logging

logging.basicConfig(level=logging.INFO)


class TestsWhenParcelLockerRepoMethodsWorkGood:

    def test_if_find_one_by_address_id_works_good(self, test_parcel_locker_repo) -> None:
        test_parcel_locker_repo.insert(ParcelLocker(address_id=1))
        found_item = test_parcel_locker_repo.find_one_by_address_id(1)
        assert found_item.address_id == 1

    def test_if_find_all_by_address_id_works_good(self, test_parcel_locker_repo) -> None:
        test_parcel_locker_repo.insert(ParcelLocker(address_id=1))
        test_parcel_locker_repo.insert(ParcelLocker(address_id=2))
        data = test_parcel_locker_repo.find_all_by_address_id([1, 2])
        assert len(data) == 2

    def test_if_get_lockers_info_works_good(self, test_parcel_locker_repo,
                                            test_locker_repo, test_category_repo) -> None:
        test_parcel_locker_repo.insert(ParcelLocker(address_id=1))
        inserted_category_id = test_category_repo.insert(Category(_id=1))
        found_pl = test_parcel_locker_repo.find_one_by_address_id(address_id=1)
        test_locker_repo.insert(Locker(is_empty=True, parcel_locker_id=found_pl._id, category_id=inserted_category_id))
        assert test_parcel_locker_repo.get_lockers_info() is not None

    def test_if_has_at_least_one_empty_locker_with_category_works_correct(self, test_parcel_locker_repo,
                                                                          test_locker_repo,
                                                                          test_category_repo) -> None:
        inserted_pl_id = test_parcel_locker_repo.insert(ParcelLocker(address_id=1))
        inserted_category_id = test_category_repo.insert(Category(_id=1))
        found_pl = test_parcel_locker_repo.find_one(inserted_pl_id)
        inserted_locker_id = test_locker_repo.insert(Locker(is_empty=False,
                                                            parcel_locker_id=found_pl._id,
                                                            category_id=inserted_category_id))
        added_locker = test_locker_repo.find_one(inserted_locker_id)
        assert test_parcel_locker_repo.has_at_least_one_empty_locker_with_category(pl_id=found_pl._id,
                                                                                   category_id=added_locker.category_id)
