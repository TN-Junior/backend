from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


participants = []
next_id = 1  

@app.route("/participants", methods=["GET"])
def get_participants():
   
    return jsonify(participants)

@app.route("/participants", methods=["POST"])
def add_participant():
    
    global next_id
    try:
        data = request.json
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        participation = data.get("participation")

        
        if not first_name or not last_name:
            return jsonify({"error": "First name and last name are required"}), 400
        if not isinstance(participation, int) or participation < 1 or participation > 100:
            return jsonify({"error": "Participation must be a number between 1 and 100"}), 400

        
        participant = {
            "id": next_id,
            "firstName": first_name,
            "lastName": last_name,
            "participation": participation
        }

        participants.append(participant)
        next_id += 1  

        return jsonify({"message": "Participant added successfully", "participant": participant}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/participants/<int:id>", methods=["PUT"])
def update_participant(id):
    
    data = request.json
    for participant in participants:
        if participant["id"] == id:
            participant["firstName"] = data.get("firstName", participant["firstName"])
            participant["lastName"] = data.get("lastName", participant["lastName"])
            participant["participation"] = data.get("participation", participant["participation"])
            return jsonify({"message": "Participant updated successfully", "participant": participant}), 200
    return jsonify({"error": "Participant not found"}), 404

@app.route("/participants/<int:id>", methods=["DELETE"])
def delete_participant(id):
    
    global participants
    participants = [p for p in participants if p["id"] != id]
    return jsonify({"message": f"Participant with ID {id} deleted successfully"}), 200

@app.route("/participants", methods=["DELETE"])
def reset_participants():
    
    global participants, next_id
    participants = []
    next_id = 1  # Reinicia o contador de IDs
    return jsonify({"message": "Participants reset successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
