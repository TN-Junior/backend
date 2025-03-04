from flask import Blueprint, request, jsonify
from .models import Participant
from . import db

main = Blueprint('main', __name__)

@main.route("/participants", methods=["POST", "GET"])
def participants():
    if request.method == "POST":
        try:
            # Recupera os dados JSON da requisição
            data = request.json
            first_name = data.get("firstName", "").strip()
            last_name = data.get("lastName", "").strip()
            participation = data.get("participation")

            # Verifica se todos os campos obrigatórios foram preenchidos
            errors = []
            if not first_name:
                errors.append("First name is required")
            if not last_name:
                errors.append("Last name is required")

            # Valida o campo participation
            if not isinstance(participation, int):
                errors.append("Participation must be a number")
            elif participation < 1 or participation > 100:
                errors.append("Participation must be a number between 1 and 100")

            # Se houver erros, retorna um erro 400
            if errors:
                return jsonify({"error": errors}), 400

            # Cria um novo participante no banco de dados
            new_participant = Participant(
                first_name=first_name,
                last_name=last_name,
                participation=participation
            )

            print("Attempting to add participant to the session...")  # Debugging print

            db.session.add(new_participant)
            db.session.commit()

            # Retorna a resposta com o participante criado
            return jsonify({"message": "Participant added successfully", "participant": {
                "id": new_participant.id,
                "firstName": new_participant.first_name,
                "lastName": new_participant.last_name,
                "participation": new_participant.participation
            }}), 201

        except Exception as e:
            # Log de erro no servidor
            db.session.rollback()  # Desfaz qualquer transação que tenha falhado
            print(f"Error occurred: {str(e)}")  # Log para debugging
            return jsonify({"error": f"Server error: {str(e)}"}), 500

    elif request.method == "GET":
        try:
            # Recupera todos os participantes
            participants = Participant.query.all()
            participants_list = [
                {
                    "id": participant.id,
                    "firstName": participant.first_name,
                    "lastName": participant.last_name,
                    "participation": participant.participation
                }
                for participant in participants
            ]
            return jsonify(participants_list), 200

        except Exception as e:
            return jsonify({"error": f"Error retrieving participants: {str(e)}"}), 500


@main.route("/participants/<int:id>", methods=["PUT", "DELETE"])
def participant(id):
    try:
        # Verifica se o participante existe
        participant = Participant.query.get(id)
        if not participant:
            return jsonify({"error": "Participant not found"}), 404

        if request.method == "PUT":
            # Atualiza os dados do participante
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

        if request.method == "DELETE":
            db.session.delete(participant)
            db.session.commit()
            return jsonify({"message": f"Participant with ID {id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@main.route("/participants", methods=["DELETE"])
def reset_participants():
    try:
        # Reseta todos os participantes
        db.session.query(Participant).delete()
        db.session.commit()
        return jsonify({"message": "Participants reset successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error resetting participants: {str(e)}"}), 500
