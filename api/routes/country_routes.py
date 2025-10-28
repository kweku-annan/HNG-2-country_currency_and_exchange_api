#!/usr/bin/env python
"""Defines routes for country and currency data"""
import random
from flask import Blueprint, jsonify
from api.models.countries import Country
from api.utils.fetch_data_helper import fetch_countries_data, fetch_exchange_rates
from api.schemas.dbStorage import DBStorage


# Initialize blueprint and storage
country_bp = Blueprint('countries', __name__)
storage = DBStorage()

@country_bp.route('/countries/refresh', methods=['POST'])
def refresh_countries_data():
    """Fetches and refreshes country data from external API"""
    countries_data = fetch_countries_data()
    if not countries_data:
        return jsonify(
            {
                "error": "External data source unavailable",
                "details": "Could not fetch data from Countries API"
            }
        ), 503

    exchange_rates_data = fetch_exchange_rates()
    if not exchange_rates_data:
        return jsonify(
            {
                "error": "External data source unavailable",
                "details": "Could not fetch data from Exchange Rates API"
            }
        ), 503

    # Parse and store countries data
    for country_info in countries_data:
        name = country_info.get('name', None)
        capital = country_info.get('capital', None)
        region = country_info.get('region', None)
        population = country_info.get('population', None)
        currencies = country_info.get('currencies', [])
        currency_code = currencies[0]['code'] if currencies else None
        flag_url = country_info.get('flag', None)
        if currency_code:
            exchange_rate = exchange_rates_data.get('rates', {}).get(currency_code, None)
            if exchange_rate:
                random_value = random.uniform(1000, 2000)
                estimated_gdp = (population * random_value) / exchange_rate
            else:
                exchange_rate = None
                estimated_gdp = None
        else:
            exchange_rate = None
            estimated_gdp = None

        new_data = {
            "name": name,
            "capital": capital,
            "region": region,
            "population": population,
            "currency_code": currency_code,
            "exchange_rate": exchange_rate,
            "estimated_gdp": estimated_gdp,
            "flag_url": flag_url
        }

        if storage.exists(name):
            country = storage.get_by_name(name)
            storage.update(country, **new_data)
        else:
            country = Country(**new_data)
            storage.save(country)

    return jsonify({"message": "Countries refreshed successfully!"}), 200

# @country_bp.route('/countries', methods=['GET'])





