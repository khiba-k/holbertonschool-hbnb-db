class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class SQLiteConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_db.db'


# Setup postgres database in pgadmin 4 or postgresql cli if postgres is preefered
class PostgreSQLConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5000/hbnb_db'
