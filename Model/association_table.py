from sqlalchemy import Table, Column, Integer, ForeignKey
from create_app_db import db

place_amenity = Table('place_amenity', db.Model.metadata,
    Column('place_id', Integer, ForeignKey('place.place_id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenity.id'), primary_key=True)
)
