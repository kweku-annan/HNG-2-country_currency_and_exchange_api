#!/usr/bin/env python
"""Database Storage Operations"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from api.models.countries import Country, Base
from config import Config

class DBStorage:
    """Manages storage of SQLALchemy database operations"""
    __engine = None
    __session = None  # Session class instance

    def __init__(self):
        """Creates the engine and session"""
        self.__engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session


    def save(self, obj):
        """Saves an object to the database"""
        try:
            self.__session.add(obj)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def exists(self, name):
        """Checks if a Country with the given value or name exists"""
        if self.__session.query(Country).filter(Country.name.ilike(name)).first():
            return True
        return False

    def get_by_name(self, name):
        """Retrieves a country by a specified value"""
        return self.__session.query(Country).filter(Country.name.ilike(name)).first()

    def get_all(self, filters=None):
        """Retrieves all Country records, optionally filtered by criteria"""
        query = self.__session.query(Country)
        if filters:
            for attr, value in filters.items():
                if attr == 'currency':
                    query = query.filter(Country.currency_code.ilike(value))
                elif attr == 'sort':
                    if value == 'gdp_desc':
                        query = query.order_by(Country.estimated_gdp.desc())
                    elif value == 'gdp_asc':
                        query = query.order_by(Country.estimated_gdp.asc())
                else:
                    query = query.filter(getattr(Country, attr).ilike(value))

        return query.all()

    def delete(self, name):
        """Deletes a country by name"""
        country = self.__session.query(Country).filter_by(name=name).first()
        if country:
            try:
                self.__session.delete(country)
                self.__session.commit()
                return True
            except Exception as e:
                self.__session.rollback()
                raise e

        return False

    def status(self):
        """Show total countries and last refresh timestamp"""
        total_countries = self.__session.query(Country).count()
        last_refreshed = self.__session.query(Country).order_by(Country.last_refreshed_at.desc()).first()
        last_refreshed_at = last_refreshed.last_refreshed_at if last_refreshed else None
        return {
            "total_countries": total_countries,
            "last_refreshed_at": last_refreshed_at.replace(microsecond=0).isoformat() + 'Z'
        }

    def image_data(self):
        """
        Generates data to be used in image generation for:
        - Total number of countries
        - Top 5 countries by estimated GDP
        - Time of last data refresh
        :return: JSON
        """
        total_countries = self.__session.query(Country).count()
        top_countries = self.__session.query(Country).order_by(Country.estimated_gdp.desc()).limit(5).all()
        last_refreshed = self.__session.query(Country).order_by(Country.last_refreshed_at.desc()).first()
        last_refreshed_at = last_refreshed.last_refreshed_at if last_refreshed else None

        data = {
            "total_countries": total_countries,
            "top_countries_by_gdp": [
                {
                    "name": country.name,
                    "estimated_gdp": float(country.estimated_gdp) if country.estimated_gdp else None
                } for country in top_countries
            ],
            "last_refreshed_at": last_refreshed_at
        }
        return data

    def update(self, country, **kwargs):
        """Updates attributes of a country"""
        try:
            for key, value in kwargs.items():
                setattr(country, key, value)
            self.__session.add(country)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e






