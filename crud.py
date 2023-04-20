from typing import List
from model import db, User, Pet, HealthRecord, Vet, FavoriteVet, ContactMessage, connect_to_db

# User CRUD operations
def create_user(username, email, password_hash, first_name, last_name, phone_number=None):
    """Create and return a new user."""
    user = User(username=username, email=email, password_hash=password_hash,
                first_name=first_name, last_name=last_name, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()

    return user

# def get_user_by_email
def get_user_by_email(email):
    """Return a user object with the given email or None if not found."""
    return User.query.filter(User.email == email).first()


def get_user_by_id(user_id):
    """Return a user by their ID."""
    return User.query.get(user_id)

def get_all_users():
    """Return all users in the database."""
    return User.query.all()

def update_user(user, **kwargs):
    """Update user information."""
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()

def delete_user(user):
    """Delete a user."""
    db.session.delete(user)
    db.session.commit()

# Pet CRUD operations
def create_pet(user_id, name, species, breed=None, birthdate=None, photo=None):
    """Create and return a new pet."""
    pet = Pet(user_id=user_id, name=name, species=species, breed=breed, birthdate=birthdate, photo=photo)

    return pet

def get_pet_by_id(pet_id):
    """Return a pet by their ID."""
    return Pet.query.get(pet_id)

def get_all_pets():
    """Return all pets in the database."""
    return Pet.query.all()

def update_pet(pet, **kwargs):
    """Update pet information."""
    for key, value in kwargs.items():
        setattr(pet, key, value)
    db.session.commit()

def get_health_records_by_pet(pet_id: int) -> List[HealthRecord]:
    """Return all health records for a specific pet."""
    return HealthRecord.query.filter(HealthRecord.pet_id == pet_id).all()
   

def delete_pet(pet):
    """Delete a pet."""
    db.session.delete(pet)
    db.session.commit()

# HealthRecord CRUD operations
def create_health_record(pet_id, record_date, weight, weight_unit, vaccination_status, notes):
    """Create and return a new health record."""
    health_record = HealthRecord(pet_id=pet_id, record_date=record_date, weight=weight,
                                  vaccination_status=vaccination_status, weight_unit=weight_unit, notes=notes)
    db.session.add(health_record)
    db.session.commit()

    return health_record

def get_health_record_by_id(record_id):
    """Return a health record by their ID."""
    return HealthRecord.query.get(record_id)

def get_all_health_records():
    """Return all health records in the database."""
    return HealthRecord.query.all()

def update_health_record(health_record, **kwargs):
    """Update health record information."""
    for key, value in kwargs.items():
        setattr(health_record, key, value)
        if 'weight_unit' in kwargs:
            health_record.weight_unit = kwargs['weight_unit']
    db.session.commit()

def delete_health_record_by_id(record_id):
    """Delete a health record by its ID."""
    health_record = get_health_record_by_id(record_id)
    db.session.delete(health_record)
    db.session.commit()



# Vet CRUD operations
def create_vet(name, address, phone_number, email=None, website=None, yelp_id=None):
    """Create and return a new vet."""
    vet = Vet(name=name, address=address, phone_number=phone_number, email=email, website=website, yelp_id=yelp_id)
    db.session.add(vet)
    db.session.commit()

    return vet

def get_vet_by_id(vet_id):
    """Return a vet by their ID."""
    return Vet.query.get(vet_id)

def get_all_vets():
    """Return all vets in the database."""
    return Vet.query.all()

def update_vet(vet, **kwargs):
    """Update vet information."""
    for key, value in kwargs.items():
        setattr(vet, key, value)
    db.session.commit()

def delete_vet(vet):
    """Delete a vet."""
    db.session.delete(vet)
    db.session.commit()

# FavoriteVet CRUD operations
def create_favorite_vet(user, vet, notes=None, reviews=None):
    """Create and return a new favorite vet."""
    favorite_vet = FavoriteVet(user=user, vet=vet, notes=notes, reviews=reviews)
    db.session.add(favorite_vet)
    db.session.commit()

    return favorite_vet

def get_favorite_vet_by_id(favorite_vet_id):
    """Return a favorite vet by their ID."""
    return FavoriteVet.query.get(favorite_vet_id)

def get_all_favorite_vets():
    """Return all favorite vets in the database."""
    return FavoriteVet.query.all()

def update_favorite_vet(favorite_vet, **kwargs):
    """Update favorite vet information."""
    for key, value in kwargs.items():
        setattr(favorite_vet, key, value)
    db.session.commit()

def delete_favorite_vet(favorite_vet):
    """Delete a favorite vet."""
    db.session.delete(favorite_vet)
    db.session.commit()

# Add the new ContactMessage CRUD operations
def create_contact_message(name, email, subject, message):
    """Create and return a new contact message."""
    contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
    db.session.add(contact_message)
    db.session.commit()

    return contact_message

def get_contact_message_by_id(contact_message_id):
    """Return a contact message by their ID."""
    return ContactMessage.query.get(contact_message_id)

def get_all_contact_messages():
    """Return all contact messages in the database."""
    return ContactMessage.query.all()

def delete_contact_message(contact_message):
    """Delete a contact message."""
    db.session.delete(contact_message)
    db.session.commit()

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
