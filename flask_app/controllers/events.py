"""
Anant Dhokia & Arvin Hakakian

This file manages all routes regarding events. Anything from
adding, deleting, and viewing events is all routed from this page.
"""
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.event import Event

# This route retrieves all events from the database and passes
# them into an html template so users can view a list of all
# entered events.
@app.route("/manage_events")
def manage_events_page():
    # Ensures user is logged in (all routes in this page contain this code)
    if not 'organizer_id' in session:
        return redirect("/")
    
    all_events = Event.get_all_events()
    return render_template("manage_events.html", all_events = all_events)

# This route takes the user to a page where they can fill out
# information regarding creating a new event.
@app.route("/add_event_page")
def render_add_event_page():
    if not 'organizer_id' in session:
        return redirect("/")
    
    # Ensures that organizer has authorization to access this page (most routes in this page contain this code)
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")
    
    return render_template("add_event.html")

# This route is run when the user submits the add event form and commits
# the new event data to the database.
@app.route("/add_event", methods=['POST'])
def add_event():
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")
    
    data = {
        "event_name": request.form['event_name'],
        "event_date": request.form['event_date'],
        "description": request.form['description']
    }
    event = Event.add_event(data)

    return redirect("/manage_events")

# This route runs when the user clicks the delete event button
# on the event dashboard. The route runs code to remove the event
# from the database.
@app.route("/delete_event/<int:event_id>")
def delete_event(event_id):
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] != "admin":
        return redirect("/main_page")

    data = {
        "event_id": event_id
    }
    
    Event.delete_event(data)
    return redirect("/manage_events")