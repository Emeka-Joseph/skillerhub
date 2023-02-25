class Config:
    SECRET_KEY='Kimberly2018/?iiu8'
#database connection params

class TestConfig(Config):
    SERVER_ADDRESS='http://127.0.0.1:9090'

SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root@localhost/skillerdb'
SECRET_KEY='Kimberly2018/?iiu8'