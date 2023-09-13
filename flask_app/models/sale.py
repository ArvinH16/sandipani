from flask_app.config.mysqlconnection import connectToMySQL
#from flask_app.models import thought
from flask import flash
import re

class Sale:
    def __init__(self, data):
        self.id = data['id']
        self.amount = data['amount']
        self.date = data['date']
        self.method = data['method']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member_id = data['member_id']
        self.member_creator = None


    @classmethod
    def create_sale(cls, data):
        query = "INSERT INTO sales(amount, date, method, notes, member_id) VALUES (%(amount)s, %(date)s, %(method)s, %(notes)s, %(member_id)s);"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def delete_member_sales(cls, data):
        query = "DELETE FROM sales WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def get_member_sales(cls, data):
        query = "SELECT * FROM sales WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result
    
    @classmethod
    def get_sale_sum(cls):
        query = "SELECT SUM(amount) AS total_amount FROM sales;"
        result = connectToMySQL('sandipani').query_db(query)

        return result
    
    @classmethod
    def get_num_sales(cls):
        query = "SELECT COUNT(*) AS donation_count FROM sales;"
        result = connectToMySQL('sandipani').query_db(query)
        
        return result
    
    @classmethod
    def get_member_sale_sum(cls, data):
        query = "SELECT SUM(amount) FROM sales WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)

        return result

    @classmethod
    def get_member_num_sales(cls, data):
        query = "SELECT COUNT(*) FROM sales WHERE member_id = %(member_id)s;"
        result = connectToMySQL('sandipani').query_db(query, data)
        
        return result