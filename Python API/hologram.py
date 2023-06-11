from database import db

class Hologram(db.Model):
    planetId = db.Column(db.Integer, primary_key=True)
    machineId = db.Column(db.Integer, primary_key=True, unique=True)

    __table_args__ = (
        db.UniqueConstraint("planetId", "machineId", name="uq_planet_machine"),
        )

    def __repr__(self):
        return f"Planet: {self.planetId}, Machine: {self.machineId}"

    def __init__(self, planetId, machineId):
        self.planetId = planetId
        self.machineId = machineId