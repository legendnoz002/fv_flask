import os
from flask import Flask 
from flask_cors import CORS
from src.database import DB
from src.routes import mobile_route
from src.routes import admin_route
project_root = os.path.dirname(__file__)

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SECRET_KEY'] = 'shambala'

DB.init()

app.debug = True

app.register_blueprint(mobile_route.get_blueprint(), url_prefix="/mobile")
app.register_blueprint(admin_route.get_blueprint(), url_prefix="/admin")

if __name__ == "__main__":
   app.run()