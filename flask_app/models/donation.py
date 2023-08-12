from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash
import re

class Donation:
    def __init__(self, data):
        self.id = data['id']
        self.amount = data['amount']
        self.date = data['date']
        self.method = data['method']
        self.event = data['event']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member_id = data['member_id']
        self.member_creator = None


    @classmethod
    def create_donation(cls, data):
        query = "INSERT INTO donations(amount, date, method, event, notes, member_id) VALUES (%(amount)s, %(date)s, %(method)s, %(event)s, %(notes)s, %(member_id)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def delete_member_donations(cls, data):
        query = "DELETE FROM donations WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def get_member_donations(cls, data):
        query = "SELECT * FROM donations WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result



