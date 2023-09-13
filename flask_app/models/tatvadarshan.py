from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Tatvadarshan:
    def __init__(self, data):
        self.id = data['id']
        self.amount = data['amount']
        self.date = data['date']
        self.method = data['method']
        self.length = data['length']
        self.expiry_date = data['expiry_date']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member_id = data['member_id']
        self.member_creator = None

    @classmethod
    def create_tatvadarshan(cls, data):
        query = "INSERT INTO tatvadarshans(amount, date, method, `length`, expiry_date, notes, member_id) VALUES (%(amount)s, %(date)s, %(method)s, %(length)s, %(expiry_date)s, %(notes)s, %(member_id)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @classmethod
    def delete_member_tatvadarshans(cls, data):
        query = "DELETE FROM tatvadarshans WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def get_member_tatvadarshans(cls, data):
        query = "SELECT * FROM tatvadarshans WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @classmethod
    def get_tatvadarshan_sum(cls):
        query = "SELECT SUM(amount) AS total_amount FROM tatvadarshans;"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    @classmethod
    def get_num_tatvadarshans(cls):
        query = "SELECT COUNT(*) AS donation_count FROM tatvadarshans;"
        result = connectToMySQL('sandipani').query_db(query)
        
        return result
    
    @classmethod
    def get_member_tatvadarshan_sum(cls, data):
        query = "SELECT SUM(amount) FROM tatvadarshans WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @classmethod
    def get_member_num_tatvadarshans(cls, data):
        query = "SELECT COUNT(*) FROM tatvadarshans WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        
        return result