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
        flash("Invalid email", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(organizer.password, data['password']):
        flash("Invalid Password", "login")
        return redirect('/')

    session['organizer_id'] = organizer.id
    return redirect("/main_page")


@app.route("/sign_up")
def sign_up():

    return render_template("sign_up.html")

@app.route("/organizer_sign_up", methods=["POST"])
def add_organizer():

    if not Organizer.sigh_up_validation(request.form):
        return redirect("/sign_up")


    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "phone_number" : request.form['phone_number'],
        "email" : request.form['email'],
        "password" : pw_hash,
        "description" : request.form['description'],
        "role" : "none"
    }
    
    organizer = Organizer.add_organizer(data)

    return redirect("/pending_page")


@app.route("/main_page")
def dashboard():
    all_members = Member.get_all_members()

    return render_template("dashboard.html", all_members = all_members)


@app.route("/manage_organizers")
def manage_org_page():
    pending_organizers = Organizer.get_all_pending_organizers()
    all_organizers = Organizer.get_all_organizers()

    return render_template("manage_organizers.html", pending_organizers = pending_organizers, all_organizers = all_organizers)

@app.route("/pend_org_form", methods=['POST'])
def process_pend_org_form():
    data = {
        "id": request.form["pending_organizers_id"],
        "updated_role": request.form["role"],
        "decision": request.form["decision"]
    }

    if data["decision"] == "deny":
        Organizer.delete_organizer(data)
        return redirect("/manage_organizers")
    else:
        Organizer.change_role(data)
        return redirect("/manage_organizers")
    
@app.route("/update_organizer", methods=['POST'])
def update_organizer():
    data = {
        "id": request.form["organizer_id"],
        "updated_role": request.form["role"],
        "current_role": request.form["organizer_role"],
        "first_name": request.form["organizer_first_name"]
    }

    if data["current_role"] == data["updated_role"]:
        flash("You haven't made any changes to the role to submit.", "update_organizer")
        return redirect("/manage_organizers")
    else:
        Organizer.change_role(data)
        first_name = data['first_name']
        updated_role = data['updated_role']

        flash(f'{first_name} just got their role changed to {updated_role}', "update_organizer")

        return redirect("/manage_organizers")

@app.route("/delete_organizer", methods=["POST"])
def delete_organizer():
    data = {
        "id": request.form["organizer_id"],
        "first_name": request.form['organizer_first_name']
    }

    first_name = data['first_name']

    Organizer.delete_organizer(data)
    flash(f'{first_name} just got deleted', "update_organizer")
    return redirect("/manage_organizer")


        