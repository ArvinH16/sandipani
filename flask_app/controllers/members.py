from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
#from flask_app.models.admin import Admin
from flask_app.models.member import Member
from flask_app.models.email_list import Email_list
from flask_app.models.student_sponsorship import Student_Sponsorship
from flask_app.models.tatvadarshan import Tatvadarshan
from flask_app.models.sale import Sale
from flask_app.models.donation import Donation


@app.route("/new_member")
def new_member_page():
    if not 'organizer_id' in session:
        return redirect("/")
    
    email_lists = Email_list.get_all_email_list()
    return render_template("new_member_page.html", email_lists = email_lists)


@app.route("/add_member", methods=["POST"])
def add_member():
    
    if not 'organizer_id' in session:
        return redirect("/")
    
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

    #email_lists = Email_list.get_all_email_list()

    # for email_list in email_lists:
    #     if str(email_list.id) in request.form:
    #         data_email_list = {
    #             "member_id": member,
    #             "email_list_id": email_list.id
    #         }
    #         Email_list.add_email_list_member(data_email_list)
    email_list_checkboxes = request.form.getlist('email_list')
    for email_list_checkbox in email_list_checkboxes:
        data_email_list = {
            "member_id": member,
            "email_list_id": int(email_list_checkbox)
        }
        Email_list.add_email_list_member(data_email_list)


    return redirect("/main_page")


@app.route("/view_member/<int:member_id>")
def view_member(member_id):

    if not 'organizer_id' in session:
        return redirect("/")

    
    data_member = {
        "member_id": member_id
    }

    email_lists = Email_list.get_all_email_list()
    member = Member.get_member(data_member)

    email_list_ids = []
    for email_list_joined in member.email_list:
        email_list_ids.append(email_list_joined.id)
    
    return render_template("view_member.html", member = member, email_lists = email_lists, email_list_ids = email_list_ids)

@app.route("/view_archived_member/<int:member_id>")
def view_archived_member(member_id):

    if not 'organizer_id' in session:
        return redirect("/")

    
    data_member = {
        "member_id": member_id
    }

    email_lists = Email_list.get_all_email_list()
    member = Member.get_member(data_member)

    email_list_ids = []
    for email_list_joined in member.email_list:
        email_list_ids.append(email_list_joined.id)
    
    return render_template("view_archived_member.html", member = member, email_lists = email_lists, email_list_ids = email_list_ids)

@app.route("/edit_member", methods=["POST"])
def edit_member():
    
    if not 'organizer_id' in session:
        return redirect("/")

    
    Member.edit_member(request.form)

    Email_list.purge_email_list_member(request.form)

    email_list_checkboxes = request.form.getlist('email_list')

#    member_email_lists = Email_list.get_member_email_lists(request.form['member_id'])
    

    Email_list.purge_email_list_member(request.form)

    for email_list_checkbox in email_list_checkboxes:
        data_email_list = {
            "member_id": request.form['member_id'],
            "email_list_id": int(email_list_checkbox)
        }
        Email_list.add_email_list_member(data_email_list)
#    for email_list in member_email_lists:
#       print(email_list)
    #tested
    return redirect("/main_page")

@app.route("/delete_member", methods=["POST"])
def delete_member():
    if not 'organizer_id' in session:
        return redirect("/")

    Member.delete_member(request.form)

    return redirect("/main_page")

@app.route("/purge_member", methods=["POST"])
def purge_member():
    if not 'organizer_id' in session:
        return redirect("/")  
    
    Donation.delete_member_donations(request.form)
    Tatvadarshan.delete_member_tatvadarshans(request.form)
    Student_Sponsorship.delete_member_student_sponsorships(request.form)
    Sale.delete_member_sales(request.form)
    Email_list.purge_email_list_member(request.form)

    Member.purge_member(request.form)

    return redirect("/archived_members")


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


@app.route("/view_member_donations/<int:member_id>")
def get_member_donations(member_id):
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")

    donations = Donation.get_member_donations({"member_id": member_id})
    num_donations = 0
    total_donation = 0
    for donation in donations:
        total_donation += donation['amount']
        num_donations += 1
    
    sales = Sale.get_member_sales({"member_id": member_id})
    num_sales = 0
    total_sale = 0
    for sale in sales:
        total_sale += sale['amount']
        num_sales += 1

    tatvadarshans = Tatvadarshan.get_member_tatvadarshans({"member_id": member_id})
    num_tatvadarshans = 0
    total_tatvadarshan = 0
    for tatvadarshan in tatvadarshans:
        total_tatvadarshan += tatvadarshan['amount']
        num_tatvadarshans += 1

    student_sponsorships = Student_Sponsorship.get_member_student_sponsorships({"member_id": member_id})
    num_student_sponsorships = 0
    total_student_sponsorship = 0
    for student_sponsorship in student_sponsorships:
        total_student_sponsorship += student_sponsorship["amount"]
        num_student_sponsorships += 1

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