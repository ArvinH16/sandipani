from flask import Flask
from datetime import timedelta
#from flask_app import app
from flask import session

app = Flask(__name__)
app.secret_key = "sezUisdf343WIjksjddddskfs103928"


# This portion of the code enforces an automatic logout mechanism after 20 minutes of user inactivity.
# It achieves this by clearing the user's session, which holds their user_id.
# Every page in the application incorporates security measures to redirect users if they aren't logged in
# or don't possess a user_id in their session, ensuring the effectiveness of this approach.

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20)  # 20-minute session timeout

# This function runs before each HTTP request to refresh the session, allowing us to track user inactivity accurately.
# It ensures that the session is updated, helping us monitor and manage user interactions effectively.
@app.before_request
def refresh_session():
    session.modified = True
    