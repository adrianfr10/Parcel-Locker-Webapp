from flask import request, Blueprint, Flask

from app.configuration import customers_service, customer_orders_service, product_repository, country_repository
from app.persistence.nosql.model import Product
from app.persistence.relational.model import Country
from app.service.dto import CreateCustomerDto, CreateCustomerOrderDto

cust_prod_blueprint = Blueprint("nosql", __name__, url_prefix="/nosql")


def configure_routes(app: Flask) -> None:
    """
    This function is used to create and configure routing for customer orders and products
    Arguments:
        app    -    an instance of Flask application
    """
    @app.route('/customer', methods=['POST'])
    def add_customer():
        inserted_customer = customers_service.add_customer(CreateCustomerDto.from_dict(data=request.get_json()))
        return inserted_customer.to_dict(), 201

    @app.route('/country/<string:country_name>', methods=['POST'])
    def add_country(country_name: str):
        inserted_country = country_repository.save_or_update(Country(name=country_name))
        return {"Successfully added:": country_name}, 200
    # -------------------------------------------------------------------
    # NoSQL routes
    # -------------------------------------------------------------------

    @cust_prod_blueprint.route('/products', methods=['POST'])
    def add_product():
        inserted_product = product_repository.add(Product.from_dict(request.get_json()))
        return {'id': str(inserted_product.id)}, 201

    @cust_prod_blueprint.route('/orders', methods=['POST'])
    def add_customer_order():
        inserted_customer_order = customer_orders_service.add_customer_order(
            CreateCustomerOrderDto.from_dict(request.get_json()))
        return {'id': str(inserted_customer_order.order_id)}, 201



