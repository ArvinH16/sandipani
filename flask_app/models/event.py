from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Event:
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.event_date = data['event_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add_event(cls, data):
        query = "INSERT INTO events (event_name, event_date, description) VALUES (%(event_name)s, %(event_date)s, %(description)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def get_all_events(cls):
        query = "SELECT * FROM events"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    @classmethod
    def delete_event(cls, data):
        query = "DELETE FROM `events` WHERE id = %(event_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result