# from flask import Flask
from Persistance import data_management as DM
from Model import place
from flask import jsonify

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
        
        return jsonify({"message": "Place created successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_places():
    """Get all places function"""
    try:
        places = manipulate_data.get(entity_type)
        if not places:
            return jsonify([]), 200
        return jsonify(list(places.keys())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_place(id):
    """Get one place and return it"""
    try:
        place = manipulate_data.get(entity_type, id)
        if not place:
            return jsonify({"error": "Place not found"}), 404

        amenities = manipulate_data.get("amenities")
        if place.get("amenities"):
            linked_amenities = [amenity for amenity in amenities if amenity.get("id") in place.get("amenities")]
            place["linked_amenities"] = linked_amenities
        
        return jsonify(place), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def update_place(data, entity_id):
    """Update a specific place"""
    try:
        request_data = data
        manipulate_data.update(entity_type, request_data, request_data.get("host_id"), entity_id)
        manipulate_data.update(entity_type, request_data, None, entity_id)
        
        return jsonify({"message": "Place updated successfully.", "updated": request_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def delete_place(id):
    """Delete a place"""
    try:
        response = manipulate_data.delete(entity_type, id)
        if response is None:
            return jsonify({"error": "Place not found"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
