"""
Anant Dhokia & Arvin Hakakian

This page handles all database queries regarding members. Anything from
creating, deleting, archiving, editing, etc. Is done in this file.
"""
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import email_list


class Member:
    # The init function creates a new instance of a member class with the given data.
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
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.email_list = []

    # This function retrieves all the members from the database for displaying purposes on the
    # organizer dashboard.
    @classmethod
    def get_all_members(cls):
        query = "SELECT * FROM members WHERE is_deleted = 0 ORDER BY created_at DESC LIMIT 50;"
        
        result = connectToMySQL('sandipani').query_db(query)

        all_member_objects = []

        for member in result:
            member_object = cls(member)

            all_member_objects.append(member_object)

        return all_member_objects

    # This function retrieves all archived members from the database
    # for displaying purposes on the organizer dashboard.
    @classmethod
    def get_all_archived_members(cls):
        query = "SELECT * FROM members WHERE is_deleted = 1 ORDER BY created_at DESC LIMIT 50;"
        result = connectToMySQL('sandipani').query_db(query)

        all_member_objects = []

        for member in result:
            member_object = cls(member)

            all_member_objects.append(member_object)

        return all_member_objects
    
    # This function queries the search from the dashboard page made by the user to the database to retreive
    # all search results that are related to the user typed.
    @classmethod
    def get_searched_members(cls, data):
        query = "SELECT * FROM members WHERE LOCATE(%(email)s, email) > 0 AND is_deleted = 0 ORDER BY created_at DESC LIMIT 50;"

        result = connectToMySQL('sandipani').query_db(query, data)
        all_searched_member_objects = []

        for member in result:
            searched_member_object = cls(member)
            all_searched_member_objects.append(searched_member_object)

        return all_searched_member_objects

    # This function queries the search from the dashboard page made by the user to the database to retreive
    # all search results that are related to the user typed.
    @classmethod
    def get_searched_archived_members(cls, data):
        query = "SELECT * FROM members WHERE LOCATE(%(email)s, email) > 0 AND is_deleted = 1 ORDER BY created_at DESC LIMIT 50;"

        result = connectToMySQL('sandipani').query_db(query, data)
        all_searched_member_objects = []

        for member in result:
            searched_member_object = cls(member)
            all_searched_member_objects.append(searched_member_object)

        return all_searched_member_objects

    # This function given the data from the form, will create a new member and add it
    # to the members table in the database
    @classmethod
    def add_member(cls, data):
        query = "INSERT INTO members (first_name, middle_name, last_name, email, spouse, parents, children, street_1, street_2, city, state, zip, country, phone_1, phone_2, notes, organizer_id) VALUES (%(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, %(spouse)s, %(parents)s, %(children)s, %(street_1)s, %(street_2)s, %(city)s, %(state)s, %(zip)s, %(country)s, %(phone_1)s, %(phone_2)s, %(notes)s, 2);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    # This method, given an id, will retrieve all the member's information that they were signed up
    # with along with any email lists they are a part of. This is so that on the dashboard page, when
    # a user wants to view a member's information, it can all be retrieved and displayed.
    @classmethod
    def get_member(cls, data):
        query = "SELECT * FROM members LEFT JOIN emailList_member ON members.id = emailList_member.member_id LEFT JOIN email_lists ON emailList_member.email_list_id = email_lists.id WHERE members.id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        member = cls(result[0])

        # Creates a list of all email lists a member is a part of.
        for member_email_list in result:
            email_list_data = {
                "id": member_email_list['email_list_id'],
                "type": member_email_list['type'],
                "created_at": member_email_list['created_at'],
                "updated_at": member_email_list['updated_at']
            }

            email_list_object = email_list.Email_list(email_list_data)

            member.email_list.append(email_list_object)
        
        return member

    # This funciton queries the database to edit a member's information.
    # When an organizer edits a member's information, this query is run
    # to commit changes to the database.
    @classmethod
    def edit_member(cls, data):
        query = "UPDATE members SET first_name = %(first_name)s, middle_name = %(middle_name)s, last_name = %(last_name)s, email = %(email)s, street_1 = %(street_1)s, street_2 = %(street_2)s, city = %(city)s, state = %(state)s, zip = %(zip)s, country = %(country)s, spouse = %(spouse)s, parents = %(parents)s, children = %(children)s, phone_1 = %(phone_1)s, phone_2 = %(phone_2)s, notes = %(notes)s WHERE id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return result

    # This function archives a member in the database by setting a deleted column
    # to true. This allows us to still keep them in the database, but removes them
    # from the database.
    @classmethod
    def delete_member(cls, data):
        query =  "UPDATE members SET is_deleted = 1 WHERE id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return result
    
    # This function permanently deletes a member from the database.
    # This occurrs when an already archived member is deleted again.
    @classmethod
    def purge_member(cls, data):
        query = "DELETE FROM members WHERE id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        return result
    
    # This function queries the database to find the number of non archived members
    # that are present in the database.
    @classmethod
    def get_member_count(cls):
        query = "SELECT COUNT(*) AS member_count FROM members WHERE is_deleted = 0;"
        result = connectToMySQL('sandipani').query_db(query)
        
        return result
    
    # This function queries the database to fund the number of archived members
    # that are currently present in the database.
    @classmethod
    def get_archived_member_count(cls):
        query = "SELECT COUNT(*) AS member_count FROM members WHERE is_deleted = 1;"
        result = connectToMySQL('sandipani').query_db(query)
        
        return result
    
    # This function unarchives an already archived member to bring them back to
    # the main dashboard page.
    @classmethod
    def unarchive_member(cls, data):
        query = "UPDATE members SET is_deleted = 0 WHERE id = %(member_id)s"
        result = connectToMySQL('sandipani').query_db(query, data)
        
        return result