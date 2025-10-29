#!/usr/bin/env python
"""Defines routes for country and currency data"""
import os.path
import random

from flask import Blueprint, jsonify, request, send_file

from api.models.countries import Country
from api.utils.fetch_data_helper import fetch_countries_data, fetch_exchange_rates
from api.schemas.dbStorage import DBStorage
from api.utils.image_generator import generate_image

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

        if name:
            if storage.exists(name):
                country = storage.get_by_name(name)
                storage.update(country, **new_data)
            else:
                country = Country(**new_data)
                storage.save(country)

            try:
                image_info = storage.image_data()
                generate_image(image_info)
            except Exception as e:
                return jsonify({"error": "Internal server error"}), 500
        else:
            continue
    return jsonify({"message": "Countries refreshed successfully!"}), 200

@country_bp.route('/countries', methods=['GET'])
def get_countries():
    """Retrieves countries with optional filtering and sorting"""
    try:
        params = request.args
        filters = storage.get_all(params)
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

    return jsonify([k.to_dict() for k in filters]), 200

@country_bp.route('/countries/<string:name>', methods=['GET'])
def get_country(name):
    """Retrieves a single country by name"""
    country = storage.get_by_name(name)
    if not country:
        return jsonify({"error": "Country not found"}), 404

    return jsonify(country.to_dict()), 200

@country_bp.route('/countries/<string:name>', methods=['DELETE'])
def delete_country(name):
    """Deletes a country by name"""
    if not storage.exists(name):
        return jsonify({"error": "Country not found"}), 404

    success = storage.delete(name)
    if not success:
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({"message": f"Country '{name}' deleted successfully"}), 200

@country_bp.route('/countries/status', methods=['GET'])
def get_countries_status():
    """Retrieves status of countries data"""
    status = storage.status()
    if not status:
        return jsonify({"error": "Internal server error"}), 500
    return jsonify(status), 200

@country_bp.route('/countries/images', methods=['GET'])
def get_country_images():
    """Serve the generated image of countries data"""
    image_path = 'cache/summary.png'

    if not os.path.exists(image_path):
        return jsonify({"error": "Summary image not found"}), 404

    return send_file(image_path, mimetype='image/png'), 200



