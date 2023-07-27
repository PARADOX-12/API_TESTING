from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import JWTManager,get_jwt_identity,jwt_required,create_access_token,create_refresh_token
from app.utils.database import connect_db
from app.routes.operation_by_id import _id_route
from app.routes.operation_by_name import name_route
from app.routes.operation_by_email import email_route
from flask_bcrypt import Bcrypt
from app.routes.auth import auth
import config


app = Flask(__name__)
connect_db(app)
JWTManager(app)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRETE_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN'] = config.JWT_REFRESH_TOKEN
app.register_blueprint(auth)
app.register_blueprint(email_route)
app.register_blueprint(name_route)
app.register_blueprint(_id_route)
