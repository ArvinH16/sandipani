from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.organizer import Organizer
from flask_app.models.member import Member
from flask_app.models.sale import Sale


@app.route("/add_donation/sale/<int:member_id>")
def render_add_sale_page(member_id):
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    data = {
        "member_id": member_id
    }
    member = Member.get_member(data)
    donation_type = "sale"
    return render_template("add_donation.html", member = member, donation_type = donation_type)


@app.route("/add_donation/sale", methods=["POST"])
def add_sale_form():
    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    data = {
        "member_id": request.form["member_id"],
        "amount": request.form["amount"],
        "date": request.form['date'],
        "method": request.form['method'],
        "notes": request.form['notes']
    }
    sale = Sale.create_sale(data)

    return redirect("/main_page")
