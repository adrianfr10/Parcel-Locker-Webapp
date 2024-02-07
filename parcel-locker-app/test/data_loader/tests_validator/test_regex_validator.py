import pytest
from typing import Any


class TestRegexValidatorCorrect:

    @pytest.fixture
    def correct_address_data(self) -> dict[str, Any]:
        return {
            "address_id": 1,
            "province": "A",
            "city": "Warsaw",
            "postal_code": "00-007",
            "coord_x": 12.232332,
            "coord_y": 13.232332
        }

    def test_when_validator_works_correct(self, validator, correct_address_data) -> None:
        assert validator.validate(correct_address_data) == correct_address_data


class TestRegexValidatorIncorrect:

    @pytest.fixture
    def incorrect_address_data(self) -> dict[str, Any]:
        return {
            "address_id": "1",
            "province": "A",
            "city": "Warsaw",
            "postal_code": "00-007",
            "coord_x": "12.23232",
            "coord_y": 13.23232
        }

    def test_when_validation_errors_occurred(self, validator, incorrect_address_data) -> None:
        with pytest.raises(ValueError):
            validator.validate(incorrect_address_data)

    @pytest.fixture
    def incorrect_postal_code_address_data(self) -> dict[str, Any]:
        return {
            "address_id": 1,
            "province": "A",
            "postal_code": "10-100",
            "coord_x": "12.23232",
            "coord_y": "13.23232"
        }

    def test_when_validator_raises_invalid_postal_code(self, validator, incorrect_postal_code_address_data) -> None:
        with pytest.raises(ValueError) as ve:
            validator.validate(incorrect_postal_code_address_data)
        assert str(ve.value).startswith("Postal code does not exist:")

