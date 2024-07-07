from Model import cities
import sys
import os

# Get the directory containing this script
current_dir = os.path.dirname(__file__)

# Construct the path to the Model directory
model_path = os.path.join(current_dir, '..', 'Model')

# Add Model directory to sys.path
sys.path.append(model_path)

from Persistance.data_management import DataManager
from flask import Flask, jsonify, request
from RU_db import get_data_from_db


def create_city():
    """Create new city"""
    data = request.json
    name = data.get('name')
    country_code = data.get('country_code')
    
    new_city = cities.Cities(name, country_code)
    result = new_city.save_to_file()
    new_city.save_to_db()

    if result == "City already exists":
        return jsonify({"error": "City already exists"}), 400
    return jsonify(new_city.to_dict()), 201

def get_all_cities():
    """Retrieve all existing cities"""
    data_manager = DataManager()
    cities_data = data_manager.get("cities")
    cities = get_data_from_db("cities")

    if cities_data or cities:
        return jsonify(cities.to_dict()), 200
    else:
        return jsonify({"message": "No cities found"}), 404

def get_specific_city(city_id):
    """Get specific city and return it"""
    data_manager = DataManager()
    city_data = data_manager.get("cities", city_id)
    city = get_data_from_db("cities", city_id)

    if city_data or cities:
        return jsonify(city.to_dict()), 200
    else:
        return jsonify({"message": "City not found"}), 404

def update_city(city_id):
    """Update an existing city"""
    data = request.json
    data_manager = DataManager()
    
    existing_city = data_manager.get("cities", city_id)
    city = get_data_from_db("cities", city_id)
    if not existing_city or not city:
        return jsonify({"message": "City not found"}), 404

    updated_city = cities.Cities(
        name=data.get('name', existing_city['name']),
        country_code=data.get('country_code', existing_city['country_code'])
    )
    updated_city.city_id = city_id
    updated_city.update_city()
    city.city_name = data.get('name', existing_city['name'])
    city.country = data.get('country_code', existing_city['country_code'])
    city.save_to_db()
    
    return jsonify(city.to_dict()), 200

def delete_city(city_id):
    """Delete city data"""
    data_manager = DataManager()
    city = get_data_from_db("cities", city_id)
    result = data_manager.delete("cities", city_id)
    city.delete_from_db()
    
    if result == "something went wrong":
        return jsonify({"message": "City not found"}), 404
    return jsonify({"message": "City deleted successfully"}), 200