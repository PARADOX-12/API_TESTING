from app_config import jsonify,request,Blueprint,jwt_required,get_jwt_identity,create_access_token,create_refresh_token
from app.Models.user import Tester
import json


name_route = Blueprint('name' , __name__)


@name_route.route('/api/testing/<name>', methods = ['GET'])
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



@name_route.route('/api/testing/<name>', methods = ['PUT'])
@jwt_required()
def update_by_name(name):
    try:
        current_user = get_jwt_identity()
        data = Tester.find_by_name(name)
        if data:
            if current_user[1] == "admin" :
                Tester.update_by_name(name)
                return jsonify({
                    "Message": "user updated successfully"
                }), 200

            return jsonify({
                "Message" : "unauthorised to use this function"
            }),401

        else:
            return jsonify({
                "Message" : "Did not find user to update by this name "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500



@name_route.route('/api/testing/<name>', methods = ['DELETE'])
@jwt_required()
def delete_by_name(name):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_name(name):
            if current_user[1] == "admin" :
                Tester.delete_by_name(name)
                return jsonify({
                    "Message": "user deleted successfully"
                }), 200


            return jsonify({
                'Message': "unauthorized to use this function"
            }), 401

        else:
            return jsonify({
                "Message": "Cannot find user by this name "
            }), 404


    except Exception as e :
        return jsonify({
            "Message": "Error occured ", "Error" : str(e)
        }), 500


