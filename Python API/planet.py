from database import db
from sqlalchemy.sql import func
from logger import logToConsole as log

class Planet(db.Model):
    __tablename__ = "Planets"

    planetId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.planetId}. {self.name}:<br>&emsp;{self.description}"

    def __init__(self, planetId, name, description):
        self.planetId = planetId
        self.name = name
        self.description = description

    @classmethod
    def getDescription(cls, planet_id, language_id):
        result = db.session.execute(func.GetPlanetDescription(planet_id, language_id))
        description = result.scalar()
        return description