#!/usr/bin/env python
"""Countries table"""
from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Country(Base):
    """Defines the country table"""
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    capital = Column(String, nullable=True)
    region = Column(String, nullable=True)
    population = Column(Integer, nullable=False)
    currency_code = Column(String, nullable=False)
    exchange_rate = Column(Numeric(18, 2), nullable=False)
    estimated_gdp = Column(Numeric(20, 1), nullable=True)
    flag_url = Column(String, nullable=True)
    last_refreshed = Column(String(60), nullable=False)


    def __init__(self, name: str, population: int, currency_code : str, exchange_rate: float, last_refreshed: str,
                 capital: str = None, region: str = None, estimated_gdp: float = None, flag_url: str = None
                 ):
        """Initializes the Country instance"""
        self.name = name
        self.capital = capital
        self.region = region
        self.population = population
        self.currency_code = currency_code
        self.exchange_rate = exchange_rate
        self.estimated_gdp = estimated_gdp
        self.flag_url = flag_url
        self.last_refreshed = last_refreshed
