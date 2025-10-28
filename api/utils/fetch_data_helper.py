#!/usr/bin/env python
"""Helper functions to fetch data from external APIs"""
import requests
from config import Config


def fetch_countries_data() :
    """Fetches countries data from the external API"""
    try:
        response = requests.get(Config.COUNTRIES_API_URL, timeout=10)
        response.raise_for_status()
        countries_data = response.json()
        return countries_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching countries data: {e}")
        return None


def fetch_exchange_rates():
    """Fetches exchange rates data from the external API"""
    try:
        response = requests.get(Config.EXCHANGE_RATE_API_URL, timeout=10)
        response.raise_for_status()
        exchange_data = response.json()
        return exchange_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates data: {e}")
        return None

print(type(fetch_countries_data()))
exchange_rate = fetch_exchange_rates()
print(exchange_rate.get('rates').get('GHS'))



