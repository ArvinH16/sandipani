from flask_app.controllers import index, admins, members
from flask_app import app




if __name__ == "__main__":
    app.run(debug=True, port=5000)




