# app.py

from flask import Flask
from flask_cors import CORS
from models.participant import db
from routes.participant import participant_bp
from config import Config

app = Flask(__name__)

# Configurações do Flask
app.config.from_object(Config)

# Configuração do CORS
CORS(app, resources={r"/*": {"origins": app.config['CORS_ALLOWED_ORIGINS']}})

# Inicializa o banco de dados
db.init_app(app)

# Registra as rotas
app.register_blueprint(participant_bp)

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
