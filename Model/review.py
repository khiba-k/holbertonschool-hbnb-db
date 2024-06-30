#!/usr/bin/python3
from datetime import datetime, timezone
from create_app_db import db
from place import Place
from user import User

class Review(db.Model):
    """
    Defines a review.
    """
    __tablename__ = 'review'

    review_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'), nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    ratings = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    # def save(self):
    #     """Save the review only if the user is not the host of the place."""
    #     place = Place.query.get(self.place_id)
    #     if self.user_id == place.host_id:
    #         raise ValueError("Host cannot review their own place.")
    #     db.session.add(self)
    #     db.session.commit()

    def save_to_db(self):
        """Saves the user information to the database."""
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """Return a dictionary representation of the Review instance."""
        return {
            'review_id': self.review_id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'comment': self.comment,
            'ratings': self.ratings,
            'created_at': str(self.created_at)
        }

    def __repr__(self) -> str:
        return f"<Review: {self.review_id}>"
