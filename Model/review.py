#!/usr/bin/python3
from place import Place
from user import User
from create_app_db import db
from base_model import BaseModel
from datetime import datetime

class Review(db.Model):
    user_id = ""
    place_id = ""
    # self.name = name
    comment = db.Column(db.String(50))
    ratings = db.Column(db.Integer)
    review_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.Date, datetime.now)

    def save(self):
        """Save the review only if the user is not the host of the place."""
        if self.user_id == self.place_id.host_id:
            raise ValueError("Host cannot review their own place.")

    def to_dict(self):
        """Return a dictionary representation of the Review instance."""
        dict = {
            'user_id': self.user_id,
            'place_id': self.place_id,
            'comment': self.comment,
            'ratings': self.ratings,
            'created_at': self.created_at,
            # 'updated_at': self.updated_at,
            'id': self.review_id
        }
        return dict