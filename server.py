from flask_app.controllers import index, organizers, members, tatvadarshans, donations, student_sponsorships, sales, events
from flask_app import app




if __name__ == "__main__":
    #app.run(debug=True, port=5000)
    app.run(debug=True, port=3500, host='0.0.0.0')




