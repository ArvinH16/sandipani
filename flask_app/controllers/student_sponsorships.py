from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
from flask_app.models.organizer import Organizer
from flask_app.models.member import Member
from flask_app.models.student_sponsorship import Student_Sponsorship


@app.route("/add_donation/student_sponsorship/<int:member_id>")
def render_add_student_sponsorship_page(member_id):
    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    data = {
        "member_id": member_id
    }
    member = Member.get_member(data)

    donation_type = "student_sponsorship"
    return render_template("add_donation.html", member = member, donation_type = donation_type)


@app.route("/add_donation/student_sponsorship", methods=["POST"])
def add_student_sponsorship_form():
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
    student_sponsorship = Student_Sponsorship.create_student_sponsorship(data)

    return redirect("/main_page")
