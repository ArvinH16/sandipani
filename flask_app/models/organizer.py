from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Organizer:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.role = data['role']
        self.phone_number = data['phone_number']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


    @classmethod
    def check_email(cls, data):
        
        query = "SELECT * FROM organizers WHERE email = %(email)s"
        result = connectToMySQL('sandipani').query_db(query, data)
        if len(result) < 1:
            return False

        return cls(result[0])
    
    @classmethod
    def add_organizer(cls, data):

        query = "INSERT INTO organizers(first_name, last_name, `description`, phone_number, email, `password`, role) VALUES (%(first_name)s, %(last_name)s, %(description)s, %(phone_number)s, %(email)s, %(password)s, %(role)s)"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @staticmethod
    def sign_up_validation(data):
        is_valid = True

        query = "SELECT * FROM organizers WHERE email = %(email)s"
        result = connectToMySQL('sandipani').query_db(query, data)
        if len(result) >= 1:
            flash("Email is already taken", "sign_up")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email. Please enter a valid email", 'sign_up')
            is_valid = False
        
        if data['password'] != data['pass_confirm']:
            flash("Passwords do not match", "sign_up")
            is_valid = False

        if len(data['password']) < 6:
            flash("passowrds needs to be at least 6 characters long", "sign_up")
            is_valid = False

        return is_valid





    