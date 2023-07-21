from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash


class Member:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.middle_name = data['middle_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.spouse = data['spouse']
        self.parents = data['parents']
        self.children = data['children']
        self.street_1 = data['street_1']
        self.street_2 = data['street_2']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.country = data['country']
        self.phone_1 = data['phone_1']
        self.phone_2 = data['phone_2']
        self.notes = data['notes']
        self.email_list = data['email_list']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_members(cls):
        query = "SELECT * FROM members"
        result = connectToMySQL('sandipani').query_db(query)

        all_member_objects = []

        for member in result:
            member_object = cls(member)

            all_member_objects.append(member_object)

        return all_member_objects

