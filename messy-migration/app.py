from flask import Flask, request, jsonify
from routes.user_routes import bp as user_routes
import sqlite3
import json

app = Flask(__name__)
app.register_blueprint(user_routes)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def home():
    return "User Management System"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)