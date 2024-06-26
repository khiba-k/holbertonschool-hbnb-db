from flask import Flask, request, jsonify
from API.user_views import create_user, get_all_users, get_specific_user, update_user, delete_user
from API.amenities_views import create_amenity, get_amenities, get_amenity, update_amenity, delete_amenity
from API.country_api import get_all_countries, get_country, get_country_cities
from API.city_api import create_city, get_all_cities, get_specific_city, update_city, delete_city
from API.places_views import create_place, get_places, get_place, update_place, delete_place
from API.reviews_views import create_review_for_place, get_reviews_by_user, get_reviews_for_place, get_review, update_review, delete_review

app = Flask(__name__)

# App index
@app.route('/')
def home():
    return "Welcome to HBNB Lesotho!"

"""
User routes
"""

# Users Routes
@app.route('/users', methods=['POST'])
def user():
    return create_user(request.get_json())

@app.route('/users', methods=['GET'])
def get_users():
    return get_all_users()

@app.route('/users/<user_id>', methods=['GET'])
def speicfic_user(user_id):
    return get_specific_user(user_id)

@app.route('/users/<user_id>', methods=['PUT'])
def up_user(user_id):
    return update_user(user_id, request.get_json())

@app.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    return delete_user(user_id)

"""
Amenity routes
"""

@app.route('/amenities', methods=['POST'])
def create_amenity_route():
    return create_amenity()

@app.route('/amenities', methods=['GET'])
def get_amenities_route():
    return get_amenities()

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_route(amenity_id):
    return get_amenity(amenity_id)

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity_route(amenity_id):
    return update_amenity(amenity_id)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_route(amenity_id):
    return delete_amenity(amenity_id)

"""
countries routes
"""

# Countries routes and paths
@app.route('/countries', methods=['GET'])
def countries_route():
    return get_all_countries()

@app.route('/countries/<country_code>', methods=['GET'])
def get_country_route(country_code):
    return get_country()

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_country_cities_route(country_code):
    return get_country_cities(country_code)

# City routes and paths

@app.route('/cities', methods=['POST'])
def create_city_route(user_id):
    return create_city()

@app.route('/cities', methods=['GET'])
def get_cities_route():
    return get_all_cities()

@app.route('/cities/<city_id>', methods=['GET'])
def retrieve_city_route(city_id):
    return get_specific_city(city_id)

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city_route(city_id):
    return update_city()

@app.route('/cities/<city_id>', methods=['DELETE'])
def del_city_route(city_id):
    return delete_city(city_id)

"""
places routes
"""

@app.route('/places', methods=['POST'])
def create_place_route():
    return create_place(request.get_json())

@app.route('/places', methods=['GET'])
def get_places_route():
    return get_places()

@app.route('/places/<string:place_id>', methods=['GET'])
def get_place_route(place_id):
    return get_place(place_id)

@app.route('/places/<string:place_id>', methods=['PUT'])
def update_place_route(place_id):
    return update_place(request.get_json(), place_id)

@app.route('/places/<string:place_id>', methods=['DELETE'])
def delete_place_route(place_id):
    return delete_place(place_id)


"""
review routes
"""

@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review_for_place_route(place_id):
    return create_review_for_place(request.get_json(), place_id)

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews_by_user_route(user_id):
    return get_reviews_by_user(request.get_json(), user_id)

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_for_place_route(place_id):
    return get_reviews_for_place(place_id)

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review_route(review_id):
    return get_review(review_id)

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review_route(review_id):
    return update_review(request.get_json(), review_id)

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_route(review_id):
    return delete_review(review_id)


if __name__ == "__main__":
    import sys
    import os

    # Get the directory two levels up (the root of your project)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(root_dir)

    persistence_path = os.path.join(root_dir, 'Persistence')
    sys.path.append(persistence_path)

    app.run(host="127.0.0.1", port="50000")