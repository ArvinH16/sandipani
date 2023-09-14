"""
Anant Dhokia & Arvin Hakakian

This file contains the class for email list objects and handles all
queries to the database regarding anything related to email lists. 
And relations between members and email lists.
"""
from flask_app.config.mysqlconnection import connectToMySQL

class Email_list:
    # The init class creates a new email list object
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # This method returns all different types of email lists from the database
    # in the form of a list of email lists
    @classmethod
    def get_all_email_list(cls):
        query = "SELECT * FROM email_lists;"
        result = connectToMySQL('sandipani').query_db(query)

        all_email_lists = []

        for email_list in result:
            email_list_object = cls(email_list)
            all_email_lists.append(email_list_object)

        return all_email_lists

    # This function is to correlate a member with an email list to show
    # which members are signed up for which email lists.
    @classmethod
    def add_email_list_member(cls, data):
        query = "INSERT INTO emailList_member(member_id, email_list_id) VALUES(%(member_id)s, %(email_list_id)s)"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    # This function deletes all email list member entries from the database
    # Function is used to either delete a member, or to clear data before
    # the member is edited to show new email list info.
    @classmethod
    def purge_email_list_member(cls, data):
        query = "DELETE FROM emailList_member WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return result

    # This function given a member id returns all the email lists the given
    # member is a part of.
    @classmethod
    def get_member_email_lists(cls, data):
        query = "SELECT * FROM emailList_member WHERE member_id = %(member_id)s;"
        results = connectToMySQL('sandipani').query_db(query, data)
        
        return results


