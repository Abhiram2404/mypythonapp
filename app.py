from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import bcrypt
import os
from dotenv import load_dotenv
import boto3
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (data['name'], data['email'], hashed_pw))
        conn.commit()
    return jsonify({'message': 'User registered'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Login successful', 'user_id': user['id']})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/donate', methods=['POST'])
def donate():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO donations (user_id, blood_group, quantity) VALUES (%s, %s, %s)",
                       (data['user_id'], data['blood_group'], data['quantity']))
        conn.commit()
    return jsonify({'message': 'Donation recorded'})

@app.route('/request', methods=['POST'])
def request_blood():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO requests (user_id, blood_group, quantity) VALUES (%s, %s, %s)",
                       (data['user_id'], data['blood_group'], data['quantity']))
        conn.commit()
    return jsonify({'message': 'Blood request recorded'})

if __name__ == '__main__':
    app.run(debug=True)
