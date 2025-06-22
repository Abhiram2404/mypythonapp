from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# MySQL connection
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),  # e.g., 'mysql' if using Docker Compose
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    cursorclass=pymysql.cursors.DictCursor
)

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (data['name'], data['email'], hashed_pw))
        conn.commit()
    return jsonify({'message': 'User registered successfully'})

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Login successful', 'user_id': user['id']})
    return jsonify({'error': 'Invalid email or password'}), 401

# Record Blood Donation
@app.route('/donate', methods=['POST'])
def donate():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO donations (user_id, blood_group, quantity) VALUES (%s, %s, %s)",
                       (data['user_id'], data['blood_group'], data['quantity']))
        conn.commit()
    return jsonify({'message': 'Donation recorded'})

# Request Blood
@app.route('/request', methods=['POST'])
def request_blood():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO requests (user_id, blood_group, quantity) VALUES (%s, %s, %s)",
                       (data['user_id'], data['blood_group'], data['quantity']))
        conn.commit()
    return jsonify({'message': 'Blood request submitted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
