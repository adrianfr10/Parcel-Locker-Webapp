import math
from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True)
class Address:
    """
    This class is used to represent the address of a parcel locker.
    Attributes:
        address_id  -   ID of the address
        province    -   province in which the address is located
        city        -   city in which the address is located
        postal_code -   postal code of the area where the address is located
        street      -   street of the address
        coord_x     -   longitude of the address in the geographic coordinate system
        coord_y     -   latitude of the address in the geographic coordinate system
    """
    address_id: int
    province: str
    city: str
    postal_code: str
    street: str
    coord_x: float
    coord_y: float

    def has_id(self, address_id: int) -> bool:
        """
        Method checks if address has given id
        :param address_id:
        :return:
        """
        return self.address_id == address_id

    def has_province_and_city(self, province: str, city: str) -> bool:
        """
        Method checks if address has given province and city
        :param province:
        :param city:
        :return:
        """
        return self.province == province and self.city == city

    def get_distance(self, address: Self) -> float:
        """
        Method returns a distance in kilometres between two address coordinates,
        :param address:
        :return:
        """
        lat1 = self.coord_y
        long1 = self.coord_x
        lat2 = address.coord_y
        long2 = address.coord_x

        degree_to_rad = float(math.pi / 180.0)

        d_lat = (lat2 - lat1) * degree_to_rad
        d_long = (long2 - long1) * degree_to_rad

        a = pow(math.sin(d_lat / 2), 2) + math.cos(lat1 * degree_to_rad) \
            * math.cos(lat2 * degree_to_rad) * pow(math.sin(d_long / 2), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 6367 * c

    @classmethod
    def from_dict(cls, address_data: dict[str, Any]) -> Self:
        """
        Method converts address from dict data into Address object
        :param address_data:
        :return:
        """
        return Address(**address_data)
