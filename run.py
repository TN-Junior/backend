from app import create_app, db  
from app.models import Participant

# Crie a aplicação Flask
app = create_app()

# Inicializa o banco de dados
with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
