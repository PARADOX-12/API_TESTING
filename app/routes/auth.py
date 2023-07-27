from app_config import jsonify,request,Blueprint,jwt_required,get_jwt_identity,Bcrypt,create_access_token,create_refresh_token
from app.Models.user import Tester
import json

auth = Blueprint('auth' , __name__)
bcrypt = Bcrypt()


@auth.route('/register', methods = ['POST'])
def register():
    try:
        data = request.get_json()
        check_user_exist = Tester.find_by_email(data['email'])
        if not check_user_exist:
            access_token = create_access_token(identity=(data['email'] , data['role']))
            refresh_token = create_refresh_token(identity=(data['email'], data['role']))
            Tester.register()
            return jsonify({
                "Message" : "user added successfully",
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }),200

        return jsonify({
            "Message" : "user already exist"
        }),403


    except Exception as e:
        return jsonify({
            "Error" : "error occured",
            "Message" : str(e)
        })



@auth.route('/login', methods = ['POST'])
@jwt_required()
def login():
    try:
        data = request.get_json()
        check_data = Tester.find_by_email(data['email'])
        if check_data:
            change = json.loads(check_data)
            encrypted_password = bcrypt.check_password_hash(change[0]['password'], data['password'])
            if encrypted_password and change[0]['role'] == data['role'] :
                access_token = create_access_token(identity=(data['email'], data['role']))
                refresh_token = create_refresh_token(identity=(data['email'], data['role']))
                return jsonify({
                    "Message": "Login successfully",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token
                }),200

            return jsonify({
                "Message": "credentails are incorrect"
            }),401

        return jsonify({
            "Message" : "user does not exist "
        }),404


    except Exception as e:
        return  jsonify({
            "message" : "Error occured", "Error" : str(e)
        }),500




@auth.route('/refresh' , methods = ['POST'])
@jwt_required(refresh= True)
def refresh_token():
   try:
       current_user = get_jwt_identity()
       if current_user:
           access_token = create_access_token(identity=current_user)
           return jsonify({
               "access_token": access_token
           }), 200

       return jsonify({
           "Message" : "Invalid credentials"
       }),401

   except Exception as e:
       return jsonify({
           "ERROR" : "error occured",
           "Message" : str(e)
       }),200




@auth.route('/user', methods = ['POST'])
@jwt_required()
def user_add():
    try:
        current_user = get_jwt_identity()
        if current_user[1] == "admin" :
            Tester.add_users()
            return jsonify({
                'Message': 'user Added Successfully'
            }), 200

        return jsonify({
            "Message" : "unauthorised to use this function"
        }),401


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500


