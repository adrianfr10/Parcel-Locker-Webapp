from app.persistence.relational.repository import CustomerRepository, CountryRepository
from app.persistence.relational.model import Customer
from app.service.dto import CreateCustomerDto, GetCustomerDto
from dataclasses import dataclass
import logging


@dataclass
class CustomersService:
    """
    Service class handling customer-related operations.

    Attributes:
    -----------
    customer_repository : CustomerRepository
        Repository for customer data operations.
    country_repository : CountryRepository
        Repository for country data operations.
    """
    customer_repository: CustomerRepository
    country_repository: CountryRepository

    def add_customer(self, create_customer_dto: CreateCustomerDto) -> GetCustomerDto:
        """
         Adds a new customer based on the provided DTO.

        Parameters:
        -----------
        create_customer_dto : CreateCustomerDto
            Data Transfer Object (DTO) containing details of the new customer.

        Returns:
        --------
        GetCustomerDto
            Data Transfer Object (DTO) representing the added customer.

        Raises:
        -------
        AttributeError
            If the country name from the DTO is not found in the country repository.
        """
        country_from_db = self.country_repository.find_by_name(create_customer_dto.country_name)
        if not country_from_db:
            raise AttributeError('Country name not found')

        logging.info(self.customer_repository.find_by_id(id_=1))

        customer = Customer(
            name=create_customer_dto.name,
            age=create_customer_dto.age,
            country=country_from_db
        )
        self.customer_repository.save_or_update(customer)
        return customer.to_entity()
