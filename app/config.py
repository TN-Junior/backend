import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carregar as variáveis do .env
load_dotenv()

# Debugging - Verificar se a variável de ambiente está carregada corretamente
print("DEBUG - DB_PASSWORD:", os.getenv('DB_PASSWORD'))

class Config:
    db_password = os.getenv('DB_PASSWORD')

    if db_password is None:
        raise ValueError("Erro: A variável de ambiente DB_PASSWORD não está definida.")

    # Usar quote_plus para garantir que caracteres especiais sejam tratados corretamente
    db_password = quote_plus(db_password)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.getenv('DB_USER')}:{db_password}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
