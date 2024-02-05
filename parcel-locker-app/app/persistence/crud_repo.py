from abc import ABC, abstractmethod

from mysql.connector import Error
from datetime import datetime, date

import logging
import inflection

logging.basicConfig(level=logging.INFO)


class CrudRepoAbs[T](ABC):
    """
    An abstract class defining the basic CRUD (Create, Read, Update, Delete) operations for a repository.
    Subclasses are expected to implement these methods based on the specific data type they handle.
    """

    @abstractmethod
    def insert(self, item: T) -> int:
        pass

    @abstractmethod
    def insert_many(self, items: list[T]) -> list[int]:
        pass

    @abstractmethod
    def update(self, item_id: int, item: T) -> int:
        pass

    @abstractmethod
    def find_n_last(self, n: int) -> list[T]:
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def find_one(self, item_id: int) -> T:
        pass

    @abstractmethod
    def delete_all(self) -> list[int] | None:
        pass

    @abstractmethod
    def delete_one(self, item_id: int) -> int:
        pass

    @abstractmethod
    def delete_all_by_id(self, ids: list[int]) -> list[int]:
        pass


class CrudRepo[T](CrudRepoAbs[T]):
    """
    Base class defining the CRUD operations on entities
    """

    def __init__(self, connection, entity_type) -> None:
        """
        Initializing class attributes with ones passed to init method
        :param connection: Connection object needed to connect with the database
        :param entity_type: Type of entity, the operations will be performed on
        """
        self._connection_pool = connection
        self._entity = entity_type
        self._entity_type = type(entity_type())

    def insert(self, item: T) -> int:
        """
        Method used to insert single entity into the database
        :param item:
        :return:
        """
        try:
            sql = f"insert into {self._table_name()} {self._column_names_for_insert()} values {CrudRepo._column_values_for_insert(item)};"
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                connection_object.commit()
                return cursor.lastrowid

        except Error as error:
            logging.error('Insert error')
            logging.error(error)
            return -1

        finally:
            if connection_object and connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def insert_many(self, items: list[T]) -> list[int]:
        """
        Method used to insert many entities into the database
        :param items:
        :return:
        """
        connection_object = None
        try:
            values = ', '.join([CrudRepo._column_values_for_insert(item) for item in items])
            sql = f"insert into {self._table_name()} {self._column_names_for_insert()} values {values}"
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                connection_object.commit()
                return [item._id for item in self.find_n_last(len(items))]

        except Error as error:
            logging.error('Insert many error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def update(self, item_id: int, item: T) -> int:
        """
        Method used to update single entity with a new one based on its ID
        :param item_id:
        :param item:
        :return:
        """
        connection_object = None
        try:
            existing_item = self.find_one(item_id)
            if existing_item:

                sql = f"update {self._table_name()} set {CrudRepo._column_names_and_values_for_update(item)} where _id = {item_id};"
                connection_object = self._connection_pool.get_connection()

                if connection_object.is_connected():
                    cursor = connection_object.cursor()
                    cursor.execute(sql)
                    connection_object.commit()
                    return self.find_one(item_id)
            else:
                raise ValueError(f"Item with ID {item_id} does not exist.")

        except Error as error:
            logging.error('Update error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_n_last(self, number: int) -> list[T]:
        """
        Method is used to find a certain number of entities from the bottom records in the database
        :param number:
        :return:
        """
        connection_object = None
        try:
            sql = f'select * from {self._table_name()} order by _id desc limit {number}'
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                return [self._entity(*row) for row in cursor.fetchall()]

        except Error as error:
            logging.error('Find n last error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_all(self) -> list[T]:
        """
        Method is used to find all entities in the database
        :return:
        """
        connection_object = None
        try:
            sql = f'select * from {self._table_name()}'
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                return [self._entity(*row) for row in cursor.fetchall()]

        except Error as error:
            logging.error('Find all error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_one(self, item_id: int) -> T:
        """
        Method is used to find single entity with given ID
        :param item_id:
        :return:
        """
        connection_object = None
        try:
            sql = f'select * from {self._table_name()} where _id = {item_id}'
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                result = cursor.fetchone()
                if result is None:
                    raise RuntimeError('Cannot get row from db')
                return self._entity(*result)

        except Error as error:
            logging.error('Find one error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def delete_one(self, item_id: int) -> int:
        """
        Method is used to delete single entity with given ID
        :param item_id:
        :return:
        """
        connection_object = None
        try:
            self.find_one(item_id)
            sql = f'delete from {self._table_name()} where _id = {item_id}'
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                connection_object.commit()
                return item_id

        except Error as error:
            logging.error('Delete one error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def delete_all(self) -> list[int] | None:
        """
         Method is used to delete all entities from a database
        :return:
        """
        try:
            all_items_ids_before_delete = [item._id for item in self.find_all()]
            sql = f'delete from {self._table_name()} where _id >= 1'
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                connection_object.commit()
                return all_items_ids_before_delete

        except Error as error:
            logging.error('Delete all error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def delete_all_by_id(self, ids: list[int]) -> list[int]:
        """
        Method is used to delete many entities with given IDs
        :param ids:
        :return:
        """
        connection_object = None
        try:
            ids_to_delete = f'({", ".join([str(i)for i in ids])})'
            sql = f'delete from {self._table_name()} where _id in {ids_to_delete}'
            connection_object = self._connection_pool.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(sql)
                connection_object.commit()
                return ids

        except Error as error:
            logging.error('Delete all by id error')
            logging.error(error)

        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    # -------------------------------------------------------------------------------------
    # Additional methods
    # -------------------------------------------------------------------------------------
    def _table_name(self) -> str:
        """
        Function returns table name related to the model
        :return:
        """
        return inflection.tableize(self._entity_type.__name__)

    def _field_names(self) -> list[str]:
        """
        Function returns column names needed to generate sql queries
        :return:
        """
        return self._entity().__dict__.keys()

    def _column_names_for_insert(self) -> str:
        """
        Function prepares column names for insert - eliminating id, which is not needed when inserting
        :return:
        """
        field_names_without_id = [field for field in self._field_names() if field.lower() != '_id']
        return f"({', '.join(field_names_without_id)})"

    @staticmethod
    def _column_values_for_insert(item: T) -> str:
        """
        This method returns a list of values that we will insert within sql
        :param item:
        :return:
        """

        def to_str(entry) -> str:
            return f"'{entry[1]}'" if isinstance(entry[1], (str, datetime, date)) else str(entry[1])

        return f"({', '.join([to_str(entry) for entry in item.__dict__.items() if entry[0].lower() != '_id'])})".replace('None', 'NULL')

    @staticmethod
    def _column_names_and_values_for_update(entity: T) -> str:
        """
        Function prepares column names and values for update
        :param entity:
        :return:
        """
        def to_str(entry) -> str:
            return entry[0] + '=' + (f"'{entry[1]}'" if isinstance(entry[1], (str, datetime, date)) else str(entry[1]))

        return ', '.join([to_str(item) for item in entity.__dict__.items() if item[0].lower() != '_id'])
