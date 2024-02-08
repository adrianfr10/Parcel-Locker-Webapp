from app.parcel_locker.model import Locker, Category, ParcelLocker


class TestWhenLockerRepoMethodsWorkGood:

    def test_when_update_locker_works_good(self, test_parcel_locker_repo, test_locker_repo, test_category_repo) -> None:
        inserted_pl_id = test_parcel_locker_repo.insert(ParcelLocker(address_id=1))
        inserted_category_id = test_category_repo.insert(Category(_id=1))
        found_pl = test_parcel_locker_repo.find_one(inserted_pl_id)
        inserted_locker_id = test_locker_repo.insert(Locker(is_empty=False,
                                                            parcel_locker_id=found_pl._id,
                                                            category_id=inserted_category_id))
        locker_to_update = Locker(is_empty=True, parcel_locker_id=found_pl._id, category_id=inserted_category_id)
        locker_after_update = test_locker_repo.update_locker(inserted_locker_id, locker_to_update)
        assert locker_after_update.is_empty == 1
