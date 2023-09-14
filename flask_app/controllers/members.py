"""
Anant Dhokia & Arvin Hakakian

This page handles all routes regarding members. Any functions such
as getting member info, adding members, summarizing member data all
occurrs in this page.
"""
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.member import Member
from flask_app.models.email_list import Email_list
from flask_app.models.student_sponsorship import Student_Sponsorship
from flask_app.models.tatvadarshan import Tatvadarshan
from flask_app.models.sale import Sale
from flask_app.models.donation import Donation

# This route renders the page where an organizer can
# fill out information regarding a new member joining
# sandipani.
@app.route("/new_member")
def new_member_page():
    # Ensures user is logged in (all routes in this page contain this code)
    if not 'organizer_id' in session:
        return redirect("/")
    
    # Ensures that organizer has authorization to access this page (most routes in this page contain this code)
    if session['role'] == "member_viewer":
        return redirect("/main_page")
    
    # This gets all email lists in the event that more are added in the future for modularity
    email_lists = Email_list.get_all_email_list()
    return render_template("new_member_page.html", email_lists = email_lists)

# This route processes the form once the user hits the submit
# button for adding a new member. The function retrieves the data
# and adds the member in the database.
@app.route("/add_member", methods=["POST"])
def add_member():
    
    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] == "member_viewer":
        return redirect("/main_page")
    
    data_member = {
        "first_name": request.form['first_name'],
        "middle_name": request.form['middle_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "spouse": request.form['spouse'],
        "parents": request.form['parents'],
        "children": request.form['children'],
        "street_1": request.form['street_1'],
        "street_2": request.form['street_2'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zip": request.form['zip'],
        "country": request.form['country'],
        "phone_1": request.form['phone_1'],
        "phone_2": request.form['phone_2'],
        "notes": request.form['notes']
    }

    member = Member.add_member(data_member)

    # Iterates through each email list the user is a part of
    # and commits the data to the database to keep modularity
    # if more email lists are added in the futute, and to keep
    # easy access to email list members.
    email_list_checkboxes = request.form.getlist('email_list')
    for email_list_checkbox in email_list_checkboxes:
        data_email_list = {
            "member_id": member,
            "email_list_id": int(email_list_checkbox)
        }
        Email_list.add_email_list_member(data_email_list)


    return redirect("/main_page")

# This route gathers all information relating to a member
# and passes it into a template so their info can be viewed
# by organizers.
@app.route("/view_member/<int:member_id>")
def view_member(member_id):

    if not 'organizer_id' in session:
        return redirect("/")
    
    data_member = {
        "member_id": member_id
    }

    # Retrieves all email lists to check whether a member is a part of each one
    email_lists = Email_list.get_all_email_list()
    member = Member.get_member(data_member)

    # Iterates through email lists member is a part of and compares to 
    # all email lists to create a list of email lists the member is a part of.
    email_list_ids = []
    for email_list_joined in member.email_list:
        email_list_ids.append(email_list_joined.id)

    return render_template("view_member.html", member = member, email_lists = email_lists, email_list_ids = email_list_ids)

# This route gathers all information relating to an
# archived member and passes it into a template so their
# info can be viewed by organizers.
@app.route("/view_archived_member/<int:member_id>")
def view_archived_member(member_id):

    if not 'organizer_id' in session:
        return redirect("/")

    
    data_member = {
        "member_id": member_id
    }

    # Retrieves all email lists to check whether a member is a part of each one
    email_lists = Email_list.get_all_email_list()
    member = Member.get_member(data_member)

    # Iterates through email lists member is a part of and compares to 
    # all email lists to create a list of email lists the member is a part of.
    email_list_ids = []
    for email_list_joined in member.email_list:
        email_list_ids.append(email_list_joined.id)
    
    return render_template("view_archived_member.html", member = member, email_lists = email_lists, email_list_ids = email_list_ids)

# This route runs when a member is edited from the view member
# screen and the function processes the updated info and commits
# the edited data to the database
@app.route("/edit_member", methods=["POST"])
def edit_member():
    
    if not 'organizer_id' in session:
        return redirect("/")

    if session['role'] == "member_viewer":
        return redirect("/main_page")

    Member.edit_member(request.form)
    # Purge their email list member entries in the database
    # so that the new edited ones can be added.
    Email_list.purge_email_list_member(request.form)

    email_list_checkboxes = request.form.getlist('email_list')

    for email_list_checkbox in email_list_checkboxes:
        data_email_list = {
            "member_id": request.form['member_id'],
            "email_list_id": int(email_list_checkbox)
        }
        Email_list.add_email_list_member(data_email_list)

    return redirect("/main_page")


# This route runs when the user deletes a member.
# The member isn't actually deleted, just archived
# so they aren't shown on the main page, but on another
# archived member dashboard.
@app.route("/delete_member", methods=["POST"])
def delete_member():
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer":
        return redirect("/main_page")

    Member.delete_member(request.form)

    return redirect("/main_page")

# This route runs when the user deletes an already archived
# member. This completely purges all the member's data including
# any donations they've contributed, and all email lists they
# are a part of.
@app.route("/purge_member", methods=["POST"])
def purge_member():
    
    if not 'organizer_id' in session:
        return redirect("/")  
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")
    
    Donation.delete_member_donations(request.form)
    Tatvadarshan.delete_member_tatvadarshans(request.form)
    Student_Sponsorship.delete_member_student_sponsorships(request.form)
    Sale.delete_member_sales(request.form)
    Email_list.purge_email_list_member(request.form)

    Member.purge_member(request.form)

    return redirect("/archived_members")

# This route allows an archived member to become unarchived
# given the member id.
@app.route("/unarchive_member/<int:member_id>")
def unarchive_member(member_id):
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer":
        return redirect("/main_page")

    data = {
        'member_id': member_id
    }
    
    Member.unarchive_member(data)

    return redirect('/archived_members')

# This route allows users to view the donation info of a member.
# The function gathers all their donation information and passes it
# into the template so that it can be viewed.
@app.route("/view_member_donations/<int:member_id>")
def get_member_donations(member_id):
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    donations = Donation.get_member_donations({"member_id": member_id})
    num_donations = Donation.get_member_num_donations({"member_id": member_id})
    total_donation = Donation.get_member_donation_sum({"member_id": member_id})
    
    sales = Sale.get_member_sales({"member_id": member_id})
    num_sales = Sale.get_member_num_sales({"member_id": member_id})
    total_sale = Sale.get_member_sale_sum({"member_id": member_id})

    tatvadarshans = Tatvadarshan.get_member_tatvadarshans({"member_id": member_id})
    num_tatvadarshans = Tatvadarshan.get_member_num_tatvadarshans({"member_id": member_id})
    total_tatvadarshan = Tatvadarshan.get_member_tatvadarshan_sum({"member_id": member_id})

    student_sponsorships = Student_Sponsorship.get_member_student_sponsorships({"member_id": member_id})
    num_student_sponsorships = Student_Sponsorship.get_member_num_student_sponsorships({"member_id": member_id})
    total_student_sponsorship = Student_Sponsorship.get_member_student_sponsorship_sum({"member_id": member_id})

    return render_template("view_member_donations.html",
        num_donations = num_donations,
        total_donation = total_donation, 
        num_sales = num_sales, 
        total_sale = total_sale, 
        num_tatvadarshans = num_tatvadarshans, 
        total_tatvadarshan = total_tatvadarshan, 
        num_student_sponsorships = num_student_sponsorships, 
        total_student_sponsorship = total_student_sponsorship,
        donations = donations,
        tatvadarshans = tatvadarshans,
        sales = sales,
        student_sponsorships = student_sponsorships)