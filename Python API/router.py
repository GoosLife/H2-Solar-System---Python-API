from application import app
from models import planet, hologram
from database import db
from sqlalchemy import select

from flask import jsonify

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/planets')
def get_planets():
    planets = planet.Planet.query.all()
    print(planet.Planet.query.all())
    planet_data = []

    for p in planets:
        planet_dict = {
            "id":p.id,
            "name":p.name,
            "description":p.description
            }
        planet_data.append(planet_dict)

    return jsonify(planet_data)

@app.route('/hologram')
def get_hologram():
    statement = select(hologram.Hologram.planetId).filter_by(machineId=1)
    planetId = db.session.execute(statement)
    return planetId

@app.route('/planets/<int:planet_id>')
def get_planet(planet_id):
    queriedPlanet = planet.Planet.query.get_or_404(planet_id);
    return str(queriedPlanet)

@app.route('/hologram/<int:current_planet_id>')
def set_hologram_planet(current_planet_id):
    new_hologram = hologram.Hologram(current_planet_id, 1) # TODO: Generate unique machine ID
    
    try:
        db.session.add(new_hologram)
        db.session.commit()
        return 'Hologram created successfully: ' + str(new_hologram)
    except Exception as e:
        db.session.rollback()
        
        try:
            db.session.execute(db.insert(hologram.Hologram),
                               [{
                                   "PlanetID":new_hologram.planetId,
                                   "MachineID":new_hologram.machineId
                                   }])
            return 'Hologram created successfully: ' + str(new_hologram)
        except Exception as e:
            return "Failed to create hologram: " + str(e)