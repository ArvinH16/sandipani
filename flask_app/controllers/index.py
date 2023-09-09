from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.donation import Donation
from flask_app.models.tatvadarshan import Tatvadarshan
from flask_app.models.student_sponsorship import Student_Sponsorship
from flask_app.models.sale import Sale
from flask_app.models.member import Member
#from flask_app.models.thought import Thought
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def main_page():

    #password = "@Sandipani.org_adminAccount!!"
    #pw_hash = bcrypt.generate_password_hash(password)
    #print(pw_hash)
    #hash_pass = "$2b$12$nYg0ahAbsb41kldxuJQO9OXjMk2.iUIQ1r3RvdSfcy1BVXyUvZEZ2"
    return render_template("sign_in.html")
    

@app.route("/pending_page")
def pending_page():
    if 'organizer_id' in session:
        return redirect("/main_page")
    
    return render_template("pending_page.html")


@app.route("/stats")
def render_stats():

    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")
    
    donation_sum = Donation.get_donation_sum()
    donation_count = Donation.get_num_donations()
    sale_sum = Sale.get_sale_sum()
    sale_count = Sale.get_num_sales()
    tatvadarshan_sum = Tatvadarshan.get_tatvadarshan_sum()
    tatvadarshan_count = Tatvadarshan.get_num_tatvadarshans()
    student_sponsorship_sum = Student_Sponsorship.get_student_sponsorship_sum()
    student_sponsorship_count = Student_Sponsorship.get_num_student_sponsorships()
    member_count = Member.get_member_count()
    archived_member_count = Member.get_archived_member_count()

    print(donation_count)

    return render_template("stats.html", donation_sum = donation_sum, donation_count = donation_count, sale_sum = sale_sum, sale_count = sale_count, tatvadarshan_sum = tatvadarshan_sum, tatvadarshan_count = tatvadarshan_count, student_sponsorship_sum = student_sponsorship_sum, student_sponsorship_count = student_sponsorship_count, member_count = member_count, archived_member_count = archived_member_count)

@app.route("/logout")
def logout():

    session.clear()
    redirect("/")

#test
    