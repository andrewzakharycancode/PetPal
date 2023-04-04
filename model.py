from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instantiate a SQLAlchemy object to interact with the database
db = SQLAlchemy()

# User model representing the users table in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    # Define a one-to-many relationship between User and Pet
    pets = db.relationship("Pet", backref="user", lazy=True)

# Pet model representing the pets table in the database
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    photo = db.Column(db.String(255), nullable=True)

    # Define a one-to-many relationship between Pet and HealthRecord
    health_records = db.relationship("HealthRecord", backref="pet", lazy=True)

# HealthRecord model representing the health_records table in the database
class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    record_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    weight = db.Column(db.Float, nullable=True)
    vaccination_status = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.Text, nullable=True)

# Vet model representing the vets table in the database
class Vet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    yelp_id = db.Column(db.String(80), unique=True, nullable=False)

    # Define a one-to-many relationship between Vet and FavoriteVet
    favorite_vets = db.relationship("FavoriteVet", backref="vet", lazy=True)

# FavoriteVet model representing the favorite_vets table in the database
class FavoriteVet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey("vet.id"), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    reviews = db.Column(db.Text, nullable=True)