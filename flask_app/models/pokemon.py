from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Pokemon:
    def __init__(self,data):
        pass

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM pokemons WHERE id = %(id)s;"
        return connectToMySQL('pokemon_schema').query_db(query, data)

    @classmethod
    def get_four(cls, data):
        query = "SELECT pokemons.id, favorites.pokemon_id, name, isShiny, img, type, ability FROM users LEFT JOIN pokemons ON users.id = pokemons.user_id LEFT JOIN favorites ON favorites.pokemon_id = pokemons.id WHERE users.id = %(user_id)s ORDER BY pokemons.id DESC LIMIT 4;"
        results = connectToMySQL('pokemon_schema').query_db(query, data)
        pokemons = []
        for poke in results:
            pokemons.append(poke)
        return pokemons
    
    @classmethod
    def get_seven(cls):
        query = "SELECT * FROM pokemons JOIN favorites ON pokemons.id = favorites.pokemon_id JOIN users ON users.id = favorites.user_id ORDER BY pokemons.id DESC LIMIT 7;"
        results = connectToMySQL('pokemon_schema').query_db(query)
        pokemons = []
        for poke in results:
            pokemons.append(poke)
        return pokemons

    @classmethod
    def create(cls, data):
        query = "INSERT INTO pokemons (user_id, pokedex, name, isShiny, img, type, ability) VALUES (%(user_id)s, %(pokedex)s, %(name)s, %(isShiny)s, %(img)s, %(type)s, %(ability)s);"
        return connectToMySQL('pokemon_schema').query_db(query,data)
    
    @classmethod
    def wild(cls, data):
        query = "INSERT INTO pokemons (pokedex, name, isShiny, img, type, ability) VALUES (%(pokedex)s, %(name)s, %(isShiny)s, %(img)s, %(type)s, %(ability)s);"
        return connectToMySQL('pokemon_schema').query_db(query,data)

    @classmethod
    def update(cls, data):
        pass
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pokemons WHERE id = %(id)s;"
        connectToMySQL('pokemon_schema').query_db(query,data)

    @staticmethod
    def validate_pokedex(data):
        is_valid = True
        if int(data['start']) < 1:
            flash("Needs a number greater than 0!")
            is_valid = False
        if int(data['end']) > 898:
            flash('There are "only" 898 Pokemon!')
            is_valid = False
        if int(data['end'])<(int(data['start'])+100):
            flash("Challenge yourself! Needs 100!")
            is_valid = False
        return is_valid