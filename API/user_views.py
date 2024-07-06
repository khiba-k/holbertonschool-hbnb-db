#!/usr/bin/python3
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_current_user, jwt_required, set_access_cookies, unset_jwt_cookies,create_access_token
import sys
import os
import bcrypt

# Get the directory containing this script
current_dir = os.path.dirname(__file__)

# Construct the path to the Model directory
model_path = os.path.join(current_dir, '..', 'Model')

# Add Model directory to sys.path
sys.path.append(model_path)

from Model.user import User
from Persistance.data_management import DataManager
from create_app_db import db


def user_login(data):
    email = data.get('email')
    password =  data.get('password')

    #Using SQLAlchemy

    user = db.session.query(User).filter_by(email=email).first()

    if user:

        if  bcrypt.checkpw(password.encode('utf-8'), user._password.encode('utf-8')):
            admin = user.is_admin
            role_dict = {
            'roles': ['admin'] if admin else ['user']}
            access_token = create_access_token(identity=user.user_id, additional_claims=role_dict)
            response = jsonify({"message": "Login successful"}, access_token)
            set_access_cookies(response, access_token)
            return response, 200
        return "Invalid Password"
    return "Invalid Email", 401
        
    #Using JSON File

    # data_manager = DataManager()
    # all_emails = data_manager.get("emails")
    # user_id = next((key for key, value in all_emails.items() if value == email), None)

    # if user_id:
    #     specific_user = data_manager.get("users", user_id)
    #     get_pass = specific_user.get("password")

    #     if  bcrypt.checkpw(password.encode('utf-8'), get_pass):
    #         access_token = create_access_token(identity=user_id)
    #         response = jsonify({"message": "Login successful"})
    #         set_access_cookies(response, access_token)
    #         return response, 200
    # return "Invalid Login", 401 #Redirect to create user




def create_user(data):
    """Create new user
    """
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    email = data.get('email')
    
    new_user = User(first_name, last_name, password, email)
    result = new_user.save_to_file()
    new_user.save_to_db()

    if result == "Email already exists":
        return jsonify({"error": "Email already exists"}), 400
    return jsonify(new_user.to_dict()), 201

def get_all_users():
    """Retrieve all existing users"""
    data_manager = DataManager()
    users_data = data_manager.get("users")

    if users_data:
        return jsonify(users_data), 200
    else:
        return jsonify({"message": "No users found"}), 404
    

def get_specific_user(user_id):
    """Get one place and return it"""
    data_manager = DataManager()
    user_data = data_manager.get("users", user_id)

    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404

def update_user(user_id, data):
    data = data
    data_manager = DataManager()
    
    existing_user = data_manager.get("users", user_id)
    if not existing_user:
        return jsonify({"message": "User not found"}), 404

     
    updated_user = User(
        firstName=data.get('first_name', existing_user['first_name']),
        lastName=data.get('last_name', existing_user['last_name']),
        password=data.get('password', existing_user['password']),
        email=data.get('email', existing_user['email'])
    )
    updated_user.user_id = user_id
    updated_user.user_update()
    
    return jsonify(updated_user.to_dict()), 200

def delete_user(user_id):
    """Delete Data from JSON file"""
    data_manager = DataManager()
    result = data_manager.delete("users", user_id)
    data_manager.delete("emails", user_id)
    
    if result == "something went wrong":
        return jsonify({"message": "User not found"}), 404
<<<<<<< HEAD
    return jsonify({"message": "User deleted successfully"}), 200
=======
    return jsonify({"message": "User deleted successfully"}), 200

def login():
    # authenticate user
    additional_claims= {"is_admin": user.is_admin}
    access_token = create_access_token(identify=user.id, additional_claims=additional_claims)
    return jsonify(access_token=access_token)
>>>>>>> main
