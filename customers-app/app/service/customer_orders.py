from app.persistence.nosql.repository import CustomerOrderRepository, CustomerFavouriteProducts, ProductRepository
from app.persistence.nosql.model import CustomerOrder, ProductItem, Product
from app.persistence.relational.repository import CustomerRepository
from app.service.dto import CreateCustomerOrderDto, GetCustomerOrderDto
from app.web.parcel_locker_requests import get_available_locker
from dataclasses import dataclass


@dataclass
class CustomerOrdersService:
    """
       Service class handling customer order-related operations.

    Attributes:
    -----------
    customer_repository : CustomerRepository
        Repository for customer data operations.
    customer_order_repository : CustomerOrderRepository
        Repository for customer order data operations.
    product_repository : ProductRepository
        Repository for product data operations.

    """
    customer_repository: CustomerRepository
    customer_order_repository: CustomerOrderRepository
    product_repository: ProductRepository

    def add_customer_order(self, create_customer_order_dto: CreateCustomerOrderDto) -> GetCustomerOrderDto:
        """
        Adds a new customer order based on the provided DTO.
        Parameters:
        -----------
        create_customer_order_dto : CreateCustomerOrderDto
            Data Transfer Object (DTO) containing details of the new customer order.

        Returns:
        --------
        GetCustomerOrderDto
            Data Transfer Object (DTO) representing the added customer order.

        Raises:
        -------
        AttributeError
            If the customer or product ID from the DTO is not found in the respective repositories.

        """
        customer_from_db = self.customer_repository.find_by_id(create_customer_order_dto.customer_id)
        product_from_db = self.product_repository.find_by_id(create_customer_order_dto.product_id)

        if not customer_from_db:
            raise AttributeError('Customer not found')

        if not product_from_db:
            raise AttributeError('Product not found')

        locker_id = get_available_locker(
            product_from_db.parcel_locker_category_id,
            create_customer_order_dto.parcel_address_id).get("empty_locker_id")

        product_item = ProductItem(product=product_from_db, quantity=create_customer_order_dto.quantity)
        customer_order = CustomerOrder(
            customer_id=customer_from_db.id,
            locker_id=locker_id,
            product_item=product_item
        )
        inserted_customer_order = self.customer_order_repository.add(customer_order)
        return GetCustomerOrderDto(order_id=inserted_customer_order.id)
