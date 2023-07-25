from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
from flask_app.models.organizer import Organizer
from flask_app.models.member import Member

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/organizer_login", methods=['POST'])
def login():

    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    organizer = Organizer.check_email(data)
    if not organizer:
        return redirect('/')
    
    if not bcrypt.check_password_hash(organizer.password, data['password']):
        #flash("Invalid Password", "login")
        return redirect('/')

    session['organizer_id'] = organizer.id
    return redirect("/main_page")


@app.route("/sign_up")
def sign_up():

    return render_template("sign_up.html")

@app.route("/organizer_sign_up", methods=["POST"])
def add_organizer():

    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "phone_number" : request.form['phone_number'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "description" : request.form['description'],
        "role" : request.form['role']
    }
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    organizer = Organizer.add_organizer(data)

    return redirect("/pending_page")

    

@app.route("/main_page")
def dashboard():
    all_members = Member.get_all_members()

    return render_template("dashboard.html", all_members = all_members)
