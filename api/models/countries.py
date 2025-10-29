#!/usr/bin/env python
"""Countries table"""
from decimal import Decimal

from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Country(Base):
    """Defines the country table"""
    from datetime import datetime
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(60), nullable=False, unique=True)
    capital = Column(String(60), nullable=True)
    region = Column(String(60), nullable=True)
    population = Column(Integer, nullable=False)
    currency_code = Column(String(10), nullable=True)
    exchange_rate = Column(Numeric(18, 2), nullable=True)
    estimated_gdp = Column(Numeric(20, 1), nullable=True)
    flag_url = Column(String(100), nullable=True)
    last_refreshed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


    def __init__(
            self, name: str, population: int, currency_code : str = None, exchange_rate: float = None,
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

    def to_dict(self):
        """Return a dictionary representation of the Country instance"""
        return {
            "id": self.id,
            "name": self.name,
            "capital": self.capital,
            "region": self.region,
            "population": self.population,
            "currency_code": self.currency_code,
            "exchange_rate": float(self.exchange_rate) if self.exchange_rate else None,
            "estimated_gdp": float(self.estimated_gdp) if self.estimated_gdp else None,
            "flag_url": self.flag_url,
            "last_refreshed_at": self.last_refreshed_at.replace(microsecond=0).isoformat() + 'Z' if self.last_refreshed_at else None
        }