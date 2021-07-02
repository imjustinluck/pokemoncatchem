from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pokemons = []
        self.favorites = []
    
    @classmethod
    def get_all(cls):
        pass

    @classmethod
    def get_one(cls, data):
        pass

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("pokemon_schema").query_db(query,data)
        if len(result) < 1:
            return False
        return User(result[0])

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('pokemon_schema').query_db(query,data)

    @classmethod
    def friend(cls, data):
        query = "INSERT INTO favorites (user_id, pokemon_id) VALUES (%(user_id)s, %(pokemon_id)s);"
        return connectToMySQL('pokemon_schema').query_db(query,data)

    @classmethod
    def update(cls, data):
        pass
    
    @classmethod
    def delete(cls, data):
        pass

    @staticmethod
    def validate_entry(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash("First Name must have a value.")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last Name must have a value.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("E-mail is invalid")
            is_valid = False
        elif User.check_duplicate({'email':data['email']}):
            flash("You already have an account.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be 8 characters long")
            is_valid = False
        else:
            if data['password'] != data['confirm_password']:
                flash("Passwords don't match")
                is_valid = False
        return is_valid

    @staticmethod
    def check_duplicate(data):
        duplicate = False
        query = "Select email FROM users WHERE email = %(email)s;"
        result = connectToMySQL('pokemon_schema').query_db(query, data)
        if result:
            duplicate = True
        return duplicate

    @staticmethod
    def login_validate(post_data):
        user_from_db = User.get_by_email({'email':post_data['email']})
        if not user_from_db:
            flash("Wrong Email / Password Combination")
            return False
        if not bcrypt.check_password_hash(user_from_db.password, post_data['password']):
            flash("Wrong Email / Password Combination")
            return False
        return True