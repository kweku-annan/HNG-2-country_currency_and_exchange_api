#!/usr/bin/env python
"""Configuration settings for the application"""
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # API URLs
    COUNTRIES_API_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
    EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/USD"
