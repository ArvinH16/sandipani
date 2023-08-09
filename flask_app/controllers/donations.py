from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
from flask_app.models.organizer import Organizer
from flask_app.models.member import Member
from flask_app.models.donation import Donation


@app.route("/add_donation/donation/<int:member_id>")
def render_add_donation_page(member_id):
    data = {
        "member_id": member_id
    }
    member = Member.get_member(data)
    return render_template("add_donation.html", member = member)


@app.route("/add_donation/donation", methods=["POST"])
def add_donation_form():
    data = {
        "member_id": request.form["member_id"],
        "amount": request.form["amount"],
        "date": request.form['date'],
        "method": request.form['method'],
        "event": request.form['event'],
        "notes": request.form['notes'],
    }
    donation = Donation.create_donation(data)

    return redirect("/main_page")
