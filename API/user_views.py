#!/usr/bin/python3
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_current_user, jwt_required
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


def user_login(data):
    email = data.get('email')
    password =  data.get('password')

    data_manager = DataManager()
    all_emails = data_manager.get("emails")
    user_id = next((key for key, value in all_emails.items() if value == email), None)

    if user_id:
        specific_user = data_manager.get("users", user_id)
        get_pass = specific_user.get("password")

        if  bcrypt.checkpw(password.encode('utf-8'), get_pass):
            access_token = create_access_token(user_id)
            return jsonify(access_token=access_token)
        return "Invalid Password"
    return "Email Does Not Exist" #Redirect to create user




def create_user(data):
    """Create new user
    """
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    email = data.get('email')
    
    new_user = User(first_name, last_name, password, email)
    result = new_user.save_to_file()

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
    return jsonify({"message": "User deleted successfully"}), 200

