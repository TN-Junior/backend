from . import db

def init_db():
    with db.app.app_context():
        db.create_all()
