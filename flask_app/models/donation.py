"""
Anant Dhokia & Arvin Hakakian

This file contains the Donation class and all functions related to
processing donation data for members.
"""
from flask_app.config.mysqlconnection import connectToMySQL

class Donation:
    # Initializes donation object given form data and commits it to memory
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

    # Inserts a donation entry into the donations table in sql database.
    @classmethod
    def create_donation(cls, data):
        query = "INSERT INTO donations(amount, date, method, event, notes, member_id) VALUES (%(amount)s, %(date)s, %(method)s, %(event)s, %(notes)s, %(member_id)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # Deletes all of a member's donations from the database given the member's id.
    @classmethod
    def delete_member_donations(cls, data):
        query = "DELETE FROM donations WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # Given a member id, returns all the member's donations that are in the database.
    @classmethod
    def get_member_donations(cls, data):
        query = "SELECT * FROM donations WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # Sums up all the donation amounts from every donation entered in the database.
    @classmethod
    def get_donation_sum(cls):
        query = "SELECT SUM(amount) AS total_amount FROM donations;"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    # Returns the number of donations that are in the database.
    @classmethod
    def get_num_donations(cls):
        query = "SELECT COUNT(*) AS donation_count FROM donations;"
        result = connectToMySQL('sandipani').query_db(query)
        
        return result

    # Finds the sum of all the donation amounts from every donation given a member id.
    @classmethod
    def get_member_donation_sum(cls, data):
        query = "SELECT SUM(amount) FROM donations WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    # Returns the number of donations that are made by a member given member id.
    @classmethod
    def get_member_num_donations(cls, data):
        query = "SELECT COUNT(*) FROM donations WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        
        return result