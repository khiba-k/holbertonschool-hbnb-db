# from base_model import BaseModel
# from datetime import datetime
from create_app_db import db
import sys
import os

# Get the directory containing this script
current_dir = os.path.dirname(__file__)

# Construct the path to the Model directory
model_path = os.path.join(current_dir, '..', 'Model')

# Add Model directory to sys.path
sys.path.append(model_path)

class Cities(db.Model):
    """
    Defines city
    """

    city_name = db.Column(db.String(50))
    country = db.Column(db.String(50), db.ForeignKey("Countries.alpha2Code"))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, city_name, country):
        self.city_name = city_name
        self.country = country

    def save_to_db(self):
        """Saves the user information to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes the user information from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        # base_dict = super().to_dict()
        base_dict = ({
            "city_name": self.city_name,
            "country": self.country,
            "city_id": self.id
        })
        return base_dict
