from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def main_page():

    #password = "zhYsj12@Sandipani.org_adminAccount!!"
    #pw_hash = bcrypt.generate_password_hash(password)
    #print(pw_hash)

    return render_template("index.html")
    

