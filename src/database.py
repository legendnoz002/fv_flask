import pymongo
from flask import jsonify
class DB():
    URI = 'mongodb://admin:admin123@ds211269.mlab.com:11269/face_vertification?retryWrites=false'
    
    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['face_vertification']
        
    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert(data)
    
    @staticmethod
    def findOne(collection, data):
        return DB.DATABASE[collection].find_one({'username' : data['username']})

    @staticmethod
    def joinEvent(data):
        event = DB.DATABASE['events'].find_one({'secret_key' : data['secret_key']})
        DB.DATABASE['users'].update_one({'username' : data['username']},{'$push' : {'attend' : {'event_id' : event['_id'],'event_name' : event['event_name'],'type' : event['type']}}})
 
    @staticmethod
    def attend(data):
        user = DB.DATABASE['users'].find_one({'username' : data['username']})
        DB.DATABASE['events'].update_one({'secret_key' : data['secret_key']},{'$push' : {'attendees' : {'user_id' : user['_id']}}})
        
        