"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    user = User.query.all()
    all_user = list(map(lambda x: x.serialize(), user))

    return jsonify(all_user), 200

@app.route('/character', methods=['GET'])
def get_character():
    character = Character.query.all()
    all_character = list(map(lambda x: x.serialize(), character))

    return jsonify(all_character), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), planet))

    return jsonify(all_planet), 200

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    vehicle = Vehicle.query.all()
    all_vehicle = list(map(lambda x: x.serialize, vehicle))

    return jsonify(all_vehicle), 200

@app.route('/user/favorite', methods=['GET'])
def get_user_fav():
    user_fav = Favorites.query.all()
    all_user_fav = list(map(lambda x: x.serialize(), user_fav))

    return jsonify(all_user_fav), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_id(character_id):
    id_character = Character.query.get(character_id)

    return jsonify(id_character.serialize()), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    id_planet = Planet.query.get(planet_id)

    return jsonify(id_planet.serialize()), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_id(vehicle_id):
    id_vehicle = Vehicle.query.get(vehicle_id)

    return jsonify(id_vehicle.serialize()), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
