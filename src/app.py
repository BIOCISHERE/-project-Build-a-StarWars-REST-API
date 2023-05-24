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
from models import db, User, Character, Planet, Vehicle, Favorites
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

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def add_character_to_fav(user_id, character_id):
    character = Favorites.query.filter_by(id_char=character_id, user_id=user_id)
    if character is None:
        fav_character = Character.query.filter_by(id=character_id).first()
        if fav_character is None:
            return jsonify({'error': 'user not found'}), 404
        else:
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify({'error': 'user not found'}), 400
            else:
                favCharacter = Favorites(id_char=character_id, user_id=user_id)
                db.session.add(favCharacter)
                db.session.commit()
                return jsonify({'msg': 'character added to favorites'}), 201
    else:
        return jsonify({'error': 'character already added to favorites'}), 201

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_fav(user_id, planet_id):
    planet = Favorites.query.filter_by(id_plan=planet_id, user_id=user_id)
    if planet is None:
        fav_planet = Planet.query.filter_by(id=planet_id).first()
        if fav_planet is None:
            return jsonify({'error': 'user not found'}), 404
        else:
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify({'error': 'user not found'}), 400
            else:
                FavPlanet = Favorites(id_plan=planet_id, user_id=user_id)
                db.session.add(FavPlanet)
                db.session.commit()
                return jsonify({'msg': 'planet added to favorites'}), 201
    else:
        return jsonify({'error': 'planet already added to favorites'}), 201

@app.route('/user/<int:user_id>/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_vehicle_to_fav(user_id, vehicle_id):
    vehicle = Favorites.query.filter_by(id_vehic=vehicle_id, user_id=user_id)
    if vehicle is None:
        fav_vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if fav_vehicle is None:
            return jsonify({'error': 'user not found'}), 404
        else:
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify({'error': 'user not found'}), 400
            else:
                favVehicle = Favorites(id_vehic=vehicle_id, user_id=user_id)
                db.session.add(favVehicle)
                db.session.commit()
                return jsonify({'msg': 'vehicle added to favorites'}), 201
    else:
        return jsonify({'error': 'vehicle already added to favorites'}), 201

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['DELETE'])
def delete_fav_character(user_id, character_id):
    character = Favorites.query.filter_by(id_char=characters_id, user_id=user_id).first()
    if character is None:
        return jsonify({'error': 'character not found in favorites'}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': 'character removed from favorites!'}), 200

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(user_id, planet_id):
    planet = Favorites.query.filter_by(id_plan=planet_id, user_id=user_id).first()
    if planet is None:
        return jsonify({'error': 'planet not found in favorites'}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'planet removed from favorites!'}), 200

@app.route('/user/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(user_id, vehicle_id):
    vehicle = Favorites.query.filter_by(id_vehic=vehicle_id, user_id=user_id).first()
    if vehicle is None:
        return jsonify({'error': 'vehicle not found in favorites'}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'msg': 'vehicle removed from favorites!'}), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
