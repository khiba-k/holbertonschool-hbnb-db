from create_app_db import db
# from base_model import BaseModel
from datetime import datetime

class Amenity(db.Model):
    name = db.Column(db.String(50))
    created_at = db.Column(db.Date, datetime.now)
    updated_at = None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }                                                