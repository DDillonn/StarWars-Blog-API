"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_adminp
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_all_user():
    user_query = User.query.all()
    all_user = list(map(lambda user: user.serialize(), user_query))
    return jsonify(all_user), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    people_query = People.query.all()
    all_people = list(map(lambda people: people.serialize(), people_query))
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people = People.query.get(people_id)
    return jsonify(people.serialize()), 200

@app.route('/people', methods=['POST'])
def add_new_people():
    request_body = request.data
    dictionary = json.loads(request_body)
    people.append(dictionary)
    print("Incoming request with the following body", dictionary)
    return flask.jsonify(people)

@app.route('/people/<int:position>', methods=['DELETE'])
def delete_people(position):
    print("This is the position to delete: ",position)
    people.pop(position)
    return flask.jsonify(people)


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets_query = Planets.query.all()
    all_planets = list(map(lambda planets: planets.serialize(), planets_query))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets(planets_id):
    planets = Planets.query.get(planets_id)
    return jsonify(planets.serialize()), 200

@app.route('/planets', methods=['POST'])
def add_new_planets():
    request_body = request.data
    dictionary = json.loads(request_body)
    planets.append(dictionary)
    print("Incoming request with the following body", dictionary)
    return flask.jsonify(planets)

@app.route('/planets/<int:position>', methods=['DELETE'])
def delete_planets(position):
    print("This is the position to delete: ",position)
    planets.pop(position)
    return flask.jsonify(planets)


@app.route('/user/favorites', methods=['GET'])
def get_all_favorites():
    favorites_query = Favorites.query.all()
    all_favorites = list(map(lambda favorites: favorites.serialize(), favorites_query))
    return jsonify(all_favorites), 200

@app.route('/user/favorites/<int:favorites_id>', methods=['GET'])
def get_favorites(favorites_id):
    favorites = Favorites.query.get(favorites)
    return jsonify(favorites.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
