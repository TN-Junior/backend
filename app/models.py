from . import db

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    participation = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name, last_name, participation):
        if not first_name or not last_name:
            raise ValueError("First name and last name cannot be empty")
        if not (1 <= participation <= 100):
            raise ValueError("Participation must be between 1 and 100")

        self.first_name = first_name
        self.last_name = last_name
        self.participation = participation

    def __repr__(self):
        return f'<Participant {self.first_name} {self.last_name}>'
