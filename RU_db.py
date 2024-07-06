from create_app_db import db

def get_data_from_db(table, id=None):
    if id:
        return db.session.query(table).filter(table.id == id).first()
    else:
        return db.session.query(table).all()