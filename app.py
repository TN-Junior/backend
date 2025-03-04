from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configurar o banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/participants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    participation = db.Column(db.Integer, nullable=False)

# Criar o banco de dados caso não exista
with app.app_context():
    if not os.path.exists("instance/participants.db"):
        db.create_all()

@app.route("/participants", methods=["GET"])
def get_participants():
    participants = Participant.query.all()
    return jsonify([
        {"id": p.id, "firstName": p.firstName, "lastName": p.lastName, "participation": p.participation}
        for p in participants
    ])

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

        participant = Participant(firstName=first_name, lastName=last_name, participation=participation)
        db.session.add(participant)
        db.session.commit()

        return jsonify({"message": "Participant added successfully", "participant": {
            "id": participant.id, "firstName": participant.firstName, "lastName": participant.lastName, "participation": participant.participation
        }}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/participants/<int:id>", methods=["PUT"])
def update_participant(id):
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({"error": "Participant not found"}), 404

    data = request.json
    participant.firstName = data.get("firstName", participant.firstName)
    participant.lastName = data.get("lastName", participant.lastName)
    participant.participation = data.get("participation", participant.participation)

    db.session.commit()
    return jsonify({"message": "Participant updated successfully", "participant": {
        "id": participant.id, "firstName": participant.firstName, "lastName": participant.lastName, "participation": participant.participation
    }}), 200

@app.route("/participants/<int:id>", methods=["DELETE"])
def delete_participant(id):
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({"error": "Participant not found"}), 404

    db.session.delete(participant)
    db.session.commit()
    return jsonify({"message": f"Participant {id} deleted successfully"}), 200

@app.route("/participants", methods=["DELETE"])
def reset_participants():
    db.session.query(Participant).delete()
    db.session.commit()
    return jsonify({"message": "All participants deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
