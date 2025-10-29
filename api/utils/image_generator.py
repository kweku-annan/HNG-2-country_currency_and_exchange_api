#!/usr/bin/env python
"""Generates Image"""
from colorsys import yiq_to_rgb

from PIL import Image, ImageDraw, ImageFont
import os


def generate_image(data):
    """Generates a summary image with country statistics"""
    # Create image (width, height, background color)
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)

    # Load a font
    font_title = ImageFont.load_default()
    font_text = ImageFont.load_default()

    # Title
    draw.text((20, 20), "Country Statistics Summary", font=font_title, fill='black')

    # Draw total countries
    draw.text((20, 80), f"Total Countries: {data['total_countries']}", fill='black', font=font_text)

    # Draw top 5 countries by GDP
    y_position = 140
    for i, country in enumerate(data['top_countries_by_gdp'], 1):
        gdp_formatted = f"${country['estimated_gdp']:,.0f}" if country['estimated_gdp'] else "N/A"
        text = f"{i}. {country['name']} - {gdp_formatted}"
        draw.text((40, y_position), text, fill='black', font=font_text)
        y_position += 30

    # Draw last refreshed time
    timestamp = data['last_refreshed_at'].strftime('%Y-%m-%d %H:%M:%S') if data['last_refreshed_at'] else "N/A"
    draw.text((20, 320), f"Last Refreshed At: {timestamp}", fill='black', font=font_text)

    # Create cache directory if it doesn't exist
    os.makedirs('cache', exist_ok=True)

    img.save('cache/summary.png')
