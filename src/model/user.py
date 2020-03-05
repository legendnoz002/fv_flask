import datetime
from src.database import DB
from flask import jsonify

from werkzeug.security import generate_password_hash, check_password_hash
class User(object):
        
    def __init__(self,username,password,admin,firstname,lastname):
        self.username = username
        self.password = password
        self.admin = admin
        self.firstname = firstname
        self.lastname = lastname

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_username(self):
        user = DB.findOne(collection='users', data=self.json())
        if user :
            self.password = user['password']
            self.admin = user['admin']
            return True
        else : 
            return False
    
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    def insert(self):
        DB.insert(collection='users', data=self.json())
    
    def get_event(self):
        user = DB.findOne(collection='users', data=self.json())
        if user :
            return user


    def json(self):
        return {
            'username' : self.username,
            'password' : self.password,
            'admin' : self.admin,
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'attend' : []
        }