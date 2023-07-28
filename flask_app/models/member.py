from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash
from flask_app.models import email_list


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
        #self.email_list = data['email_list']
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

    @classmethod
    def add_member(cls, data):
        #Add admin id from session later when we protect pages
        #add email list when fixed
        query = "INSERT INTO members (first_name, middle_name, last_name, email, spouse, parents, children, street_1, street_2, city, state, zip, country, phone_1, phone_2, notes, organizer_id) VALUES (%(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, %(spouse)s, %(parents)s, %(children)s, %(street_1)s, %(street_2)s, %(city)s, %(state)s, %(zip)s, %(country)s, %(phone_1)s, %(phone_2)s, %(notes)s, 2);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @classmethod
    def get_member(cls, data):
        query = "SELECT * FROM members WHERE id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return cls(result[0])

    @classmethod
    def edit_member(cls, data):
        query = "UPDATE members SET first_name = %(first_name)s, middle_name = %(middle_name)s, last_name = %(last_name)s, email = %(email)s, street_1 = %(street_1)s, street_2 = %(street_2)s, city = %(city)s, state = %(state)s, zip = %(zip)s, country = %(country)s, spouse = %(spouse)s, parents = %(parents)s, children = %(children)s, phone_1 = %(phone_1)s, phone_2 = %(phone_2)s, notes = %(notes)s WHERE id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return result
    

