from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Email_list:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_email_list(cls):
        query = "SELECT * FROM email_lists;"
        result = connectToMySQL('sandipani').query_db(query)

        all_email_lists = []

        for email_list in result:
            email_list_object = cls(email_list)
            all_email_lists.append(email_list_object)

        return all_email_lists
