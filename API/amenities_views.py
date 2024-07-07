from flask import jsonify, request
from Persistance import data_management as DM
from Model.amenities import Amenity as am
from RU_db import get_data_from_db

dm = DM.DataManager()
entity_type = "amenities"

def create_amenity(name):
    """Create an amenity"""
    try:
        
        if not name:
            return jsonify({"error": "Name is required"}), 400

        amenity_data = am(name).to_dict()
        dm.save(entity_type, amenity_data)
        am.save_to_db()
        return jsonify({"message": "Amenity saved successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_amenities():
    """Get a list of amenities"""
    try:
        amenities = dm.get(entity_type)
        amenities_from_db = get_data_from_db("amenity")
        if not amenities or not amenities_from_db:
            return jsonify([]), 200
        return jsonify(amenities_from_db.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_amenity(id):
    """Get a specific amenity"""
    try:
        amenity = dm.get(entity_type, id)
        amenity_from_db = get_data_from_db("amenity", id)
        if not amenity or amenity_from_db:
            return jsonify({"error": "Amenity not found"}), 404
        return jsonify(amenity_from_db.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_amenity(id):
    """Update an existing amenity"""
    try:
        request_data = request.json
        if not request_data:
            return jsonify({"error": "No data provided"}), 400

        dm.update(entity_type, request_data, None, id)
        amenity_from_db = get_data_from_db("amenity", id)
        amenity_from_db.name = request_data.get("name")
        return jsonify({"message": "Amenity updated successfully", "updated": request_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_amenity(id):
    """Delete an amenity"""
    try:
        response = dm.delete(entity_type, id)
        amenity_from_db = get_data_from_db("amenity", id)
        amenity_from_db.delete_from_db()
        if response is None:
            return jsonify({"error": "Amenity not found"}), 404
        return jsonify({"message": "Amenity deleted successfully", "deleted": id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
