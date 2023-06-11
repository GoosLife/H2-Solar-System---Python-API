from application import app
from models import planet, hologram
from database import db

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
    new_hologram = hologram.Hologram(1,1) # TODO: Generate unique machine ID
    
    try:
        db.session.add(new_hologram)
        db.session.commit()
        return 'Hologram created successfully: ' + str(new_hologram)
    except Exception as e:
        db.session.rollback()
        return "Failed to create hologram: " + str(e)