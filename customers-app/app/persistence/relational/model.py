from __future__ import annotations

from typing import Any, Self

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.relational.configuration import Base, create_session
from app.service.dto import GetCustomerDto


class Customer(Base):
    """
    This class represents a customer entity in the orm database
    Attributes:
        id: ID of the customer
        name: Name of the customer
        age: Age of the customer
        country_id: ID of the country of residence of the customer
        country: Residence country of the customer
    """
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]

    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    country: Mapped[Country] = relationship(back_populates='customers')

    def to_entity(self) -> GetCustomerDto:
        """
        This method converts class attributes: name, age and country_id
        into DTO
        """
        return GetCustomerDto(self.name, self.age, self.country_id)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Customer object.
        """
        return f'{self.id} ... {self.name} ... {self.age}'

    def __str__(self) -> str:
        """
        Returns a string representation of the Customer object.
        """
        return repr(self)


class Country(Base):
    """
    This class represents a country entity in the ORM database.

    Attributes:
        id: ID of the country
        name: Name of the country
        customers: List of customers associated with the country
    """
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    customers: Mapped[list[Customer]] = relationship(
        back_populates='country',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Country object.
        """
        return f'{self.id} ... {self.name}'

    def __str__(self) -> str:
        """
        Returns a string representation of the Country object.
        """
        return repr(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return Country(**data)

    def save_or_update(self) -> None:
        """
        Saves or updates the country in the database.

        """
        with create_session() as session, session.begin():
            session.add(session.merge(self) if self.id else self)

    def delete(self) -> None:
        """
        Deletes the country from the database.
        """
        with create_session() as session, session.begin():
            session.delete(self)

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        """
        Finds a country by its ID
        Args:
            id_ (int): ID of the country to find.
        Returns:
            Country | None: Found country or None if not found.

        """
        with create_session() as session:
            statement = select(Country).filter_by(id=id_)
            return session.execute(statement).scalars().first()

    @classmethod
    def find_by_name(cls, name: str) -> Self | None:
        """
         Finds a country by its name.
         Args:
             name (str): Name of the country to find.
         Returns:
             Country | None: Found country or None if not found.
         """
        with create_session() as session:
            statement = select(Country).filter_by(name=name)
            return session.execute(statement).scalars().first()

    @staticmethod
    def save_or_update_many(countries: list['Country']) -> None:
        """
         Saves or updates multiple countries in the database.
         Args:
             countries (list[Country]): List of countries to save or update.
         """
        with create_session() as session, session.begin():
            session.add_all([
                session.merge(country) if country.id else country
                for country in countries
            ])

    @staticmethod
    def find_all() -> list['Country']:
        """
        Retrieves all countries from the database.

        Returns:
            list[Country]: List of all countries.
        """
        with create_session() as session:
            statement = select(Country)
            return session.execute(statement).scalars().all()

    @staticmethod
    def delete_all() -> None:
        """
        Deletes all countries from the database.
        """
        with create_session() as session, session.begin():
            session.query(Country).delete()
