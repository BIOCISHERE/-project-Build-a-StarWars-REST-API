from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favotites_id = db.Column(db.Integer, db.ForeignKey("Favorites.id"))

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'Character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)
    fav_characters = db.relationship('FavCharacter', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color
        }

class FavCharacter(db.Model):
    __tablename__ = 'FavCharacter'
    id = db.Column(db.Integer, primary_key=True)
    id_of_fav = db.Column(db.Integer, db.ForeignKey(Character.id))
    favorites = db.relationship('Favorites', lazy=True)

    def __repr__(self):
        return '<FavCharacter %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_of_fav": self.id_of_fav
        }    

class Planet(db.Model):
    __tablename__ = 'Planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    fav_planets = db.relationship('FavPlanet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter
        }

class FavPlanet(db.Model):
    __tablename__ = 'FavPlanet'
    id = db.Column(db.Integer, primary_key=True)
    id_of_fav = db.Column(db.Integer, db.ForeignKey(Planet.id))
    favorites = db.relationship('Favorites', lazy=True)

    def __repr__(self):
        return '<FavPlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_of_fav": self.id_of_fav
        }    

class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    passangers = db.Column(db.Integer, nullable=False)
    vehicle_class = db.Column(db.String(120), nullable=False)
    fav_vehicles = db.relationship('FavVehicules', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cost_in_credits": self.cost_in_credits,
            "cargo_capacity": self.cargo_capacity,
            "passangers": self.passangers,
            "vehicle_class": self.vehicle_class
        } 

class FavVehicules(db.Model):
    __tablename__ = 'FavVehicules'
    id = db.Column(db.Integer, primary_key=True)
    id_of_fav = db.Column(db.Integer, db.ForeignKey(Vehicle.id))
    favorites = db.relationship('Favorites', lazy=True)

    def __repr__(self):
        return '<FavVehicules %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_of_fav": self.id_of_fav
        }    

class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id = db.Column(db.Integer, primary_key=True)
    id_char = db.Column(db.Integer, db.ForeignKey(FavCharacter.id))
    id_plan = db.Column(db.Integer, db.ForeignKey(FavPlanet.id))
    id_vehic = db.Column(db.Integer, db.ForeignKey(FavVehicules.id))
    users = db.relationship('User', lazy=True)
    

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_char": self.id_char,
            "id_plan": self.id_plan,
            "id_vehic": self.id_vehic
        }    