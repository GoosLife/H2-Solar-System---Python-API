from application import app
from models import planet, hologram
from database import db
from flask import jsonify, request
from logger import logToConsole as log

# SEND PRE-FLIGHT
@app.before_request
def before_request():
    if request.method == "OPTIONS":
            return _build_cors_preflight_response()

# INDEX ENDPOINT (CAN BE USED TO TEST CONNECTIVITY)

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
    planet_id = request.json['planet_id']
    language = request.json['language']
    description = planet.Planet.getDescription(planet_id, language)
    return description


## HOLOGRAM

# Get hologram ID for machine
@app.route('/hologram/<int:machine_id>')
def get_hologram(machine_id):
    hologram_entry = hologram.Hologram.query.filter_by(machineId=machine_id).first()

    if hologram_entry is not None:
        planetId = hologram_entry.planetId
        return str(planetId)
    else:
        return "No hologram found for id " + str(machine_id)


# Set hologram
@app.route('/hologram', methods=['POST'])
def set_hologram_planet():
    if request.content_type == 'application/json':
        new_planet_id = request.json['planet_id']
        new_machine_id = 1  # TODO: Generate unique machine ID
        
        # Upsert hologram

        try:
            hologram.Hologram.upsert(new_planet_id, new_machine_id)
            db.session.commit()

        # Failed to upsert hologram

        except Exception as e:
            db.session.rollback()
            log(str(e), 'SQL ERROR')
            'Failed to create or update hologram.'
    else:
        
        # Invalid request body

        return 'Request body must be JSON'

def _build_cors_preflight_response():
    response = app.make_response("")
    response.headers.add('Access-Control-Allow-Origin', '10.108.144.0/21')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response