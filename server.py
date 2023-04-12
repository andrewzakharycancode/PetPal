from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)
from model import db, connect_to_db, User, Pet, HealthRecord, Vet, FavoriteVet
from crud import (create_user, get_user_by_id, get_pet_by_id, get_user_by_email, create_pet) 

app = Flask(__name__)
app.secret_key = "dev"
from jinja2 import Environment, StrictUndefined


# Show homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')

    email = request.form['email']
    password_hash = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    phone_number = request.form['phone_number']

    user = get_user_by_email(email)

    if user:
        flash('An account with this email already exists. Please log in.')
    else:
        create_user(username, email, password_hash, first_name, last_name, phone_number)
        flash('Account created! Please log in.')

    return redirect('/')

# About
@app.route('/about')
def about():
    return render_template('about.html')


# Get user by email
@app.route('/api/user', methods=['GET'])
def get_user():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    })


# Log in a user
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    user = get_user_by_email(email)
    print(f"User: {user}")

    if not user or not user.check_password(password):
        flash('Invalid email or password. Please try again.')
        return redirect('/')
    else:
        session['user_id'] = user.id
        flash(f'Welcome, {user.first_name}!')
        return redirect('/dashboard')


    

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to view your dashboard.')
        return redirect('/')

    pets = Pet.query.filter_by(user_id=session["user_id"]).all()
    return render_template('dashboard.html', pets=pets)


# # Show user dashboard
# @app.route('/dashboard')
# def show_dashboard():
#     if 'user_id' not in session:
#         flash('Please log in to view your dashboard.')
#         return redirect('/')

#     user = get_user_by_id(session['user_id'])

#     return render_template('dashboard.html', user=user)

# View all pets of the user
@app.route('/pets')
def view_pets():
    if 'user_id' not in session:
        flash('Please log in to view your pets.')
        return redirect('/')

    user = get_user_by_id(session['user_id'])

    return render_template('pets.html', user=user)

# Add a pet to the user's account

@app.route("/add_pet", methods=["POST"])
def add_pet():
    """Add a pet for the logged-in user."""

    # Get the form data
    pet_name = request.form["pet_name"]
    pet_species = request.form["pet_species"] 
    user_id = session["user_id"]

    # Create a new pet and add it to the database
    # create_pet = Pet(name=pet_name, species=pet_species, owner_id=user_id)  # Change this line
    new_pet = create_pet(user_id, pet_name, pet_species)
    db.session.add(new_pet)
    db.session.commit()

    flash(f"{pet_name} has been added to your pets!")
    return redirect("/dashboard")



# @app.route('/add_pet', methods=['POST'])
# def add_pet():
#     if 'user_id' not in session:
#         flash('Please log in to add a pet.')
#         return redirect('/')

#     user_id = session['user_id']
#     name = request.form['name']
#     species = request.form['species']
#     breed = request.form['breed']
#     birthdate = request.form['birthdate']
#     photo = request.form['photo']

#     pet = crud.create_pet(user_id, name, species, breed, birthdate, photo)

#     flash(f'{pet.name} has been added to your pets.')
#     return redirect('/pets')

# Add the get route
# @app.route('/add_pet', methods=['POST'])

# View health records for a specific pet
@app.route('/health_records/<int:pet_id>')
def view_health_records(pet_id):
    pet = get_pet_by_id(pet_id)

    return render_template('health_records.html', pet=pet)

# Add a health record for a specific pet
@app.route('/add_health_record', methods=['POST'])
def add_health_record():
    pet_id = request.form['pet_id']
    record_date = request.form['record_date']
    weight = request.form['weight']
    vaccination_status = request.form['vaccination_status']
    notes = request.form['notes']

    health_record = crud.create_health_record(pet_id, record_date, weight, vaccination_status, notes)

    flash('Health record added.')

    return redirect(url_for('view_health_records', pet_id=pet_id))

# Search for vets
@app.route('/search_vets')
def search_vets():
    return render_template('search_vets.html')

#View user's favorite vets
@app.route('/favorite_vets')
def view_favorite_vets():
    if 'user_id' not in session:
        flash('Please log in to view your favorite vets.')
    return redirect('/')

#user = crud.get_user_by_id(session['user_id'])
#return render_template('favorite_vets.html', user=user)

# Add a vet to the user's favorite vets
@app.route('/add_favorite_vet', methods=['POST'])
def add_favorite_vet():
    if 'user_id' not in session:
        flash('Please log in to add a favorite vet.')
    return redirect('/')


#user_id = session['user_id']
#vet_id = request.form['vet_id']
#notes = request.form['notes']
#reviews = request.form['reviews']

#favorite_vet = crud.create_favorite_vet(user_id, vet_id, notes, reviews)

#flash('Vet added to your favorite vets.')
#return redirect('/favorite_vets')

#Log out the user
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True) 