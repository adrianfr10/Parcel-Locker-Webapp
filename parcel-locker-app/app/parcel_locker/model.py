from dataclasses import dataclass, replace
from datetime import datetime
from typing import Self, Any


@dataclass(frozen=True)
class ParcelLocker:
    """
    Represents a parcel locker entity
    Attributes:
        _id  -  ID of the parcel locker
        address_id  -  ID of the address where parcel locker is located
    """
    _id: int = 0
    address_id: int = 0


@dataclass(frozen=True)
class Locker:
    """
    Represents a locker entity, a place where you put parcels when using parcel locker
    Attributes:
        _id         -                   ID of the locker
        is_empty    -                   Describes a binary state of the locker, that can be either empty or occupied
        not_empty_start_date_time   -   Indicates a date when the locker changed state to occupied
        parcel_locker_id    -           ID of the parcel locker, where the locker exists
        category_id     -               Represents the category of the locker, which is related to its dimensions
    """
    _id: int = 0
    is_empty: bool = False
    not_empty_start_date_time: float | None = None
    parcel_locker_id: int | None = None
    category_id: int | None = None

    @classmethod
    def with_not_empty_start_date(cls, original, new_value) -> Self:
        """
        Method is used to replace not_empty_start_date_time with new_value because of frozen
        dataclass restrictions
        :param original:
        :param new_value:
        :return:
        """
        return replace(original, not_empty_start_date_time=new_value)

    @classmethod
    def with_is_empty(cls, original, new_value) -> Self:
        """
        Method is used to replace is_empty attribute with new_value because of frozen
        dataclass restrictions
        :param original:
        :param new_value:
        :return:
        """
        return replace(original, is_empty=new_value)

    def update_not_empty_start_date_time(self, timestamp: float | None = None) -> Self:
        """
        Method to update the not_empty_start_date_time field.
        :param timestamp: New timestamp for not_empty_start_date_time
        :return: New Locker instance with updated not_empty_start_date_time
        """
        return Locker(
            self._id,
            self.is_empty,
            timestamp,
            self.parcel_locker_id,
            self.category_id
        )

    def change_state(self, is_empty: bool) -> Self:
        """
        Method is used to change a locker state from empty to occupied, and the other way around.
        :param is_empty:
        :return:
        """
        return Locker(
            self._id,
            is_empty,
            self.not_empty_start_date_time,
            self.parcel_locker_id,
            self.category_id
        )

    def is_not_empty_too_long(self, limit_hours: int) -> bool:
        """
        Method checks whether the parcel is not occupying the locker for longer that specified time
        :param limit_hours:
        :return:
        """
        return self.not_empty_start_date_time + limit_hours * 3600 < datetime.now().timestamp()


@dataclass(frozen=True)
class Category:
    """
    Represents a category entity that is tied to the locker
    Attributes:
        _id     -    ID of the category
        name    -    Name of the category
        height  -    Height of the locker
        weight  -    Max weight of the parcel
        dept    -   Depth of the locker
    """
    _id: int = 0
    name: str = ''
    height: float = 0.0
    weight: float = 0.0
    dept: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Method converts data as dict into the Category object
        :param data:
        :return:
        """
        return cls(name=data["name"], height=data["height"], weight=data["weight"], dept=data["dept"])
