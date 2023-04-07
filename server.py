from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)
from model import db, connect_to_db, User, Pet, HealthRecord, Vet, FavoriteVet
from crud import (create_user, get_user_by_id, get_pet_by_id, get_all_users, update_user, delete_user ) 
                #   get_all_users, update_user, delete_user,
                #   create_pet, get_pet_by_id, get_all_pets, update_pet, delete_pet,
                #   create_health_record, get_health_record_by_id, get_all_health_records,
                #   update_health_record, delete_health_record,
                #   create_vet, get_vet_by_id, get_all_vets, update_vet, delete_vet,
                #   create_favorite_vet, get_favorite_vet_by_id, get_all_favorite_vets,
                #   update_favorite_vet, delete_favorite_vet)
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Show homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Register a new user
@app.route('/register', methods=['POST'])
def register_user():
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

# Log in a user
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    user = get_user_by_email(email)

    if not user or not user.check_password(password):
        flash('Invalid email or password. Please try again.')
        return redirect('/')
    else:
        session['user_id'] = user.id
        flash(f'Welcome, {user.first_name}!')
        return redirect('/dashboard')

# Show user dashboard
@app.route('/dashboard')
def show_dashboard():
    if 'user_id' not in session:
        flash('Please log in to view your dashboard.')
        return redirect('/')

    user = get_user_by_id(session['user_id'])

    return render_template('dashboard.html', user=user)

# View all pets of the user
@app.route('/pets')
def view_pets():
    if 'user_id' not in session:
        flash('Please log in to view your pets.')
        return redirect('/')

    user = get_user_by_id(session['user_id'])

    return render_template('pets.html', user=user)

# Add a pet to the user's account
@app.route('/add_pet', methods=['POST'])
def add_pet():
    if 'user_id' not in session:
        flash('Please log in to add a pet.')
        return redirect('/')

    user_id = session['user_id']
    name = request.form['name']
    species = request.form['species']
    breed = request.form['breed']
    birthdate = request.form['birthdate']
    photo = request.form['photo']

    pet = crud.create_pet(user_id, name, species, breed, birthdate, photo)

    flash(f'{pet.name} has been added to your pets.')
    return redirect('/pets')


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
