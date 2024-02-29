from app.persistence.relational.configuration import engine
from app.persistence.relational.repository import CustomerRepository, CountryRepository
from app.persistence.nosql.repository import (
    ProductRepository,
    CustomerOrderRepository,
    CustomerFavouriteProductsRepository
)
from app.service.customers import CustomersService
from app.service.customer_orders import CustomerOrdersService


# sql repo
customer_repository = CustomerRepository(engine)
country_repository = CountryRepository(engine)

# nosql repo
product_repository = ProductRepository()
customer_order_repository = CustomerOrderRepository()

# services initialization
customers_service = CustomersService(customer_repository, country_repository)
customer_orders_service = CustomerOrdersService(customer_repository, customer_order_repository, product_repository)
