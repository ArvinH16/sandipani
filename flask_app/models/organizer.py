"""
Anant Dhokia & Arvin Hakakian

This pages serves any database queries relating to oranizers.
Anything from adding, deleting, editing roles, managing sign ins,
and pending organizers is all done in this file.
"""
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Organizer:
    # This init function creates a new organizer instance given the data.
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
        

    # This function checks whether a given email is already present in the database.
    # This is to avoid multiple organizers with the same email.
    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM organizers WHERE email = %(email)s"
        result = connectToMySQL('sandipani').query_db(query, data)
        if len(result) < 1:
            return False

        return cls(result[0])
    
    # This function given data adds a new organizer to the database
    @classmethod
    def add_organizer(cls, data):
        query = "INSERT INTO organizers(first_name, last_name, `description`, phone_number, email, `password`, role) VALUES (%(first_name)s, %(last_name)s, %(description)s, %(phone_number)s, %(email)s, %(password)s, %(role)s)"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # This function given an id, deletes an orgnaizer from the database.
    @classmethod
    def delete_organizer(cls, data):
        query = "DELETE FROM organizers WHERE id = %(id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # This function given a new role, and an id, updates an organizer's role in the database.
    @classmethod
    def change_role(cls, data):
        query = "UPDATE organizers SET role = %(updated_role)s WHERE id = %(id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # This function retrieves all organizers that are yet to be assigned a role
    # and are still awaiting approval from an administrator. This is for displaying
    # purposes for the admin's organizer dashboard for them to manage current and pending
    # organizers.
    @classmethod
    def get_all_pending_organizers(cls):
        query = "SELECT * FROM organizers WHERE role = 'none';"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    # This function retrieves all organizers that have been assigned a role.
    # This is for displaying purposes on the admin's manage organizers page where
    # they can see all current and pending organizers.
    @classmethod
    def get_all_organizers(cls):
        query = "SELECT * FROM organizers WHERE role != 'none';"
        result = connectToMySQL('sandipani').query_db(query)

        return result

    # This method ensures that when an organizer signs up, their email isn't already
    # taken, their email is a valid email, their passwords match the confirm password
    # field, and their password is secure enough.
    @staticmethod
    def sigh_up_validation(data):
        
        is_valid = True

        query = "SELECT * FROM organizers WHERE email = %(email)s"
        result = connectToMySQL('sandipani').query_db(query, data)
        if len(result) >= 1:
            flash("Email is already taken", "sign_up")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email. Please emter a valid email", 'sign_up')
            is_valid = False

        if data['password'] != data['pass_confirm']:
            flash("Passwords do not match", "sign_up")
            is_valid = False

        if len(data['password']) < 6:
            flash("Password needs to be at least 6 characters long", "sign_up")
            is_valid = False
            
        return is_valid
        
