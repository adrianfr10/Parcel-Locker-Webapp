import re

from app.data_loader.factory.address.validator.validator import Validator


class TestValidatorWorksCorrectly:

    def test_when_matches_regex_is_correct(self) -> None:
        assert Validator.matches_regex('[A-Za-z ]', 'test string')

    def test_when_is_greater_than_is_not_correct(self) -> None:
        assert Validator.is_greater_than(5, 50)


class TestValidatorWithIncorrectData:

    def test_when_matches_regex_does_not_match(self) -> None:
        assert Validator.matches_regex(r'^[A-Z]$', 'test') is False

    def test_when_is_greater_than_not_correct(self) -> None:
        assert Validator.is_greater_than(50, 5) is False
