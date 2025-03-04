class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
