from flask import Blueprint , request , jsonify , current_app as app
from src.model.user import User
from src.database import DB
import jwt 

mobile_route = Blueprint('mobile_route', __name__)

def get_blueprint():
    return mobile_route
    
@mobile_route.route('/ping')
def index():
    msg = {"message" : "bong"}
    return jsonify(msg),200



@mobile_route.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    

    msg = ""

    if not req_data['username'] or not req_data['password']:
        msg = {"status" : {"type" : "failure", "message" : "somethings is wrong"}}
        return jsonify(msg),200
    
    user = User(req_data['username'],req_data['password'],None)

    

    if user.check_username() : 
        if user.check_password(req_data['password']) :
            token_data = {
                'username' : user.username,
                'admin' : user.admin
            }

            token = jwt.encode(token_data,app.config['SECRET_KEY'])
           
            return jsonify({'token' : token.decode('UTF-8')}),200
        else :
            msg = {"status" : {"type" : "failure", "message" : "wrong password"}}
            return jsonify(msg),200
    else :
        msg = {"status" : {"type" : "failure", "message" : "user not found"}}
        return jsonify(msg),200
  





@mobile_route.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    admin = False

    msg = ""

    if not username or not password:
        msg = {"status" : {"type" : "failure", "message" : "somethings is wrong"}}
        return jsonify(msg),200

    user = User(username=username,password=password,admin=admin)

    found = user.check_username()

    if not found : 
        msg = {"status" : {"type" : "success", "message" : "username available"}}
        user.set_password(password)
        user.insert()
        return jsonify(msg), 200
    else :
        msg = {"status" : {"type" : "failure", "message" : "user already exist"}}
        return jsonify(msg), 200

