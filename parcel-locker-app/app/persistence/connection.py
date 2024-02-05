import logging
import os
from typing import Self

from dotenv import load_dotenv
from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool

logging.basicConfig(level=logging.INFO)
load_dotenv()

connection = pooling.MySQLConnectionPool(
    pool_name='my_pool',
    pool_size=5,
    pool_reset_session=True,
    host=os.getenv('HOST'),
    database=os.getenv('DATABASE'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    port=int(os.getenv('PORT'))
)


class MySQLConnectionPoolBuilder:
    """
    This class implements a Builder design pattern for creating and managing connection for the database
    """
    def __init__(self):
        """
        Initializing the pool config with data from environmental variables
        """
        self._pool_config = {
            'pool_name': 'my_connection_pool',
            'pool_size': 5,
            'pool_reset_session': True,
            'host': os.getenv('HOST'),
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
            'database': os.getenv('DATABASE'),
            'port': int(os.getenv('PORT'))
        }

    def set_pool_size(self, new_size: int) -> Self:
        """
        Methods sets pool size with new size provided
        :param new_size:
        :return:
        """
        self._pool_config['pool_size'] = new_size
        return self

    def set_host(self, new_host: str) -> Self:
        """
        Method sets host with new host provided
        :param new_host:
        :return:
        """
        self._pool_config['host'] = new_host
        return self

    def set_user(self, new_user: str) -> Self:
        """
        Method sets username with new username provided
        :param new_user:
        :return:
        """
        self._pool_config['user'] = new_user
        return self

    def set_password(self, new_password: str) -> Self:
        """
        Method sets password with new password provided
        :param new_password:
        :return:
        """
        self._pool_config['password'] = new_password
        return self

    def set_database(self, new_database: str) -> Self:
        """
        Method sets database name with new name provided
        :param new_database:
        :return:
        """
        self._pool_config['database'] = new_database
        return self

    def set_port(self, new_port: int) -> Self:
        """
        Method sets database port with new port provided
        :param new_port:
        :return:
        """
        self._pool_config['port'] = new_port
        return self

    def build(self) -> MySQLConnectionPool:
        """
        Method is used to build the connection pool with set config
        :return:
        """
        print(self._pool_config)
        return MySQLConnectionPool(**self._pool_config)
