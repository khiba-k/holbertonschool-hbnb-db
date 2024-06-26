from country import Country
from base_model import BaseModel
from Model.country import Country

class Place(BaseModel):
    """
    Defines a place.
    """

    def __init__(self, host_id: str, place_name: str = None, description: str = None, 
                 address: str = None, country_name: str = None, city_name: str = None, 
                 latitude: float = None, longitude: float = None, number_of_rooms: int = None, 
                 bathrooms: int = None, price_per_night: float = None, max_guests: int = None, amenities: list = None):
        super().__init__()
        
        self.place_id = self.id
        self.place_name = place_name
        self.description = description
        self.address = address
        self.host_id = host_id
        self.country = Country(country_name)
        self.city = city_name
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities

    def to_dict(self):
        """Return a dictionary representation of the Place instance."""
        base_dict = super().to_dict()
        base_dict.update({
            'place_name': self.place_name,
            'description': self.description,
            'address': self.address,
            'host_id': self.host_id,
            'id': self.place_id,
            'country': self.country.country_name,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'number_of_rooms': self.number_of_rooms,
            'bathrooms': self.bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenities': self.amenities,
            'created_at': str(self.created_at)
        })
        return base_dict