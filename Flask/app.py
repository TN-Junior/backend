from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Banco de dados em memória para armazenar os participantes
participants = []

@app.route("/participants", methods=["GET"])
def get_participants():
    """Retorna a lista de participantes com suas porcentagens exatas."""
    return jsonify(participants)

@app.route("/participants", methods=["POST"])
def add_participant():
    """Adiciona um novo participante ao banco de dados."""
    try:
        data = request.json
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        participation = data.get("participation")

        # Validação dos campos
        if not first_name or not last_name:
            return jsonify({"error": "First name and last name are required"}), 400
        if not isinstance(participation, int) or participation < 1 or participation > 100:
            return jsonify({"error": "Participation must be a number between 1 and 100"}), 400

        participants.append({
            "firstName": first_name,
            "lastName": last_name,
            "participation": participation  # Mantendo o valor exato
        })

        return jsonify({"message": "Participant added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/participants", methods=["DELETE"])
def reset_participants():
    """Reseta a lista de participantes."""
    global participants
    participants = []
    return jsonify({"message": "Participants reset successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
