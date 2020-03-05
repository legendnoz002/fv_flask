import os
from flask import Flask , jsonify
from flask_cors import CORS
from src.database import DB
from src.routes import mobile_route

UPLOAD_FOLDER = r'C:\Users\ACER_NEW\Desktop\FLASK_SERVER\src\images'
SECRET_KEY = 'shambala'


project_root = os.path.dirname(__file__)

app = Flask(__name__)


CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB.init()

app.debug = True

app.register_blueprint(mobile_route.get_blueprint(), url_prefix="/mobile")

@app.route('/')
def bing():
       return jsonify({ "msg" : "bong"}),200


if __name__ == "__main__":
   app.run()