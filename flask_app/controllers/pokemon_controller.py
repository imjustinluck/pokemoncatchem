from flask import render_template, request, session, redirect, jsonify
from flask_app.models.pokemon import Pokemon
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    id = ""
    if 'uuid' in session:
        id = session['uuid']
    return render_template("index.html", id = id)

@app.route('/start', methods=['POST'])
def start():
    if not Pokemon.validate_pokedex(request.form):
        return redirect('/')
    session['start']=int(request.form['start'])
    session['end']=int(request.form['end'])
    return redirect('/game')

@app.route('/game')
def game():
    id = ""
    if 'uuid' in session:
        id = session['uuid']
    if 'start' not in session:
        return redirect('/welcome')
    return render_template("game.html", id = id)

@app.route('/pokemon/create', methods=['POST'])
def create_pokemon():
    data = {}
    if 'uuid' in session:
        data = {
            "user_id":session['uuid'],
            "pokedex":request.form["pokedex"],
            "name":request.form["name"].capitalize(),
            "isShiny":request.form["isShiny"],
            "img":request.form["img"],
            "type":request.form["type"],
            "ability":request.form["ability"]
        }
    else:
        data = {
            "user_id":1,
            "pokedex":request.form["pokedex"],
            "name":request.form["name"].capitalize(),
            "isShiny":request.form["isShiny"],
            "img":request.form["img"],
            "type":request.form["type"],
            "ability":request.form["ability"]
        }
    Pokemon.create(data)
    return jsonify(message = "Pokemon Caught!")

@app.route('/pokemon/recent')
def recent_pokemon():
    default_id = 1
    if 'uuid' in session:
        default_id = session['uuid']
    return jsonify(Pokemon.get_four({'user_id':default_id}))

@app.route('/pokemon/rivals')
def rivals():
    return jsonify(Pokemon.get_seven())

@app.route('/pokemon/view', methods=["POST"])
def view():
    return jsonify(Pokemon.get_one(request.form))

@app.route('/pokemon/friend/<int:id>')
def friend(id):
    data = {
        'pokemon_id': id,
        'user_id': session['uuid']
    }
    User.friend(data)
    return redirect('/game')

@app.route('/pokemon/setfree/<int:id>')
def free(id):
    Pokemon.delete({'id':id})
    return redirect('/game')

@app.route('/reset')
def reset():
    if (session):
        session.clear()
    return redirect('/welcome')