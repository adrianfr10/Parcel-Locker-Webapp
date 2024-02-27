import logging
from dataclasses import dataclass

from app.persistence.nosql.model import (
    Product,
    CustomerOrder,
    CustomerFavouriteProducts
)

logging.basicConfig(level=logging.INFO)


@dataclass
class ProductRepository:
    """
    This class is a repository for managing Product related operations.
    """
    @staticmethod
    def add(product: Product) -> None:
        """
        This method is used to add product into the database
        """
        return product.save()

    @staticmethod
    def find_by_id(product_id: str) -> Product:
        """
        This method is used to find a product by its ID
        """
        return Product.objects(id=product_id).first()


@dataclass
class CustomerOrderRepository:
    """
    This class is a repository for managing CustomerOrder related operations.
    """
    @staticmethod
    def add(customer_order: CustomerOrder) -> None:
        """
        This method is used to add customer order into the database
        """
        return customer_order.save()


@dataclass
class CustomerFavouriteProductsRepository:
    """
    This class is a repository for managing CustomerFavouriteProducts related operations.
    """
    @staticmethod
    def add(customer_favourite_products: CustomerFavouriteProducts) -> None:
        """
        This method is used to add customer favourite products into the database
        """
        return customer_favourite_products.save()
