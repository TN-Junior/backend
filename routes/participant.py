from flask import Blueprint, request, jsonify
from models.participant import db, Participant

participant_bp = Blueprint('participant', __name__)

@participant_bp.route("/participants", methods=["GET", "POST", "OPTIONS"])
def participants():
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    if request.method == "GET":
        participants = Participant.query.all()
        return jsonify([{
            "id": p.id,
            "firstName": p.first_name,
            "lastName": p.last_name,
            "participation": p.participation
        } for p in participants])

    if request.method == "POST":
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
