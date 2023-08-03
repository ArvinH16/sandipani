from flask_app import app
from flask import render_template, redirect, request, session, flash
#from flask_app.models.user import User
#from flask_app.models.thought import Thought
#from flask_app.models.admin import Admin
from flask_app.models.member import Member
from flask_app.models.email_list import Email_list


@app.route("/new_member")
def new_member_page():
    email_lists = Email_list.get_all_email_list()
    return render_template("new_member_page.html", email_lists = email_lists)


@app.route("/add_member", methods=["POST"])
def add_member():
    

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
    data_member = {
        "member_id": member_id
    }

    email_lists = Email_list.get_all_email_list()

    email_lists_checked = Email_list.get_member_email_lists(data_member)
    print(email_lists_checked)
    # email_list_ids_checked_list = []
    # for email_list_id_checked in email_list_ids_checked:
    #     email_list_ids_checked_list.append(email_list_id_checked.id)
    email_list_ids = []
    for email_list_checked in email_lists_checked:
        email_list_ids.append(email_list_checked['email_list_id'])
    

    member = Member.get_member(data_member)
    
    return render_template("view_member.html", member = member, email_lists = email_lists, email_list_ids = email_list_ids)

@app.route("/edit_member", methods=["POST"])
def edit_member():
    
    member_edited = Member.edit_member(request.form)

    email_list_checkboxes = request.form.getlist('email_list')

#    member_email_lists = Email_list.get_member_email_lists(request.form['member_id'])

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
