import pytest

from app.address.model import Address


class TestWhenGetDistanceIsCorrect:

    @pytest.fixture
    def correct_address_1(self) -> Address:
        return Address(1, "Bielany", "Warsaw", "01-842", "Sokratesa", 45.0, 80.0)

    @pytest.fixture
    def correct_address_2(self) -> Address:
        return Address(1, "Bielany", "Warsaw", "01-842", "Bajana", 45.0, 79.99)

    def test_when_get_distance_works_good(self, correct_address_1, correct_address_2) -> None:
        assert correct_address_1.get_distance(correct_address_2)

    def test_when_get_distance_works_good_with_same_coords(self, correct_address_1) -> None:
        assert correct_address_1.get_distance(correct_address_1) == 0.0
