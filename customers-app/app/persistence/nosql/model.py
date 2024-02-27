from datetime import datetime
from typing import Any, Self

from mongoengine import (
    Document,
    StringField,
    EmbeddedDocument,
    ReferenceField,
    ListField,
    EmbeddedDocumentField,
    IntField,
    DateTimeField,
    DecimalField,
    CASCADE
)


class Product(Document):
    """
    This class represents a product object in a non-relational database
    Attributes:
        name    -   name of the product
        price   -   price value of the product
        parcel_locker_category_id   -    ID of the category to which the locker you want to
        store the product belongs. Represented by the id_ attribute in the Category entity
    """
    name = StringField(max_length=50, required=True)
    price = DecimalField(precision=2)
    parcel_locker_category_id = IntField()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Method converts raw data into Product object
        """
        return cls(**data)


class ProductItem(EmbeddedDocument):
    """
    This class represents a product item object in a non-relational database
    Attributes:
        product    -    The product object reference
        quantity   -    Quantity the product
    """
    product = ReferenceField(Product)
    quantity = IntField()


class CustomerOrder(Document):
    """
    This class represents a customer order object in a non-relational database
    Attributes:
        customer_id    -    ID of the customer
        locker_id      -    ID of the locker that customer uses
        order_date     -    Date of the order placement
        product_item   -    Representation of a product item from above
    """
    customer_id = IntField()
    locker_id = IntField()
    order_date = DateTimeField(default=datetime.now)
    product_item = EmbeddedDocumentField(ProductItem)


class CustomerFavouriteProducts(Document):
    """
    This class represents a customers' favourite products in a non-relational database
    Attributes:
        customer_id    -    ID of the customer
        products       -    Collection of customers' favourite products
    """
    customer_id = IntField()
    products = ListField(ReferenceField(Product,  reverse_delete_rule=CASCADE))
