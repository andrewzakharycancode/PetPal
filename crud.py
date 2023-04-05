from model import db, User, Pet, HealthRecord, Vet, FavoriteVet

# User CRUD operations
def create_user(username, email, password_hash, first_name, last_name, phone_number=None):
    """Create and return a new user."""
    user = User(username=username, email=email, password_hash=password_hash,
                first_name=first_name, last_name=last_name, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()

    return user

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
def create_pet(user, name, species, breed=None, birthdate=None, photo=None):
    """Create and return a new pet."""
    pet = Pet(user=user, name=name, species=species, breed=breed, birthdate=birthdate, photo=photo)
    db.session.add(pet)
    db.session.commit()

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

def delete_pet(pet):
    """Delete a pet."""
    db.session.delete(pet)
    db.session.commit()

# HealthRecord CRUD operations
def create_health_record(pet, record_date, weight=None, vaccination_status=None, notes=None):
    """Create and return a new health record."""
    health_record = HealthRecord(pet=pet, record_date=record_date, weight=weight,
                                  vaccination_status=vaccination_status, notes=notes)
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
    db.session.commit()

def delete_health_record(health_record):
    """Delete a health record."""
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
