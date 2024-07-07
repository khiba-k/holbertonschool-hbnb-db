# from flask import Flask
from Persistance import data_management as DM
from Model import place
from flask import jsonify
from RU_db import get_data_from_db

manipulate_data = DM.DataManager()
entity_type = "places"


def create_place(req_data):
    """
    Add place to data structure and save it using DataManager.
    """
    try:
        request_data = req_data
        required_fields = [
            "host_id", "place_name", "description", "address",
            "country_name", "city_name", "latitude", "longitude",
            "number_of_rooms", "bathrooms", "price_per_night", 
            "max_guests", "amenities"
        ]

        # for field in required_fields:
        #     if field not in request_data:
        #         return jsonify({"error": f"Missing field: {field}"}), 400

        place_name = request_data.get("place_name").replace(" ", "_")

        place_obj = place.Place(
            request_data.get("host_id"),
            place_name, request_data.get("description"),
            request_data.get("address"),
            request_data.get("country_name"), request_data.get("city_name"),
            request_data.get("latitude"), request_data.get("longitude"),
            request_data.get("number_of_rooms"), request_data.get("bathrooms"),
            request_data.get("price_per_night"), request_data.get("max_guests"),
            request_data.get("amenities")
        )

        data = place_obj.to_dict()
        manipulate_data.save(entity_type, data, place_obj.host_id, place_obj.place_name)
        manipulate_data.save(entity_type, data)
        place_obj.save_to_db()
        
        return jsonify({"message": "Place created successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_places():
    """Get all places function"""
    try:
        places = manipulate_data.get(entity_type)
        places_from_db = get_data_from_db("places")
        if not places or not places_from_db:
            return jsonify([]), 200
        return jsonify(places_from_db.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_place(id):
    """Get one place and return it"""
    try:
        place = manipulate_data.get(entity_type, id)
        place_from_db = get_data_from_db("places", id)
        if not place or not place_from_db:
            return jsonify({"error": "Place not found"}), 404

        amenities = manipulate_data.get("amenities")
        if place.get("amenities"):
            linked_amenities = [amenity for amenity in amenities if amenity.get("id") in place.get("amenities")]
            place["linked_amenities"] = linked_amenities
        
        return jsonify(place_from_db.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def update_place(data, id):
    """Update a specific place"""
    try:
        request_data = data
        manipulate_data.update(entity_type, request_data, request_data.get("host_id"), id)
        manipulate_data.update(entity_type, request_data, None, id)
        place_from_db = get_data_from_db("places", id)
        for key, value in data.keys():
            for key_class, value_class in place_from_db.__dict__:
                if key_class == key:
                    place_from_db.key_class = value
        place_from_db.save_to_db()
        
        return jsonify({"message": "Place updated successfully.", "updated": request_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def delete_place(id):
    """Delete a place"""
    try:
        response = manipulate_data.delete(entity_type, id)
        get_data_from_db("places", id).delete_from_db()
        if response is None:
            return jsonify({"error": "Place not found"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
