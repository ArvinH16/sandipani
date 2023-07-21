from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Admin:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


    @classmethod
    def check_email(cls, data):
        
        query = "SELECT * FROM admins WHERE email = %(email)s"
        result = connectToMySQL('sandipani').query_db(query, data)
        if len(result) < 1:
            return False

        return cls(result[0])

    