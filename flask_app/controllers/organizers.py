"""
Anant Dhokia & Arvin Hakakian

This file handles all routes regarding organizers. Anything
from creating, deleting, editing, or changing roles of organizers
is all done here.
"""
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.organizer import Organizer
from flask_app.models.member import Member
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# This route is what is run when a user clicks log in
# on the starting page. The data is collected and checked
# to make sure email and passwords match before creating
# a session and advancing them to the organizer dashboard.
@app.route("/organizer_login", methods=['POST'])
def login():

    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    # Checks to make sure the email is valid
    organizer = Organizer.check_email(data)
    if not organizer:
        flash("Invalid email", "login")
        return redirect('/')
    
    # Hashes password for security and ensures it matches with the database
    if not bcrypt.check_password_hash(organizer.password, data['password']):
        flash("Invalid Password", "login")
        return redirect('/')

    # Makes sure the organizer has been approved before letting them log in.
    if organizer.role == "none":
        flash("You have successfully signed up, but awaiting organizer approval", "login")
        return redirect('/')

    session['organizer_id'] = organizer.id
    session['role'] = organizer.role
    session['first_name'] = organizer.first_name

    return redirect("/main_page")

# This route is run to render the sign up form
# for new organizers to create an account.
@app.route("/sign_up")
def sign_up():

    return render_template("sign_up.html")

# This route is run when an organizer creates their account.
# The data is retrieved and a new organizer is committed to the
# database.
@app.route("/organizer_sign_up", methods=["POST"])
def add_organizer():

    # Ensures password is complicated enough, both passwords entered match, email is valid, etc.
    if not Organizer.sigh_up_validation(request.form):
        return redirect("/sign_up")

    # Hashes password
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
    
    Organizer.add_organizer(data)

    return redirect("/pending_page")

# This route retrieves all data necessary to render the dashboard
# page where organizers can see all members listed and search for
# members.
@app.route("/main_page", methods=['GET', 'POST'])
def dashboard():
    
    # Ensures user is logged in (all routes in this page contain this code)
    if not 'organizer_id' in session:
        return redirect("/")
    
    # Searching members algorithim and saves data to session
    if request.method == 'POST':
        search_email = request.form['query']
        data = {
            "email": search_email
        }
        
        all_members = Member.get_searched_members(data)
        session['search_results'] = [member.__dict__ for member in all_members]
        
        return redirect("/search_results")
    else:
        session.pop('search_results', None)
        all_members = Member.get_all_members()

    return render_template("dashboard.html", all_members = all_members)

# Route runs when an organizer searches for an email.
# Gathers search results from session and displays them on a 
# template.
@app.route("/search_results")
def search_member():
    if not 'organizer_id' in session:
        return redirect("/")

    all_members = session.get('search_results', [])
    return render_template("dashboard.html", all_members = all_members)
    
# This route gathers all organizer data to display for admins
# to manage organizer data.
@app.route("/manage_organizers")
def manage_org_page():

    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] != "admin":
        return redirect("/main_page")

    pending_organizers = Organizer.get_all_pending_organizers()
    all_organizers = Organizer.get_all_organizers()

    return render_template("manage_organizers.html", pending_organizers = pending_organizers, all_organizers = all_organizers)

# This route processes the data when an organizer evaluates
# a pending organizer's data to assign them a role or accept/reject them.
@app.route("/pend_org_form", methods=['POST'])
def process_pend_org_form():
    
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] != "admin":
        return redirect("/main_page")

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
    
# This is the route that runs when an organizer
# edits an organizer's role.
@app.route("/update_organizer", methods=['POST'])
def update_organizer():

    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] != "admin":
        return redirect("/main_page")

    data = {
        "id": request.form["organizer_id"],
        "updated_role": request.form["role"],
        "current_role": request.form["organizer_role"],
        "first_name": request.form["organizer_first_name"]
    }
    # Ensuring the role isn't updated to the one they're already assigned to.
    if data["current_role"] == data["updated_role"]:
        flash("You haven't made any changes to the role to submit.", "update_organizer")
        return redirect("/manage_organizers")
    else:
        Organizer.change_role(data)
        first_name = data['first_name']
        updated_role = data['updated_role']

        flash(f'{first_name} just got their role changed to {updated_role}', "update_organizer")

        return redirect("/manage_organizers")

# This is the route that runs when an admin deletes another
# organizer.
@app.route("/delete_organizer", methods=["POST"])
def delete_organizer():

    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] != "admin":
        return redirect("/main_page")

    data = {
        "id": request.form["organizer_id"],
        "first_name": request.form['organizer_first_name']
    }

    first_name = data['first_name']

    Organizer.delete_organizer(data)
    flash(f'{first_name} just got deleted', "update_organizer")
    return redirect("/manage_organizers")

# This function collects all archived members and implements some
# backend to allow searching to function.
@app.route("/archived_members", methods=['GET', 'POST'])
def archived_page():
    
    if not 'organizer_id' in session:
        return redirect("/")
    
    # Allows users to search and stores data in session to be processed
    if request.method == 'POST':
        search_email = request.form['query']
        data = {
            "email": search_email
        }
        all_members = Member.get_searched_archived_members(data)

        session['search_results'] = [member.__dict__ for member in all_members]
        return redirect("/archived_search_results")

    else:
        session.pop('search_results', None)
        all_archived_members = Member.get_all_archived_members()

    return render_template("archived_member_dashboard.html", all_archived_members = all_archived_members)

# Route runs when an organizer searches for an email.
# Gathers search results from session and displays them on a 
# template for archived members.
@app.route("/archived_search_results")
def search_archived_member():
    if not 'organizer_id' in session:
        return redirect("/")

    all_archived_members = session.get('search_archived_results', [])
    
    return render_template("archived_member_dashboard.html", all_archived_members = all_archived_members)