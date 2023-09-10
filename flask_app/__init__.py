from flask import Flask
from datetime import timedelta
#from flask_app import app
from flask import session

app = Flask(__name__)
app.secret_key = "sezUisdf343WIjksjddddskfs103928"

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20)  # 20-minute session timeout

@app.before_request
def refresh_session():
    session.modified = True
    