"""
Anant Dhokia & Arvin Hakakian

This page handles all routes having to do with logging in,
handling new organizer requests, logging out, and other basic
website functions.
"""
from flask_app import app
from flask import render_template, redirect, session
from flask_app.models.donation import Donation
from flask_app.models.tatvadarshan import Tatvadarshan
from flask_app.models.student_sponsorship import Student_Sponsorship
from flask_app.models.sale import Sale
from flask_app.models.member import Member
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# This route renders the sign in page for users
# coming into the website to be able to sign in.
@app.route("/")
def main_page():
    return render_template("sign_in.html")
    
# This route takes new users to a page where they see confirmation of their
# sign up and that they are pending approval from an admin to start use of
# the application
@app.route("/pending_page")
def pending_page():
    # Only allows organizers who have just signed up to access this page.
    # Approved organizers cannot access this page.
    if 'organizer_id' in session:
        return redirect("/main_page")
    
    return render_template("pending_page.html")

# This route gathers information about all types of donations,
# member counts, archived member counts, and sends them to a
# template where the information can be viewed.
@app.route("/stats")
def render_stats():
    # Ensures user is logged in (most routes in this page contain this code)
    if not 'organizer_id' in session:
        return redirect("/")
    
    # Ensures that organizer has authorization to access this page (most routes in this page contain this code)
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

    return render_template("stats.html", 
        donation_sum = donation_sum, 
        donation_count = donation_count, 
        sale_sum = sale_sum, 
        sale_count = sale_count, 
        tatvadarshan_sum = tatvadarshan_sum, 
        tatvadarshan_count = tatvadarshan_count,
        student_sponsorship_sum = student_sponsorship_sum, 
        student_sponsorship_count = student_sponsorship_count, 
        member_count = member_count, 
        archived_member_count = archived_member_count)

# This route logs out the user by clearing
# their session and redirecting them to the
# login page.
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")