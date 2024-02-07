import pytest

from app.data_loader.factory.address.validator.regex_validator import RegexValidator


@pytest.fixture
def validator() -> RegexValidator:
    return RegexValidator(r'^\d{2}-\d{3}$')
