from flask_app.controllers import pokemon_controller, user_controller

from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)