from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify, g)
from model import db, connect_to_db, User, Pet, HealthRecord, Vet, FavoriteVet
from crud import (create_user, get_user_by_id, get_pet_by_id, get_user_by_email, create_pet, create_health_record, get_health_records_by_pet, update_health_record, create_contact_message, delete_health_record_by_id) 
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Read the Yelp API key from the environment variable
yelp_api_key = os.getenv("YELP_API_KEY")


app = Flask(__name__)
app.secret_key = "dev"
from jinja2 import Environment, StrictUndefined


# # Show homepage
# @app.route('/')
# def homepage():
#     return render_template('homepage.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)

@app.route('/')
def homepage():
    if g.user:
        return redirect('/dashboard')
    else:
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

# @app.route('/health_records/<int:pet_id>')
# def view_health_records(pet_id):
#     pet = get_pet_by_id(pet_id)
#     health_records = get_health_records_by_pet(pet_id)
#     return render_template('health_records.html', pet=pet, health_records=health_records)

# @app.route('/health_records/<int:pet_id>')
# def view_health_records(pet_id):
#     pet = get_pet_by_id(pet_id)

#     return render_template('health_records.html', pet=pet)

@app.route('/add_health_record/<int:pet_id>', methods=['GET', 'POST'])
def add_health_record(pet_id):
    pet = get_pet_by_id(pet_id)

    if request.method == 'GET':
        return render_template('add_health_record.html', pet=pet)

    record_date = request.form['record_date'] #need to be a dat/time object
    weight = request.form['weight'] #needs to be a float
    weight_unit = request.form['weight_unit']
    vaccination_status = request.form['vaccination_status']
    notes = request.form['notes']

    health_record = create_health_record(pet_id, record_date, weight, weight_unit, vaccination_status, notes)  
    print(health_record)
    flash('Health record added.')

    return redirect(url_for('view_health_records', pet_id=pet_id))

@app.route("/view_health_records/<int:pet_id>")
def view_health_records(pet_id):
    health_records= get_health_records_by_pet(pet_id)
    pet = get_pet_by_id(pet_id)
    health_records_dict_list = []
    for record in health_records:
        health_records_dict_list.append(record.to_dict())
    print(health_records_dict_list)
    return render_template("health_records.html", pet=pet, health_records=health_records, health_records_dict_list=health_records_dict_list)

@app.route('/edit_health_record/<int:record_id>', methods=['GET', 'POST'])
def edit_health_record(record_id):
    health_record = get_health_record_by_id(record_id)

    if request.method == 'GET':
        return render_template('edit_health_record.html', health_record=health_record)

    record_date = request.form['record_date'] 
    weight = request.form['weight']
    weight_unit = request.form['weight_unit'] 
    vaccination_status = request.form['vaccination_status']
    notes = request.form['notes']

    update_health_record(health_record, record_date=record_date, weight=weight, weight_unit=weight_unit, vaccination_status=vaccination_status, notes=notes)
    flash('Health record updated.')

    return redirect('/dashboard')  # Redirect to the Dashboard after updating the health record

def get_health_record_by_id(record_id):
    return HealthRecord.query.get(record_id)

# Delete health record
@app.route('/pets/<int:pet_id>/health_records/delete/<int:record_id>', methods=['POST'])
def delete_health_record(pet_id, record_id):
    if 'user_id' not in session:
        flash('Please log in to delete a health record.')
        return redirect('/')

    delete_health_record_by_id(record_id)
    flash('Health record deleted!')

    return redirect(f"/view_health_records/{pet_id}")



# Search for vets
@app.route('/vetfinder', methods=['GET', 'POST'])
def search_vets():
    page = int(request.args.get("page", 1))
    offset = (page - 1) * 20
    location = request.args.get("location", "")

    if request.method == 'POST':
        location = request.form.get("location")

    if location:
        url = f"https://api.yelp.com/v3/businesses/search?location={location}&term=vet&sort_by=rating&limit=20&offset={offset}"
        headers = {"accept": "application/json", "Authorization": f"Bearer {yelp_api_key}"}
        response = requests.get(url, headers=headers)
        data = response.json()  # Parse JSON response
        businesses = data.get("businesses", [])  # Extract businesses list
        return render_template('search_vets.html', businesses=businesses, location=location, page=page)

    else:
        return render_template('search_vets.html', page=page)


#View user's favorite vets
@app.route('/favorite_vets')
def view_favorite_vets():
    if 'user_id' not in session:
        flash('Please log in to view your favorite vets.')
    return redirect('/')


# Add a vet to the user's favorite vets
@app.route('/add_favorite_vet', methods=['POST'])
def add_favorite_vet():
    if 'user_id' not in session:
        flash('Please log in to add a favorite vet.')
    return redirect('/')

# Contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        create_contact_message(name, email, subject, message)
        return render_template('contact_success.html')

    return render_template('contact.html')

@app.route('/contact/success')
def contact_success():
    return render_template('contact_success.html')




#Log out the user
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True) 