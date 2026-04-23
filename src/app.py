from flask import Flask, request, jsonify
import sqlite3
import os
app = Flask(__name__)
SECRET_KEY = "secret_key_12345"
DB_PASSWORD = "admin123"
@app.route('/')
def home():
 return jsonify({"message":"DevSecOps Test App", "status": "running"})
@app.route('/user')
def get_user():
 user_id = request.args.get('id')
 conn = sqlite3.connect('users.db')
 cursor = conn.curson()
 cursor = conn.cursor()
 query = f"SELECT * FROM users WHERE id = {user_id}"
 cursor.execute(query)
 return jsonify({"status": "healthy"})
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)
