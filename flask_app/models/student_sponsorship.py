"""
Anant Dhokia & Arvin Hakakian

This file contains the Student Sponsorship class and all functions related to
processing student sponsorship data for members.
"""
from flask_app.config.mysqlconnection import connectToMySQL


class Student_Sponsorship:
    # Initializes student sponsorship object given form data and commits it to memory
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
    
    # Inserts a student sponsorship entry into the student sponsorship table in sql database.
    @classmethod
    def create_student_sponsorship(cls, data):
        query = "INSERT INTO student_sponsorships(amount, date, method, length, expiry_date, notes, member_id) VALUES(%(amount)s, %(date)s, %(method)s, %(length)s, %(expiry_date)s, %(notes)s, %(member_id)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    # Deletes all of a member's student sponsorships from the database given the member's id.
    @classmethod
    def delete_member_student_sponsorships(cls, data):
        query = "DELETE FROM student_sponsorships WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    # Given a member id, returns all the member's student sponsorships that are in the database.
    @classmethod
    def get_member_student_sponsorships(cls, data):
        query = "SELECT * FROM student_sponsorships WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    # Sums up all the student sponsorship amounts from every student sponroship entered in the database.
    @classmethod
    def get_student_sponsorship_sum(cls):
        query = "SELECT SUM(amount) AS total_amount FROM student_sponsorships;"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    # Returns the number of student sponorships that are in the database.
    @classmethod
    def get_num_student_sponsorships(cls):
        query = "SELECT COUNT(*) AS donation_count FROM student_sponsorships;"
        result = connectToMySQL('sandipani').query_db(query)
        
        return result

    # Finds the sum of all the student sponrorship amounts from every student sponsorship given a member id.
    @classmethod
    def get_member_student_sponsorship_sum(cls, data):
        query = "SELECT SUM(amount) FROM student_sponsorships WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    # Returns the number of student sponsorships that are made by a member given member id.
    @classmethod
    def get_member_num_student_sponsorships(cls, data):
        query = "SELECT COUNT(*) FROM student_sponsorships WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        
        return result