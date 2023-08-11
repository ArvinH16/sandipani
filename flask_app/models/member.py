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
        self.email_list = []

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
    def get_searched_members(cls, data):
        #query = "SELECT * FROM members WHERE email LIKE '%a%';"
        query = "SELECT * FROM members WHERE LOCATE(%(email)s, email) > 0;"
        #query = "SELECT * FROM members WHERE CHARINDEX(%(email)s, email) > 0;"

        result = connectToMySQL('sandipani').query_db(query, data)
        all_searched_member_objects = []

        for member in result:
            searched_member_object = cls(member)
            all_searched_member_objects.append(searched_member_object)

        return all_searched_member_objects


    @classmethod
    def add_member(cls, data):
        #Add admin id from session later when we protect pages
        #add email list when fixed
        query = "INSERT INTO members (first_name, middle_name, last_name, email, spouse, parents, children, street_1, street_2, city, state, zip, country, phone_1, phone_2, notes, organizer_id) VALUES (%(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, %(spouse)s, %(parents)s, %(children)s, %(street_1)s, %(street_2)s, %(city)s, %(state)s, %(zip)s, %(country)s, %(phone_1)s, %(phone_2)s, %(notes)s, 2);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @classmethod
    def get_member(cls, data):
        #query = "SELECT * FROM members WHERE id = %(member_id)s;"
        query = "SELECT * FROM members LEFT JOIN emailList_member ON members.id = emailList_member.member_id LEFT JOIN email_lists ON emailList_member.email_list_id = email_lists.id WHERE members.id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        member = cls(result[0])
        print("member with empty list")
        print(member)
        for member_email_list in result:
            email_list_data = {
                "id": member_email_list['email_list_id'],
                "type": member_email_list['type'],
                "created_at": member_email_list['created_at'],
                "updated_at": member_email_list['updated_at']
            }

            email_list_object = email_list.Email_list(email_list_data)

            print("printed email list object")
            print(email_list_object)

            member.email_list.append(email_list_object)
        
        print("member with email list object")
        print(member)
        return member

        
        #return cls(result[0])


        #query = "SELECT * FROM members LEFT JOIN emailList_member ON members.id = emailList_member.member_id;"

        # for member in result:
        #     one_member = cls(member)

        #     member_email_list = {
        #         "id": member['emailList_member.id'],
        #         "type": member['emailList_member.type'],
        #         "created_at": member['emailList_member.created_at'],
        #         "updated_at": member['emailList_member.updated_at']
        #     }

    @classmethod
    def edit_member(cls, data):
        query = "UPDATE members SET first_name = %(first_name)s, middle_name = %(middle_name)s, last_name = %(last_name)s, email = %(email)s, street_1 = %(street_1)s, street_2 = %(street_2)s, city = %(city)s, state = %(state)s, zip = %(zip)s, country = %(country)s, spouse = %(spouse)s, parents = %(parents)s, children = %(children)s, phone_1 = %(phone_1)s, phone_2 = %(phone_2)s, notes = %(notes)s WHERE id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return result

    @classmethod
    def delete_member(cls, data):
        query = "DELETE FROM members WHERE id = %(member_id)s;"
        email_list.Email_list.purge_email_list_member(data)
        result = connectToMySQL('sandipani').query_db(query, data)
        return result
    

