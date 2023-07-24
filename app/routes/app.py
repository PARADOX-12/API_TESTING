import json
from flask import Flask,jsonify,request
from flask_mongoengine import MongoEngine
from app.Models.user import Tester
from flask_jwt_extended import JWTManager,create_access_token, jwt_required
from flask_bcrypt import Bcrypt
import datetime


bcrypt = Bcrypt()

app = Flask(__name__)
JWTManager(app)
app.config['JWT_SECRET_KEY'] = '01b8e17d4cccabb880dc07708f0e6673'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


try:
    app.config['MONGODB_SETTINGS'] = {
       'host' : 'mongodb://localhost/API_TESTING'
    }

    db = MongoEngine()
    db.init_app(app)

    print("DataBase Connected Successfully")

except Exception as e  :
    print("Error occure while connecting", e)



@app.route('/user', methods = ['POST'])
@jwt_required()
def user_add():
    try:
        Tester.add_users()
        return jsonify({
            'Message': 'user Added Successfully'
        }), 200


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500




@app.route('/user/<_id>', methods = ['GET'])
@jwt_required()
def find_user(_id):
    try:
        if Tester.find_by_id(_id):
            data = Tester.find_by_id(_id)
            change = json.loads(data)
            updated_array = [{**item, "_id": item["_id"]["$oid"]} for item in change]
            return updated_array,200

        else:
            return jsonify({
                "Message": "Cannot find users by this Id "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500




@app.route('/user/<_id>', methods = ['PUT'])
@jwt_required()
def update_user(_id):
    try:
        if Tester.find_by_id(_id):
            Tester.update_by_id(_id)
            return jsonify({
                "Message": "user updated successfully"
            }), 200

        else:
            return jsonify({
                "Message" : "Did not find user to update by this Id "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500




@app.route('/user/<_id>', methods = ['DELETE'])
@jwt_required()
def delete_User(_id):
    try:
        if Tester.find_by_id(_id):
            Tester.delete_by_id(_id)
            return jsonify({
                "Message": "user deleted successfully"
            }), 200

        else:
            return jsonify({
                "Message": "Cannot find user by this Id "
            }), 404


    except Exception as e :
        return jsonify({
            "Message": "Error occured ", "Error" : str(e)
        }), 500



@app.route('/register', methods = ['POST'])
def register():
    try:
        data = request.get_json()
        check_user_exist = Tester.find_by_email(data['email'])
        if not check_user_exist:
            access_token = create_access_token(identity=data['email'])
            Tester.register()
            return jsonify({
                "Message" : "user added successfully",
                "access_token" : access_token
            }),200

        return jsonify({
            "Message" : "user already exist"
        }),403

    except Exception as e:
        return jsonify({
            "Error" : "error occured",
            "Message" : str(e)
        })




@app.route('/login', methods = ['POST'])
def login():
    try:
        data = request.get_json()
        check_data = Tester.find_by_email(data['email'])
        if check_data:
            change = json.loads(check_data)
            encrypted_password = bcrypt.check_password_hash(change[0]['password'], data['password'])
            if encrypted_password:
                access_token = create_access_token(identity=data['email'])
                return jsonify({
                    "Message": "Login successfully",
                    "access_token" : access_token
                }),200

            return jsonify({
                "Message": "The Email or Password is incorrect"
            }),401

        return jsonify({
            "Message" : "user does not exist "
        }),404


    except Exception as e:
        return  jsonify({
            "message" : "Error occured", "Error" : str(e)
        }),500




@app.route('/api/testing/<name>', methods = ['GET'])
@jwt_required()
def find_name(name):
    try:
        data = Tester.find_by_name(name)
        if data:
            change = json.loads(data)
            updated_array = [{**item, "_id": item["_id"]["$oid"]} for item in change]
            return updated_array, 200

        return jsonify({
            "Message": "Cannot find user by this name"
        }), 404


    except Exception as e:
        return jsonify({
            "ERROR" : "error occured",
            "Message" : str(e)
        })




@app.route('/api/testing/<name>', methods = ['PUT'])
@jwt_required()
def update_by_name(name):
    try:
        data = Tester.find_by_name(name)
        if data:
            Tester.update_by_name(name)
            return jsonify({
                "Message": "user updated successfully"
            }), 200

        else:
            return jsonify({
                "Message" : "Did not find user to update by this name "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500




@app.route('/api/testing/<name>', methods = ['DELETE'])
@jwt_required()
def delete_by_name(name):
    try:
        if Tester.find_by_name(name):
            Tester.delete_by_name(name)
            return jsonify({
                "Message": "user deleted successfully"
            }), 200

        else:
            return jsonify({
                "Message": "Cannot find user by this name "
            }), 404


    except Exception as e :
        return jsonify({
            "Message": "Error occured ", "Error" : str(e)
        }), 500




@app.route('/api/testing/by_email/<email>', methods = ['GET'])
@jwt_required()
def get_user(email):
    try:
        if Tester.find_by_email(email):
            data = Tester.find_by_email(email)
            change = json.loads(data)
            updated_array = [{**item, "_id": item["_id"]["$oid"]} for item in change]
            return updated_array, 200

            return jsonify({
                'Message' : "unauthorized"
            }),401

        else:
            return jsonify({
                "Message" : "Did not find user to by this email "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500



@app.route('/api/testing/update_by_email/<email>', methods = ['PUT'])
@jwt_required()
def update_by_email(email):
    try:
        if Tester.find_by_email(email):
            Tester.update_by_email(email)
            return jsonify({
                "Message": "user updated successfully"
            }), 200

        return jsonify({
            "Message": "cannot update user by this email"
        }), 404

    except Exception as e:
        return jsonify({
            "ERROR" : "error occured",
            "Message" : str(e)
        })



@app.route('/api/testing/delete_by_email/<email>', methods = ['DELETE'])
@jwt_required()
def delete_by_email(email):
    try:
        if Tester.find_by_email(email):
            Tester.delete_by_email(email)
            return jsonify({
                "Message": "user deleted successfully"
            }), 200

        else:
            return jsonify({
                "Message": "Cannot find user by this email "
            }), 404


    except Exception as e :
        return jsonify({
            "Message": "Error occured ", "Error" : str(e)
        }), 500




if __name__ == '__main__':
    app.run(debug=True)