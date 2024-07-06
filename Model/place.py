"""
module for defining a place
"""

from datetime import datetime, timezone
from create_app_db import db
from sqlalchemy.dialects.postgresql import JSON

class Place(db.Model):
    """
    Defines a place.
    """
    __tablename__ = 'place'
    __table_args__ = {'extend_existing': True}

    place_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    place_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    # Relationships
    amenities = db.Column(JSON, db.ForeignKey('amenity.id'))

    def save_to_db(self):
        """Saves the user information to the database."""
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        """Deletes the user information from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Return a dictionary representation of the Place instance."""
        return {
            'place_name': self.place_name,
            'description': self.description,
            'address': self.address,
            'host_id': self.host_id,
            'id': self.place_id,
            'country': self.country,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'number_of_rooms': self.number_of_rooms,
            'bathrooms': self.bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'created_at': str(self.created_at)
        }

    def __repr__(self) -> str:
        return f"<Place: {self.place_name}>"
