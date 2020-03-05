from flask import Blueprint , request , jsonify , current_app as app
from src.model.user import User
from src.database import DB
import jwt 
import os, os.path
import face_recognition
from werkzeug.utils import secure_filename
from src.database import DB

mobile_route = Blueprint('mobile_route', __name__)


ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}


def get_blueprint():
    return mobile_route

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mobile_route.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    
    msg = ""

    if not req_data['username'] or not req_data['password']:
        msg = {"status" : {"type" : "failure", "message" : "somethings is wrong"}}
        return jsonify(msg),200
    
    user = User(req_data['username'],req_data['password'],None,None,None)

    

    if user.check_username() : 
        if user.check_password(req_data['password']) :
            token_data = {
                'username' : user.username,
                'admin' : user.admin
            }

            token = jwt.encode(token_data,app.config['SECRET_KEY'])
           
            return jsonify({'token' : token.decode('UTF-8'),"username" : user.username, "status" : {"type" : "success"}}),200
        else :
            msg = {"status" : {"type" : "failure", "message" : "wrong password"}}
            return jsonify(msg),200
    else :
        msg = {"status" : {"type" : "failure", "message" : "user not found"}}
        return jsonify(msg),200
  





@mobile_route.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    ext = request.form.get('ext')
    admin = False

    msg = ""

    if not username or not password:
        msg = {"status" : {"type" : "failure", "message" : "somethings is wrong"}}
        return jsonify(msg),201

    if 'file' not in request.files:
        msg = {"status" : {"type" : "failure", "message" : "no file part"}}
        return jsonify(msg),201

    user = User(username=username,password=password,admin=admin,firstname=firstname,lastname=lastname)
    file = request.files['file']

    if file.filename == '':
        return jsonify({"msg" : "no file selected"}),201

    found = user.check_username()

    if not found :  
        os.chdir(app.config['UPLOAD_FOLDER'])
        msg = {"status" : {"type" : "success", "message" : "username available"}}
        user.set_password(password)
        user.insert()
        try:
            os.mkdir("{foldername}".format(foldername = username))
        except OSError:
            print("fail")

        if file and allowed_file(file.filename):
            _dir = os.path.join(app.config['UPLOAD_FOLDER'],"{foldername}".format(foldername = username))
            file_count = len(os.listdir(_dir)) + 1

            filename = "{0}_{1}.{2}".format(username, file_count, ext)
            file.save(os.path.join(_dir, filename))
        
        return jsonify(msg), 200
    else :
        msg = {"status" : {"type" : "failure", "message" : "user already exist"}}
        return jsonify(msg), 404




@mobile_route.route('/get_event', methods=['POST'])
def get_event():
    event = []
    req_data = request.get_json()
    response = DB.findOne(collection='users', data=req_data)
    if response == None:
        return jsonify({"msg" : "no record"}),201

    for document in response["attend"]:
        document['event_id'] = str(document['event_id'])
        document['event_name'] = document['event_name']
        document['type'] = document['type']
        event.append(document)
    return jsonify(event),200

@mobile_route.route('/join_event', methods=['POST'])
def join_events():
    req_data = request.get_json()
    # { 
    #     "secret_key" : "QR123",
    #     "username" : "test12345"
    # }
    DB.joinEvent(data=req_data)
    DB.attend(data=req_data)
    return jsonify({"msg" : "xd"}),200

    



@mobile_route.route('/compare', methods=['POST'])
def test():
    if 'file' not in request.files:
        msg = {"status" : {"type" : "failure", "message" : "no file part"}}
        return jsonify(msg),201

    file = request.files['file']
    username = request.form.get('username')

    path = "./src/images/{0}/{0}_1.jpeg".format(username)

    if file.filename == '':
        return jsonify({"msg" : "no file selected"}),201
    
    if file and allowed_file(file.filename):
        test_pic = face_recognition.load_image_file(file)
        face_encoding = face_recognition.face_encodings(test_pic)[0]
        unknown_pic = face_recognition.load_image_file(path)
        unknown_pic_encoding = face_recognition.face_encodings(unknown_pic)[0]
        results = face_recognition.compare_faces([face_encoding], unknown_pic_encoding)
        if results[0] == True:
            print("SUCCESSSSS")
            return jsonify({ "msg" : "matched"}),200
        else:
            print("FAIL")
            return jsonify({ "msg" : "not matched"}),201

   





