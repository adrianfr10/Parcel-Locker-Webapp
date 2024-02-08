import logging

from app.parcel_locker.model import ParcelLocker

logging.basicConfig(level=logging.INFO)


class TestWhenCrudRepoMethodsWorkCorrectly:

    def test_if_insert_works_good(self, fake_repo) -> None:
        res = fake_repo.insert(ParcelLocker(address_id=1))
        assert res > 0

    def test_if_insert_many_works_good(self, fake_repo) -> None:
        fake_repo.insert_many([ParcelLocker(address_id=1), ParcelLocker(address_id=2)])
        data = fake_repo.find_all()
        assert len(data) == 2

    def test_if_update_works_good(self, fake_repo) -> None:
        inserted_id = fake_repo.insert(ParcelLocker(address_id=1))
        updated_locker = ParcelLocker(address_id=2)
        fake_repo.update(inserted_id, updated_locker)
        fetched_updated_locker = fake_repo.find_one(inserted_id)
        assert fetched_updated_locker.address_id == 2

    def test_if_find_n_last_works_good(self, fake_repo) -> None:
        fake_repo.insert_many([ParcelLocker(address_id=1),
                               ParcelLocker(address_id=2),
                               ParcelLocker(address_id=3)
                               ]
                              )
        last_two_lockers = fake_repo.find_n_last(2)
        assert len(last_two_lockers) == 2
        assert last_two_lockers[0].address_id == 3
        assert last_two_lockers[1].address_id == 2

    def test_if_find_all_works_good(self, fake_repo) -> None:
        fake_repo.insert_many([ParcelLocker(address_id=1), ParcelLocker(address_id=2)])
        result = fake_repo.find_all()
        assert len(result) == 2

    def test_if_find_one_works_good(self, fake_repo) -> None:
        inserted_id = fake_repo.insert(ParcelLocker(address_id=1))
        parcel_locker = fake_repo.find_one(inserted_id)
        assert parcel_locker.address_id == 1

    def test_if_delete_all_works_good(self, fake_repo) -> None:
        fake_repo.insert(ParcelLocker(address_id=1))
        fake_repo.delete_all()
        data = fake_repo.find_all()
        assert len(data) == 0

    def test_if_delete_one_works_good(self, fake_repo) -> None:
        inserted_id = fake_repo.insert(ParcelLocker(address_id=1))
        fake_repo.delete_one(inserted_id)
        data = fake_repo.find_all()
        assert len(data) == 0

    def test_if_delete_all_by_id_works_good(self, fake_repo) -> None:
        fake_repo.insert_many([ParcelLocker(address_id=1),
                               ParcelLocker(address_id=2),
                               ParcelLocker(address_id=3)])
        items_to_delete_ids = [obj._id for obj in fake_repo.find_all() if obj.address_id in [1, 2]]

        fake_repo.delete_all_by_id(items_to_delete_ids)
        data_after_delete = fake_repo.find_all()
        assert len(data_after_delete) == 1
