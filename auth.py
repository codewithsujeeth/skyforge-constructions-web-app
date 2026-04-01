from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import jwt, datetime, os
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from db import get_db

auth_bp = Blueprint('auth', __name__)

def serialize_user(user):
    return {
        'user_id': str(user['_id']),
        'name': user.get('name', ''),
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        'role': user.get('role', 'user')
    }

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip()
    password = data.get('password', '')
    role = (data.get('role') or 'user').strip().lower()

    if role not in {'user', 'admin'}:
        return jsonify({'error': 'Role must be user or admin'}), 400
    if not name or not email or not phone or not password:
        return jsonify({'error': 'Name, email, phone, and password are required'}), 400

    db = get_db()
    user = {
        'name': name,
        'email': email,
        'phone': phone,
        'password': generate_password_hash(password),
        'role': role,
        'created_at': datetime.datetime.utcnow()
    }

    try:
        result = db.users.insert_one(user)
    except DuplicateKeyError:
        return jsonify({'error': 'Email or phone already registered'}), 409

    user['_id'] = result.inserted_id
    return jsonify({
        'message': 'Account created successfully',
        'user': serialize_user(user)
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    role = (data.get('role') or 'user').strip().lower()
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip()
    password = data.get('password', '')

    if role not in {'user', 'admin'}:
        return jsonify({'error': 'Role must be user or admin'}), 400
    if not password or (not email and not phone):
        return jsonify({'error': 'Email or phone and password are required'}), 400

    db = get_db()
    query = {'role': role}
    if email and phone:
        query['$or'] = [{'email': email}, {'phone': phone}]
    elif email:
        query['email'] = email
    else:
        query['phone'] = phone

    user = db.users.find_one(query)
    if not user or not check_password_hash(user['password'], data.get('password', '')):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({
        'user_id': str(user['_id']),
        'name': user.get('name', ''),
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        'username': user.get('email', '') or user.get('phone', ''),
        'role': user.get('role', 'admin'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, os.environ.get('SECRET_KEY', 'skyforge-secret-key-2024'), algorithm='HS256')
    return jsonify({
        'token': token,
        'user': serialize_user(user)
    })

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.json
    db = get_db()
    # Simple auth check
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'skyforge-secret-key-2024'), algorithms=['HS256'])
        db.users.update_one({'_id': ObjectId(payload['user_id'])}, {'$set': {'password': generate_password_hash(data['new_password'])}})
        return jsonify({'message': 'Password updated'})
    except:
        return jsonify({'error': 'Unauthorized'}), 401

@auth_bp.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    db = get_db()
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
    except Exception:
        return jsonify({'error': 'Invalid user id'}), 400

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user['_id'] = str(user['_id'])
    return jsonify(user)
