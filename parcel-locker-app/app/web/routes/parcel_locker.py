from flask import Blueprint, request, Flask

from app.configuration import parcel_locker_service
from app.parcel_locker.dto import CreateParcelWithLockersDto
from app.configuration import category_repo
from app.parcel_locker.model import Category


parcel_lockers_bp = Blueprint("parcel_lockers", __name__, url_prefix='/parcel_lockers')


def configure_routes(app: Flask) -> None:
    """
    Function is used to configure and create parcel locker routes
    Attributes:
        app   -    Flask object needed for web configuration
    :param app:
    :return:
    """
    # -----------------------------------------------------------------------------------
    # ADDING PARCEL LOCKER
    # -----------------------------------------------------------------------------------
    @parcel_lockers_bp.route('/', methods=['POST'])
    def add_parcel_locker():
        create_parcel_with_lockers_dto = CreateParcelWithLockersDto.from_dict(request.get_json())
        return {"parcel_locker_id": parcel_locker_service.add_parcel_locker(create_parcel_with_lockers_dto)}, 201

    # -----------------------------------------------------------------------------------
    # IS THERE A LOCKER OF GIVEN CATEGORY UNDER GIVEN ADDRESS
    # -----------------------------------------------------------------------------------
    @parcel_lockers_bp.route("/category/<int:category_id>/address/<int:address_id>", methods=['GET'])
    def get_first_empty_locker_with_category(category_id: int, address_id: int):
        return {"empty_locker_id": parcel_locker_service.get_first_empty_locker_with_category(category_id, address_id)}, 200

    # -----------------------------------------------------------------------------------
    # ADDING CATEGORIES
    # -----------------------------------------------------------------------------------
    @parcel_lockers_bp.route("/category", methods=['POST'])
    def create_categories():
        category = Category.from_dict(request.get_json())
        return {"category id": category_repo.insert(category)}, 200

    # -----------------------------------------------------------------------------------
    # FILLING UP LOCKER
    # -----------------------------------------------------------------------------------
    @parcel_lockers_bp.route("/fill_locker/category_id/<int:category_id>/address_id/<int:address_id>", methods=['POST'])
    def fill_up_locker(category_id: int, address_id: int):
        return {"Filled locker id": parcel_locker_service.fill_up_locker(category_id, address_id)}, 200

    # -----------------------------------------------------------------------------------
    # REMOVING LOCKERS WITH EXCEEDED TIME
    # -----------------------------------------------------------------------------------
    @parcel_lockers_bp.route("/locker/remove/limit_hours/<int:limit_hours>", methods=['POST'])
    def remove_lockers_with_exceeded_time(limit_hours: int):
        return {"Removed content lockers ids": parcel_locker_service.remove_lockers_with_exceeded_time(limit_hours)}, 200
