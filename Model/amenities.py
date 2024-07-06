from datetime import datetime, timezone
from create_app_db import db
# from association_table import place_amenity

class Amenity(db.Model):
    """
    Defines an amenity.
    """
    __tablename__ = 'amenity'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True)

    def save_to_db(self):
        """Saves the user information to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes the user information from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at) if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<Amenity: {self.name}>"
                                      