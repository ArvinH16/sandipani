from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
#from flask_app.models.admin import Admin
from flask_app.models.member import Member


@app.route("/new_member")
def new_member_page():
    return render_template("new_member_page.html")


@app.route("/add_member", methods=["POST"])
def add_member():

    member = Member.add_member(request.form)

    return redirect("/main_page")

