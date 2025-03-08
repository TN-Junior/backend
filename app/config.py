import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carregar as variáveis do arquivo .env
load_dotenv()

class Config:
    # Garantir que os valores sejam strings e codificar corretamente
    db_user = quote_plus(os.getenv('DB_USER', 'root'))
    db_password = quote_plus(os.getenv('DB_PASSWORD', ''))
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = quote_plus(os.getenv('DB_NAME', 'test'))

    # String de conexão corrigida para evitar problemas com caracteres especiais
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
