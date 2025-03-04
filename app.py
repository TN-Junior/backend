from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    participation = db.Column(db.Integer, nullable=False)

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

@app.route("/participants", methods=["GET"])
def get_participants():
    participants = Participant.query.all()
    return jsonify([{
        "id": p.id,
        "firstName": p.first_name,
        "lastName": p.last_name,
        "participation": p.participation
    } for p in participants])

@app.route("/participants", methods=["POST"])
def add_participant():
    try:
        data = request.json
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        participation = data.get("participation")

        if not first_name or not last_name:
            return jsonify({"error": "First name and last name are required"}), 400
        if not isinstance(participation, int) or participation < 1 or participation > 100:
            return jsonify({"error": "Participation must be a number between 1 and 100"}), 400

        new_participant = Participant(
            first_name=first_name,
            last_name=last_name,
            participation=participation
        )
        db.session.add(new_participant)
        db.session.commit()

        return jsonify({"message": "Participant added successfully", "participant": {
            "id": new_participant.id,
            "firstName": new_participant.first_name,
            "lastName": new_participant.last_name,
            "participation": new_participant.participation
        }}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/participants/<int:id>", methods=["PUT"])
def update_participant(id):
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({"error": "Participant not found"}), 404

    data = request.json
    participant.first_name = data.get("firstName", participant.first_name)
    participant.last_name = data.get("lastName", participant.last_name)
    participant.participation = data.get("participation", participant.participation)
    
    db.session.commit()
    return jsonify({"message": "Participant updated successfully", "participant": {
        "id": participant.id,
        "firstName": participant.first_name,
        "lastName": participant.last_name,
        "participation": participant.participation
    }}), 200

@app.route("/participants/<int:id>", methods=["DELETE"])
def delete_participant(id):
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({"error": "Participant not found"}), 404

    db.session.delete(participant)
    db.session.commit()
    return jsonify({"message": f"Participant with ID {id} deleted successfully"}), 200

@app.route("/participants", methods=["DELETE"])
def reset_participants():
    db.session.query(Participant).delete()
    db.session.commit()
    return jsonify({"message": "Participants reset successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
