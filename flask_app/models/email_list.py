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

    #This is for email_list_member database where we correlate members and email lists
    @classmethod
    def add_email_list_member(cls, data):
        query = "INSERT INTO emailList_member(member_id, email_list_id) VALUES(%(member_id)s, %(email_list_id)s)"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def remove_email_list_member(cls, data):
        pass

    @classmethod
    def get_member_email_lists(cls, data):
        query = "SELECT * FROM emailList_member WHERE member_id = %(member_id)s;"

        results = connectToMySQL('sandipani').query_db(query, data)
        # member_email_lists_ids = []
        # for member_email_lists_id in results:
        #     member_email_lists_ids.append(member_email_lists_id.member_id)
        # print(member_email_lists_ids)
        return results


