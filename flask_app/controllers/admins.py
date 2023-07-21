from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
from flask_app.models.admin import Admin
from flask_app.models.member import Member

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/admin_login", methods=['POST'])
def login():

    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    admin = Admin.check_email(data)
    if not admin:
        return redirect('/')
    
    if not bcrypt.check_password_hash(admin.password, data['password']):
        #flash("Invalid Password", "login")
        return redirect('/')

    session['admin_id'] = admin.id
    return redirect("/main_page")

@app.route("/main_page")
def dashboard():
    all_members = Member.get_all_members()

    return render_template("dashboard.html", all_members = all_members)
