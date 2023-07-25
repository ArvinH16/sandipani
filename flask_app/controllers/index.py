from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def main_page():

    #password = "@Sandipani.org_adminAccount!!"
    #pw_hash = bcrypt.generate_password_hash(password)
    #print(pw_hash)
    #hash_pass = "$2b$12$nYg0ahAbsb41kldxuJQO9OXjMk2.iUIQ1r3RvdSfcy1BVXyUvZEZ2"

    return render_template("index.html")
    

@app.route("/pending_page")
def pending_page():
    return render_template("pending_page.html")
