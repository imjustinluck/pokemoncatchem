from flask.json import jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

@app.route('/login')
def home():
    id = ""
    if 'uuid' in session:
        id = session['uuid']
    return render_template('login.html', id = id)

@app.route('/user/login', methods = ['POST'])
def login():
    if not User.login_validate(request.form):
        return redirect('/login')
    user = User.get_by_email({"email" : request.form["email"]})
    if not user:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['uuid'] = user.id
    session['first_name'] = user.first_name
    return redirect("/welcome")

@app.route('/user/register', methods = ['POST'])
def register():
    if not User.validate_entry(request.form):
        return redirect('/login')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.create(data)
    session['uuid'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/welcome')