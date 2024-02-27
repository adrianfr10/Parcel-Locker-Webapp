from dataclasses import dataclass
from typing import Any, Self


@dataclass
class CreateCustomerDto:
    """
     Data Transfer Object (DTO) class for creating a customer.

     Attributes:
     -----------
     name : str
         Name of the customer.
     age : int
         Age of the customer.
     country_name : str
         Name of the country.
    """
    name: str
    age: int
    country_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string")
        if not isinstance(self.age, int):
            raise ValueError("Age must be an integer")
        if not isinstance(self.country_name, str):
            raise ValueError("Country name must be a string")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Creates a CreateCustomerDto instance from a dictionary.
        """
        return cls(name=data["name"], age=data["age"], country_name=data["country_name"])


@dataclass
class GetCustomerDto:
    """
     Data Transfer Object (DTO) class for getting customer details.

     Attributes:
     -----------
     name : str
         Name of the customer.
     age : int
         Age of the customer.
     country_id : int
         ID of the country.
    """

    name: str
    age: int
    country_id: int

    def to_dict(self) -> dict:
        """
        Converts the GetCustomerDto instance to a dictionary.
        """
        return self.__dict__


@dataclass
class CreateCustomerOrderDto:
    """
    Data Transfer Object (DTO) class for creating a customer order.

    Attributes:
    -----------
    customer_id : str
        ID of the customer.
    product_id : str
        ID of the product.
    quantity : int
        Quantity of the product in the order.
    parcel_address_id : int
        ID of the parcel address.
    """
    customer_id: str
    product_id: str
    quantity: int
    parcel_address_id: int

    def __post_init__(self) -> None:
        if not isinstance(self.customer_id, str):
            raise ValueError("Customer id must be an integer")
        if not isinstance(self.product_id, str):
            raise ValueError("Product id in NoSQL DB must be a string")
        if not isinstance(self.quantity, int):
            raise ValueError("Quantity must be an integer")
        if not isinstance(self.parcel_address_id, int):
            raise ValueError("Parcel address id must be an int")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Creates a CreateCustomerOrderDto instance from a dictionary.
        """
        return cls(**data)


@dataclass
class GetCustomerOrderDto:
    """
       Data Transfer Object (DTO) class for getting customer order details.

    Attributes:
    -----------
    order_id : int
        ID of the order.

    """
    order_id: int

    def to_dict(self) -> dict:
        """
        Converts the GetCustomerOrderDto instance to a dictionary.
        """
        return self.__dict__
