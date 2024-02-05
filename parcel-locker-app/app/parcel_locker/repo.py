import logging
from typing import Optional

from app.parcel_locker.model import ParcelLocker, Locker, Category
from app.persistence.crud_repo import CrudRepo

logging.basicConfig(level=logging.INFO)


class ParcelLockerRepo(CrudRepo[ParcelLocker]):
    """
    This class contains methods to manage and handle the parcel locker data.
    """

    def __init__(self, connection) -> None:
        """
        Method initializes class attributes with ones provided
        :param connection: The connection object needed to connect with the database
        """
        super().__init__(connection, ParcelLocker)

    def find_one_by_address_id(self, address_id: int) -> ParcelLocker:
        """
        This method gets a single parcel locker based on its address ID.
        :param address_id:
        :return:
        """
        try:
            sql = f"select * from parcel_lockers p where p.address_id = {address_id} ;"

            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return ParcelLocker(*result)
                else:
                    raise ValueError(f"No ParcelLocker found with address_id: {address_id}")
        except Exception as error:
            logging.error('Find by address id error')
            logging.error(error)
        finally:
            if connection_object is not None and connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_all_by_address_id(self, address_ids: list[int]) -> list[ParcelLocker]:
        """
        This method is used to find all instances of a parcel locker based on multiple address IDs
        :param address_ids:
        :return:
        """
        try:
            if len(address_ids) == 1:
                sql = f"select * from parcel_lockers p where p.address_id = {address_ids[0]} ;"
            else:
                sql = f"select * from parcel_lockers p where p.address_id in {tuple(address_ids)} ;"
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                return [ParcelLocker(*row) for row in cursor.fetchall()]
        except Exception as error:
            logging.error('Find all by address id error')
            logging.error(error)
        finally:
            if connection_object is not None and connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def has_at_least_one_empty_locker_with_category(self, pl_id: int, category_id: int) -> bool:
        """
        This method checks if there are empty lockers of given category in a parcel locker of given ID
        :param pl_id:
        :param category_id:
        :return:
        """
        try:
            sql = f"""
                select *
                from parcel_lockers pl
                inner join lockers l on pl._id = l.parcel_locker_id
                where pl._id = {pl_id}
                and l.category_id = {category_id}
                and l.is_empty = false;
            """

            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql, {'parcel_locker_id': pl_id, 'category_id': category_id})
                result = cursor.fetchone()
                return result is not None  # True if at least one empty locker with the given category exists
        except Exception as error:
            logging.error('Has at least one empty locker with category error')
            logging.error(error)
        finally:
            if connection_object is not None and connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def get_lockers_info(self) -> list[tuple[int, int, int, bool]]:
        """
        This method gets data describing parcel lockers state - availability of lockers from all categories
        :return:
        """
        try:
            sql = """
                select p._id as parcel_locker_id, l._id as locker_id, l.category_id, l.is_empty
                from parcel_lockers p
                inner join lockers l on p._id = l.parcel_locker_id
            """

            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as error:
            logging.error('Get lockers info error')
            logging.error(error)
        finally:
            if connection_object is not None and connection_object.is_connected():
                cursor.close()
                connection_object.close()


class LockerRepo(CrudRepo[Locker]):
    """
    This class contains methods for handling locker data
    """

    def __init__(self, connection) -> None:
        """
        Method initializes class attributes with ones provided
        :param connection: The connection object needed to connect with the database
        """
        super().__init__(connection, Locker)

    def update_locker(self, locker_id: int, updated_locker: Locker) -> Optional[Locker]:
        """
        Updates a locker with the given ID using the provided updated locker object
        :param locker_id: ID of the locker to update
        :param updated_locker: Updated Locker object
        :return: Updated Locker object or None if the locker doesn't exist or an error occurs
        """
        connection_object = None
        try:
            existing_locker = self.find_one(locker_id)
            if existing_locker:
                # Validate the input locker
                if not isinstance(updated_locker, Locker):
                    raise ValueError("Input is not a valid Locker object.")

                # Construct the SQL query with placeholders
                sql = f"""
                    update {self._table_name()}
                    set is_empty=%s, not_empty_start_date_time=%s, parcel_locker_id=%s, category_id=%s
                    where _id = %s;
                """
                values = (
                    updated_locker.is_empty,
                    updated_locker.not_empty_start_date_time,
                    updated_locker.parcel_locker_id,
                    updated_locker.category_id,
                    locker_id
                )

                connection_object = self._connection_pool.get_connection()

                if connection_object.is_connected():
                    cursor = connection_object.cursor()
                    cursor.execute(sql, values)
                    connection_object.commit()

                    return self.find_one(locker_id)
            else:
                raise ValueError(f"Locker with ID {locker_id} does not exist.")

        except Exception as error:
            logging.error('Update locker error')
            logging.error(error)
            return None
        finally:
            if connection_object and connection_object.is_connected():
                cursor.close()
                connection_object.close()


class CategoryRepo(CrudRepo[Category]):

    def __init__(self, connection) -> None:
        """
        Method initializes class attributes with ones provided
        :param connection: The connection object needed to connect with the database
        """
        super().__init__(connection, Category)
