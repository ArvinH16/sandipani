"""
Anant Dhokia & Arvin Hakakian

This file manages all routes, and functions regarding any student
sponsorships made to sandipani. Anything from retrieving information, to
adding entries into the database regarding donations is done here.
"""
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.member import Member
from flask_app.models.tatvadarshan import Tatvadarshan

# This route renders the page where organizers can fill out
# a form to add a tatvadarshan entry for a member. Id is passed
# into the route to specify which member the tatvadarshan
# is being added to.
@app.route("/add_donation/tatvadarshan/<int:member_id>")
def render_add_tatvadarshan_page(member_id):
    # Ensures user is logged in (all routes in this page contain this code)
    if not 'organizer_id' in session:
        return redirect("/")
    
    # Ensures that organizer has authorization to access this page (all routes in this page contain this code)
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    data = {
        "member_id": member_id
    }
    member = Member.get_member(data)

    donation_type = "tatvadarshan"
    return render_template("add_donation.html", member = member, donation_type = donation_type)

# This route runs when the organizer submits the tatvadarshan form
# and adds the info into the database under the correct member.
@app.route("/add_donation/tatvadarshan", methods=["POST"])
def add_tatvadarshan_form():

    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    data = {
        "member_id": request.form["member_id"],
        "amount": request.form["amount"],
        "date": request.form['date'],
        "method": request.form['method'],
        "length": request.form['length'],
        "expiry_date": request.form['expiry_date'],
        "notes": request.form["notes"]
    }
    
    Tatvadarshan.create_tatvadarshan(data)

    return redirect("/main_page")
