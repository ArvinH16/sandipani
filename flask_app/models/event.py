"""
Anant Dhokia & Arvin Hakakian

This page handles all queries to the database regarding events.
Anything regarding adding, deleting, getting events is all queried
through this file.
"""
from flask_app.config.mysqlconnection import connectToMySQL

class Event:
    # This init function creates a new event object given initialization data.
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.event_date = data['event_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # This method given the correct data, adds a new event into the database.
    @classmethod
    def add_event(cls, data):
        query = "INSERT INTO events (event_name, event_date, description) VALUES (%(event_name)s, %(event_date)s, %(description)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # This method returns all the events currently in the database for displaying purposes
    # on the event dashboard.
    @classmethod
    def get_all_events(cls):
        query = "SELECT * FROM events"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    # This function given the id of the event, deletes the event from
    # the database.
    @classmethod
    def delete_event(cls, data):
        query = "DELETE FROM `events` WHERE id = %(event_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result