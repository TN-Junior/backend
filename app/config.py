import os
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

class Config:
    # Utilizar a URL do banco diretamente do .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
