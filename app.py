import json
import os
from flask import Flask, jsonify, request
try:
    from flask_cors import CORS
except Exception:
    CORS = None
from ml_model import recommend_style

app = Flask(__name__, static_folder='.', static_url_path='')
if CORS:
    CORS(app)
else:
    @app.after_request
    def _add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

sample_users = [
    {"id": 1, "name": "Lina", "age": 27},
    {"id": 2, "name": "David", "age": 34},
    {"id": 3, "name": "Amina", "age": 22},
    {"id": 4, "name": "Noah", "age": 29},
    {"id": 5, "name": "Zara", "age": 31}
]
custom_users = []
next_id = 1001


def ensure_data_store():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as handle:
            json.dump([], handle, indent=2)


def load_custom_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as handle:
            return json.load(handle)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_custom_users():
    ensure_data_store()
    with open(USERS_FILE, 'w', encoding='utf-8') as handle:
        json.dump(custom_users, handle, indent=2)


ensure_data_store()
custom_users = load_custom_users()
if custom_users:
    next_id = max(user['id'] for user in custom_users) + 1
else:
    next_id = 1001


def find_user(user_id):
    for user in sample_users + custom_users:
        if user["id"] == user_id:
            return user
    return None


@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(sample_users + custom_users)


@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    age = data.get('age')

    if not name or not isinstance(age, int) or age <= 0:
        return jsonify({"error": "Name and age are required."}), 400

    user = {"id": next_id, "name": name, "age": age}
    custom_users.append(user)
    next_id += 1
    save_custom_users()
    return jsonify(user), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    age = data.get('age')

    if not name or not isinstance(age, int) or age <= 0:
        return jsonify({"error": "Name and age are required."}), 400

    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    user['name'] = name
    user['age'] = age
    save_custom_users()
    return jsonify(user)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global custom_users
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    custom_users[:] = [item for item in custom_users if item['id'] != user_id]
    save_custom_users()
    return jsonify({"message": "User deleted."})


@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    age = data.get('age')

    if not name or not isinstance(age, int) or age <= 0:
        return jsonify({"error": "Name and age are required."}), 400

    theme = recommend_style(name, age)
    return jsonify(theme)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(path):
        return app.send_static_file(path)
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
