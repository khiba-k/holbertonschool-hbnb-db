from flask_restx import Namespace, Resource, fields
import sys
import os

# Get the directory containing this script
current_dir = os.path.dirname(__file__)

# Construct the path to the Model directory
model_path = os.path.join(current_dir, '..', 'Model')

# Add Model directory to sys.path
sys.path.append(model_path)


from flask import Flask, jsonify, request
import requests
from geopy.geocoders import Nominatim

class Country:
    def __init__(self, name, alpha2Code):
        self.name = name
        self.alpha2Code = alpha2Code

    @staticmethod
    def get_all_countries():
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()
        return [{'name': country['name']['common'], 'alpha2Code': country['cca2']} for country in countries]
    
    @staticmethod
    def get_country():
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()
        return [{'name': country['name']['common'], 'alpha2Code': country['cca2']} for country in countries]

    @staticmethod
    def get_all_cities(alpha2Code):
        geolocator = Nominatim(user_agent="city_explorer")
        country = Country.get_country(alpha2Code)
        country_name = country['name']
        cities = []
        try:
            location = geolocator.geocode(country_name, exactly_one=False, limit=None)
            if location:
                for loc in location:
                    cities.append(loc.address)
        except Exception as e:
            print(f"Error fetching cities for {country_name}: {e}")
        return cities

def get_all_countries():
    """Retrieve all countries with their alpha-2 codes"""
    countries = Country.get_all_countries()

    if countries:
        return jsonify(countries), 200
    else:
        return jsonify({"message": "No countries found"}), 404

def get_country():
    """Retrieve all countries with their alpha-2 codes"""
    country = Country.get_country()

    if country:
        return jsonify(country), 200
    else:
        return jsonify({"message": "No countries found"}), 404

def get_country_cities(alpha2Code):
        """Retrieve all cities of a specific country"""
        cities = Country.get_all_cities(alpha2Code)
        if cities:
            return jsonify(cities), 200
        else:
            return jsonify({"message": "No cities found for this country"}), 404
