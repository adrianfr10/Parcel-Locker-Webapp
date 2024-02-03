import logging
import httpx
from typing import Any
from app.data_loader.factory.address.validator.validator import Validator

logging.basicConfig(level=logging.INFO)


class RegexValidator(Validator):
    """
    Validator class implementing regex-based validation for address data.
    """

    def __init__(self, regex: str) -> None:
        """
        Initializes the RegexValidator, with regex field
        :param regex: Regular expression pattern used for validation.
        """
        self.regex = regex

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validates address data based on regex patterns and external API calls.
        Raises:
            ValueError: If validation errors occur or the postal code doesn't exist.
        :param data: address data to be validated.
        :return: Validated address data.
        """
        errors = {}

        if not data['postal_code']:
            errors['postal_code'] = 'required'
        if not isinstance(data["address_id"], int):
            raise ValueError("Id must be an int")

        if not Validator.matches_regex(self.regex, data['postal_code']):
            errors['postal_code'] = 'incorrect format'

        if errors:
            raise ValueError("Validation errors!")

        postal_code = data['postal_code']
        api_url = f"https://kodpocztowy.intami.pl/api/{postal_code}"
        response = httpx.get(api_url)
        if response.status_code == 404:
            raise ValueError(f"Postal code does not exist: {postal_code}")

        results = response.json()
        logging.info(results)

        return data
