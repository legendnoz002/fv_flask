from flask import Blueprint , request , jsonify , current_app as app



admin_route = Blueprint('admin_route',__name__)

def get_blueprint():
    return admin_route

@admin_route.route('/ping')
def index():
    return 'admin pong'