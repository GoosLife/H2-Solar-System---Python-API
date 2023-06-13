from application import app
from models import planet, hologram
from database import db
from flask import jsonify, request
from sqlalchemy import text
from datetime import datetime
from logger import logToConsole as log

@app.route('/')
def index():
    return "Hello, World!"

## PLANETS

@app.route('/planets')
def get_planets():
    planets = planet.Planet.query.all()
    print(planet.Planet.query.all())
    planet_data = []

    for p in planets:
        planet_dict = {
            "planetId":p.planetId,
            "name":p.name,
            "description":p.description
            }
        planet_data.append(planet_dict)

    return jsonify(planet_data)

@app.route('/planets/<int:planet_id>')
def get_planet(planet_id):
    queriedPlanet = planet.Planet.query.get_or_404(planet_id);
    return jsonify(queriedPlanet)

@app.route('/planets/description', methods=["POST"])
def getPlanetDescriptionByLanguage():
    return 0


## HOLOGRAM

# Get hologram ID for machine
@app.route('/hologram/<int:machine_id>')
def get_hologram(machine_id):
    response = app.make_response("")

    hologram_entry = hologram.Hologram.query.filter_by(machineId=machine_id).first()

    if hologram_entry is not None:
        planetId = hologram_entry.planetId
        response.set_data(str(planetId))
    else:
        response.set_data("No hologram found for id " + str(machine_id))

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



# Set hologram
@app.route('/hologram', methods=['POST', 'OPTIONS'])
def set_hologram_planet():
    response = app.make_response("")

    if request.content_type == 'application/json':
        new_planet_id = request.json['planet_id']
        new_machine_id = 1  # TODO: Generate unique machine ID
        
        # Upsert hologram

        try:
            existing_hologram = hologram.Hologram.query.filter_by(machineId=new_machine_id).first()

            # Update hologram

            if existing_hologram:
                existing_hologram.planetId = new_planet_id
                db.session.commit()
                response.set_data('Hologram updated successfully: ' + str(existing_hologram))
            
            # Insert hologram

            else:
                new_hologram = hologram.Hologram(planetId=new_planet_id, machineId=new_machine_id)
                db.session.add(new_hologram)
                db.session.commit()
                response.set_data('Hologram created successfully: ' + str(new_hologram))
        
        # Failed to upsert hologram

        except Exception as e:
            db.session.rollback()
            log(str(e), 'SQL ERROR')
            response.set_data('Failed to create or update hologram.')
    else:
        
        # Invalid request body

        response.set_data('Request body must be JSON')

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response