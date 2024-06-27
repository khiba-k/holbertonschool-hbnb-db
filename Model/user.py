#!/usr/bin/python3
"""Defines class for User entity"""
import bcrypt
from base_model import BaseModel
from Persistance.data_management import DataManager
from datetime import datetime
from create_app_db import db


class User(db.Model):
    """Handles the users information

    Attributes:
        emails []: Has all the existing emails in the system
        user_places []: Has list of the places the user is hosting
        user_details {}: Dictionery containing users information 
    """

    emails = []
    user_places = []
    users = {}

    def __init__(self, firstName, lastName, password, email):
        """Method initializes the User Class instance

        Args:
            firstName (string): users first name
            lastName (string): users last name
            password (string): users password
            email (string): users email
        """

        self.stamps = BaseModel()
        self.user_id = self.stamps.id
        self.firstName = firstName
        self.lastName = lastName
        self.__password = self.hash_password(password)
        self.email = email
        self.created_at = str(self.stamps.created_at)

    def hash_password(self, password):
        """Hashes a password using bcrypt.

        Args:
            password (string): the plain-text password to hash

        Returns:
            string: the hashed password
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def to_dict(self):
        """Creates a dictionary of all users
        """
        
        data = {
            "first_name": self.firstName,
            "last_name": self.lastName,
            "email": self.email,
            "password": self.__password,
            "created_at": self.created_at
        }
        return data
    
    def save_to_file(self):
        """Saves user information to json file
        """
        
        data_manager = DataManager()
        existing_emails = data_manager.get("emails")

        if "@gmail.com" not in self.email:
            raise ValueError("Email has to include '@gmail.com'")
        
        if self.email in existing_emails.values():
            return "Email already exists"
        
        data_manager.save("emails", self.email, None,  self.user_id)
        data_manager.save("users", self.to_dict(), None, self.user_id)

    def user_update(self):
        """Update user information in json file
        """
        data_manager = DataManager()
        data_manager.update("users", self.to_dict(), None, self.user_id)

    def delete_user(self):
        """Deletes user information from json file
        """
        data_management = DataManager()
        email_delete_result = data_management.delete("users", self.user_id)
        user_delete_result = data_management.delete("emails", self.user_id)

        return email_delete_result, user_delete_result

    

