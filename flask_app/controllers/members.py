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

    member = Member.add_member(request.form)

    return redirect("/main_page")

@app.route("/view_member/<int:member_id>")
def view_member(member_id):
    data_member = {
        "member_id": member_id
    }
    member = Member.get_member(data_member)
    
    return render_template("view_member.html", member = member)

@app.route("/edit_member", methods=["POST"])
def edit_member():
    
    member_edited = Member.edit_member(request.form)
    #tested
    return redirect("/main_page")
