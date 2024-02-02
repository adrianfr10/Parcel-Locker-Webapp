from dataclasses import dataclass
from app.address.model import Address


@dataclass(eq=False)
class AddressService:
    """
    This class is a service class for managing address-related operations
    Attributes:
        addresses   -   represents a collection of addresses where parcel lockers are located
    """
    addresses: list[Address]

    def get_address_by_id(self, address_id: int) -> Address:
        """
        Method returns an address with given id
        :param address_id:
        :return:
        """
        found_addresses = [address for address in self.addresses if address.has_id(address_id)]
        if len(found_addresses) != 1:
            raise ValueError(f'No unique address with id: {address_id}')

        return found_addresses[0]

    def get_all_addresses_from_province_and_city(self, province: str, city: str) -> list[Address]:
        """
        Method returns a list of addresses with given province and city
        :param province:
        :param city:
        :return:
        """
        if not isinstance(province, str) and not isinstance(city, str):
            raise ValueError("Province and city must be strings")
        return [a for a in self.addresses if a.has_province_and_city(province, city)]

    def get_address_closest_to(self, destination_address: Address) -> Address | None:
        """
        Method returns an address closest to the address given
        :param destination_address:
        :return:
        """
        return min(self.addresses, key=lambda adr: adr.get_distance(destination_address), default=None)
