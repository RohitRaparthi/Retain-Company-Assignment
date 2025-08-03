from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.auth import hash_password, verify_password
import sqlite3

bp = Blueprint('user_routes', __name__)
DATABASE = 'users.db'

@bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]})
    else:
        return jsonify({"error": "User not found"}), 404  # <<--- important


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    finally:
        cursor.close()
        conn.close()



@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name, email = data.get('name'), data.get('email')

    if not (name and email):
        return "Missing fields", 400

    conn = get_db_connection()
    conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated"})



@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"})


@bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return "Please provide a name", 400

    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',)).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if user and verify_password(password, user['password']):
        return jsonify({"status": "success", "user_id": user['id']})
    return jsonify({"status": "failed"}), 401