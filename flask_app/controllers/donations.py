"""
Anant Dhokia & Arvin Hakakian

This file manages all routes, and functions regarding any dollar amount 
donations made to sandipani. Anything from retrieving information, to
adding entries into the database regarding donations is done here.
"""

from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.member import Member
from flask_app.models.donation import Donation


# This route renders the page where organizers can fill out
# a form to add a donation entry for a member. Id is passed
# into the route to specify which member the donation is being
# added to.
@app.route("/add_donation/donation/<int:member_id>")
def render_add_donation_page(member_id):
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
    donation_type = "donation"
    return render_template("add_donation.html", member = member, donation_type = donation_type)

# This route runs when the organizer submits the donation form
# and adds the info into the database under the correct member.
@app.route("/add_donation/donation", methods=["POST"])
def add_donation_form():
    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    data = {
        "member_id": request.form["member_id"],
        "amount": request.form["amount"],
        "date": request.form['date'],
        "method": request.form['method'],
        "event": request.form['event'],
        "notes": request.form['notes']
    } 
      
    Donation.create_donation(data)

    return redirect("/main_page")