from flask import Blueprint, request, jsonify
from .models import Participant
from . import db

main = Blueprint('main', __name__)

@main.route("/participants", methods=["POST", "GET"])
def participants():
    """
    Operações para obter e adicionar participantes.

    ---
    get:
      description: Retorna todos os participantes.
      responses:
        200:
          description: Lista de participantes.
          schema:
            type: array
            items:
              properties:
                id:
                  type: integer
                  example: 1
                firstName:
                  type: string
                  example: "João"
                lastName:
                  type: string
                  example: "Silva"
                participation:
                  type: integer
                  example: 50

    post:
      description: Adiciona um novo participante.
      parameters:
        - in: body
          name: body
          required: true
          schema:
            properties:
              firstName:
                type: string
                example: "João"
              lastName:
                type: string
                example: "Silva"
              participation:
                type: integer
                example: 50
      responses:
        201:
          description: Participante adicionado com sucesso.
        400:
          description: Erro nos dados enviados.
    """
    if request.method == "POST":
        try:
            data = request.json
            first_name = data.get("firstName", "").strip()
            last_name = data.get("lastName", "").strip()
            participation = data.get("participation")

            errors = []
            if not first_name:
                errors.append("First name is required")
            if not last_name:
                errors.append("Last name is required")
            if not isinstance(participation, int):
                errors.append("Participation must be a number")
            elif participation < 1 or participation > 100:
                errors.append("Participation must be between 1 and 100")

            if errors:
                return jsonify({"error": errors}), 400

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
            db.session.rollback()
            return jsonify({"error": f"Server error: {str(e)}"}), 500

    elif request.method == "GET":
        try:
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
    """
    Atualiza ou remove um participante pelo ID.

    ---
    put:
      description: Atualiza um participante.
      parameters:
        - in: path
          name: id
          required: true
          type: integer
          example: 1
        - in: body
          name: body
          required: true
          schema:
            properties:
              firstName:
                type: string
                example: "Carlos"
              lastName:
                type: string
                example: "Almeida"
              participation:
                type: integer
                example: 60
      responses:
        200:
          description: Participante atualizado com sucesso.
        404:
          description: Participante não encontrado.

    delete:
      description: Remove um participante pelo ID.
      parameters:
        - in: path
          name: id
          required: true
          type: integer
          example: 1
      responses:
        200:
          description: Participante deletado com sucesso.
        404:
          description: Participante não encontrado.
    """
    try:
        participant = Participant.query.get(id)
        if not participant:
            return jsonify({"error": "Participant not found"}), 404

        if request.method == "PUT":
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
