import json
from dataclasses import dataclass
from typing import Any, Self


@dataclass
class CreateParcelWithLockersDto:
    """
    This class is a representation of a Data Transfer Object, used for
    Attributes:
        address_id  -   ID of the address
        lockers     -   Number of lockers of given category ID
    """
    address_id: int
    # assuming that whoever specifies the category id, knows that it exists.
    lockers: dict[str, int]  # {category_id: amount_of_lockers}

    def __post_init__(self) -> None:
        """
        Used to validate the dto data.
        :return:
        """

        if not isinstance(self.address_id, int):
            raise ValueError("Address id must be an integer")

        if not isinstance(self.lockers, dict):
            raise ValueError("Lockers must be a dictionary")

        for key, value in self.lockers.items():
            if not isinstance(key, str) or not isinstance(value, int):
                raise ValueError("Wrong key or value data type")

            if value < 0:
                raise ValueError("Number of lockers cannot be negative.")

    @classmethod
    def from_json(cls, json_data: str) -> Self:
        """
        Method converts data in JSON format into the CreateParcelWithLockersDto object
        :param json_data:
        :return:
        """
        res = json.loads(json_data)
        return cls(**res)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Method converts data as dict into the CreateParcelWithLockersDto object
        :param data:
        :return:
        """
        return cls(address_id=data["address_id"], lockers=data["lockers"])
