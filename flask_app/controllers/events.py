from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.event import Event

@app.route("/manage_events")
def manage_events_page():
    if not 'organizer_id' in session:
        return redirect("/")
    
    all_events = Event.get_all_events()
    return render_template("manage_events.html", all_events = all_events)

@app.route("/add_event_page")
def render_add_event_page():
    if not 'organizer_id' in session:
        return redirect("/")
    
    if session['role'] == "member_viewer" or session['role'] == "member_editor":
        return redirect("/main_page")
    
    return render_template("add_event.html")

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