from create_app_db import db
from Model import user, place, amenities, cities, review  # Import your models
from API import country_api

def get_data_from_db(table, id=None):
    table_obj = db.metadata.tables.get(table)
    if table_obj is None:
        raise ValueError(f"Table {table} not found in metadata")
    
    if id:
        if table == "user":
            return db.session.query(user.User).filter(user.User.user_id == id).first()
        if table == "place":
            return db.session.query(place.Place).filter(place.Place.place_id == id).first()
        if table == "amenity":
            return db.session.query(amenities.Amenity).filter(amenities.Amenity.id == id).first()
        if table == "city":
            return db.session.query(cities.Cities).filter(cities.Cities.id == id).first()
        if table == "country":
            return db.session.query(country_api.Country).filter(country_api.Country.alpha2Code == id).first()
        if table == "review":
            return db.session.query(review.Review).filter(review.Review.review_id == id).first()
    return db.session.query(table_obj).all()
