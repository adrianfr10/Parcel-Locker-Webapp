from abc import ABC, abstractmethod

import inflection
from sqlalchemy import (
    Engine,
    select
)
from sqlalchemy.orm import (
    Session,
    sessionmaker
)

from app.persistence.relational.model import Customer, Country


class CrudRepository[T](ABC):
    @abstractmethod
    def save_or_update(self, entity: T) -> None:
        pass

    @abstractmethod
    def save_or_update_many(self, entities: list[T]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass

# -----------------------------------------------------------------------
# [ CRUD REPO - ORM ]
# -----------------------------------------------------------------------


class CrudRepositoryORM[T](CrudRepository[T]):

    def __init__(self, engine: Engine) -> None:
        """
        Initialize the CRUD Repository.
        Parameters:
        -----------
        engine : Engine
            Database engine for executing database operations.
        entity_type : Any
            Type of the entity being operated on.
        """
        self._engine = engine
        self._entity_type = self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, item: T) -> None:
        """
        Saves or updates a single item in the database.
        Parameters:
        -----------
        item : Any
            Item to be saved or updated.
        """
        with self._create_session() as session, session.begin():
            session.add(session.merge(item) if item.id else item)

    def save_or_update_many(self, items: list[T]) -> None:
        """
        Saves or updates multiple items in the database.
        Parameters:
        -----------
        items : list[Any]
            List of items to be saved or updated.
        """
        with self._create_session() as session, session.begin():
            session.add_all([session.merge(item) if item.id else item for item in items])

    def find_by_id(self, id_: int) -> T | None:
        """
        Finds an item by its ID.
        """
        with self._create_session() as session:
            statement = select(self._entity_type).filter_by(id=id_)
            return session.execute(statement).scalars().first()

    def find_all(self) -> list[T]:
        """
         Finds all items of the specified entity type.
        """
        with self._create_session() as session:
            statement = select(self._entity_type)
            return list(session.execute(statement).scalars().all())

    def delete_by_id(self, id_: int) -> None:
        """
         Deletes an item by its ID.
        """
        with self._create_session() as session, session.begin():
            statement = select(self._entity_type).filter_by(id=id_)
            item_to_delete = session.execute(statement).scalars().first()
            if not item_to_delete:
                raise ValueError(f"Item with id:{id_} does not exist")
            session.delete(item_to_delete)

    def delete_all(self) -> None:
        """
        Delete all items.
        """
        with self._create_session() as session, session.begin():
            statement = select(self._entity_type)
            items_to_delete = session.execute(statement).scalars().all()
            for item in items_to_delete:
                session.delete(item)

    # -----------------------------------------------------------------------------
    # AUXILIARY METHODS
    # -----------------------------------------------------------------------------

    def _create_session(self) -> Session:
        """
        Creates a database session.
        """
        Session = sessionmaker(bind=self._engine, expire_on_commit=False)
        return Session()

    def __tablename__(self) -> str:
        """
         Returns the table name for the entity type.
        """
        return inflection.tableize(self._entity_type.__name__)


class CustomerRepository(CrudRepositoryORM[Customer]):
    """
     Repository handling database operations for Customer entities.
     Inherits from CrudRepository and extends its functionality.

    """
    def __init__(self, engine: Engine) -> None:
        """
        Initialize the Customer Repository.
        Parameters:
        -----------
        engine : Engine
            Database engine for executing database operations.
        """
        super().__init__(engine)


class CountryRepository(CrudRepositoryORM[Country]):
    """
    Repository handling database operations for Country entities.
    Inherits from CrudRepository and extends its functionality.
    """
    def __init__(self, engine: Engine) -> None:
        """
        Initialize the Country Repository.
        Parameters:
        -----------
        engine : Engine
            Database engine for executing database operations.
        """
        super().__init__(engine)

    def find_by_name(self, name: str) -> Customer | None:
        """
         Finds a country by name in the database.
        Parameters:
        -----------
        name : str
            Name of the country.
        """
        with self._create_session() as session:
            statement = select(self._entity_type).filter_by(name=name)
            return session.execute(statement).scalars().first()
