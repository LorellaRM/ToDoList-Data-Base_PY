"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
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

@app.route('/todo/user/<username>', methods=['GET'])
def get_all_todos(username):
    user = User.query.filter_by(username = username).first()
    todos = Todo.query.filter_by(user_id = user.id).all()
    return jsonify({
        'data': [todo.serialize() for todo in todos]
    }), 200

@app.route('/todo/user/<username>', methods=['POST'])
def new_user(username):
    # body = request.get_json()
    new_user = User(username = username)
    new_user.add_new_user()
    return "Username created", 201

@app.route('/todo/user/<username>/task', methods=['POST'])
def post_new_todos(username):
    body = request.get_json()
    print(body)
    if body is None:
        return "The request body is null", 400

    user = User.query.filter_by(username = username).first()
    new_todo = Todo(user_id = username, label = body["label"], done = body["done"])
    new_todo.add_todo()

    return "Todo Added", 200

@app.route('/todo/user/<username>/task/<int:id>', methods=['PUT'])
def update_todos(username, id):
    body = request.get_json()
    print(body)
    if body is None:
        return "The request body is null", 400

    Todo.update_todo(id, body)

    return "Todo Added", 200

@app.route('/todo/user/<username>', methods=['DELETE'])
def delete_user(username):
    user_to_delete = User.query.filter_by(username = username).first()
    user_to_delete.delete()

    return "User deleted, see you soon", 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
