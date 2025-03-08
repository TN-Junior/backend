import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carregar as variáveis do arquivo .env
load_dotenv()

class Config:
    # Garantir que a senha seja uma string e codificar corretamente
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'test')

    # Codificar a senha para evitar erros na URL
    db_password_encoded = quote_plus(db_password)

    SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_password_encoded}@{db_host}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
