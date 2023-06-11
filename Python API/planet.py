from database import db

class Planet(db.Model):
    __tablename__ = "Planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.id}. {self.name}:<br>&emsp;{self.description}"

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description