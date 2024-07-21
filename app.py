import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, get_current_user, jwt_required, get_jwt
from API.user_views import create_user, get_all_users, get_specific_user, update_user, delete_user, user_login
from API.amenities_views import create_amenity, get_amenities, get_amenity, update_amenity, delete_amenity
from API.country_api import get_all_countries, get_country, get_country_cities
from API.city_api import create_city, get_all_cities, get_specific_city, update_city, delete_city
from API.places_views import create_place, get_places, get_place, update_place, delete_place
from API.reviews_views import create_review_for_place, get_reviews_by_user, get_reviews_for_place, get_review, update_review, delete_review
from config import SQLiteConfig, PostgreSQLConfig
from create_app_db import db, init_db
import secrets
from RU_db import get_data_from_db
from Permissions import user_permission, place_permission, review_permission

config_name = os.getenv('FLASK_CONFIGURATION', 'SQLiteConfig')

config_map = {
    'SQLiteConfig': SQLiteConfig,
    'PostgreSQLConfig': PostgreSQLConfig
}

"""Export environment variables to set the configuration in terminal"""
# export FLASK_CONFIGURATION=SQLiteConfig
# export FLASK_CONFIGURATION=PostgreSQLConfig

app = Flask(__name__)
app.config.from_object(config_map[config_name])
app.config["JWT_SECRET_KEY"] = "abc123$"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
jwt = JWTManager(app)

init_db(app)

if config_name == 'SQLiteConfig' and not os.path.exists("hbnb_db.sqlite3"):
    with app.app_context():
        db.create_all()

# App index
@app.route('/')
def home():
    return "Welcome to HBNB Lesotho!"

"""
User routes
"""

# Users Routes
@app.route ('/login', methods=['POST'])
def login():
    return user_login(request.get_json())

@app.route('/users', methods=['POST'])
def user():
    return create_user(request.get_json())

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    result = user_permission(get_all_users)
    return result
    
@app.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def specfic_user(user_id):
    result = user_permission(get_specific_user, user_id)
    return result 
    
@app.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def up_user(user_id):
    data = request.get_json()
    result = user_permission(update_user, user_id, data)
    return result

@app.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def del_user(user_id):
    result = user_permission(delete_user, user_id)
    return result

"""
Amenity routes
"""

@app.route('/amenities', methods=['POST'])
@jwt_required()
def create_amenity_route():
    return create_amenity()

@app.route('/amenities', methods=['GET'])
@jwt_required()
def get_amenities_route():
    return get_amenities()

@app.route('/amenities/<amenity_id>', methods=['GET'])
@jwt_required()
def get_amenity_route(amenity_id):
    return get_amenity(amenity_id)

@app.route('/amenities/<amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity_route(amenity_id):
    return update_amenity(amenity_id)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity_route(amenity_id):
    return delete_amenity(amenity_id)

"""
countries routes
"""

# Countries routes and paths
@app.route('/countries', methods=['GET'])
@jwt_required()
def countries_route():
    return get_all_countries()

@app.route('/countries/<country_code>', methods=['GET'])
@jwt_required()
def get_country_route(country_code):
    return get_country()

@app.route('/countries/<country_code>/cities', methods=['GET'])
@jwt_required()
def get_country_cities_route(country_code):
    return get_country_cities(country_code)

# City routes and paths

@app.route('/cities', methods=['POST'])
@jwt_required()
def create_city_route(user_id):
    return create_city()

@app.route('/cities', methods=['GET'])
@jwt_required()
def get_cities_route():
    return get_all_cities()

@app.route('/cities/<city_id>', methods=['GET'])
@jwt_required()
def retrieve_city_route(city_id):
    return get_specific_city(city_id)

@app.route('/cities/<city_id>', methods=['PUT'])
@jwt_required()
def update_city_route(city_id):
    return update_city()

@app.route('/cities/<city_id>', methods=['DELETE'])
@jwt_required()
def del_city_route(city_id):
    return delete_city(city_id)

"""
places routes
"""

@app.route('/places', methods=['POST'])
@jwt_required()
def create_place_route():
    data = request.get_json()
    result = place_permission(create_place, None, data)
    return result

@app.route('/places', methods=['GET'])
@jwt_required()
def get_places_route():
    result = place_permission(get_places)
    return result

@app.route('/places/<string:place_id>', methods=['GET'])
@jwt_required()
def get_place_route(place_id):
    result = place_permission(get_place, place_id)
    return result

@app.route('/places/<string:place_id>', methods=['PUT'])
@jwt_required()
def update_place_route(place_id):
    data = request.get_json()
    result = place_permission(update_place, place_id, data)
    return result

@app.route('/places/<string:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place_route(place_id):
    result = place_permission(delete_place, place_id)
    return result


"""
review routes
"""

@app.route('/places/<place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review_for_place_route(place_id):
    data = request.get_json()
    result = review_permission(create_review_for_place, place_id, data)
    return result

@app.route('/users/<user_id>/reviews', methods=['GET'])
@jwt_required()
def get_reviews_by_user_route(user_id):
    data = request.get_json()
    result = review_permission(get_reviews_by_user, None, data, user_id)
    return result

@app.route('/places/<place_id>/reviews', methods=['GET'])
@jwt_required()
def get_reviews_for_place_route(place_id):
    result = review_permission(get_reviews_for_place, place_id)
    return result

@app.route('/reviews/<review_id>', methods=['GET'])
@jwt_required()
def get_review_route(review_id):
    result = review_permission(get_review, None, None, None, review_id)
    return result 

@app.route('/reviews/<review_id>', methods=['PUT'])
@jwt_required()
def update_review_route(review_id):
    data = request.get_json()
    result = review_permission(update_review, None, data, None, review_id)
    return result

@app.route('/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review_route(review_id):
    result = review_permission(delete_review, None, None, None, review_id)
    return result



if __name__ == "__main__":
    import sys
    import os

    # Get the directory two levels up (the root of your project)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(root_dir)

    persistence_path = os.path.join(root_dir, 'Persistence')
    sys.path.append(persistence_path)

    app.run(host="127.0.0.1", port="5000", debug=True, threaded=True)