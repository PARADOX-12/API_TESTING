from app_config import jsonify,Blueprint,jwt_required,get_jwt_identity
from app.Models.user import Tester
import json


_id_route = Blueprint('_id', __name__)


@_id_route.route('/user/<_id>', methods = ['PUT'])
@jwt_required()
def update_user(_id):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_id(_id):
            if current_user[1] == "admin" :
                Tester.update_by_id(_id)
                return jsonify({
                    "Message": "user updated successfully"
                }), 200

            return jsonify({
                "Message" : "unauthorised to use this function"
            }), 401

        else:
            return jsonify({
                "Message" : "Did not find user to update by this Id "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500



@_id_route.route('/user/<_id>', methods = ['DELETE'])
@jwt_required()
def delete_User(_id):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_id(_id):
            if current_user[1] == "admin":
                Tester.delete_by_id(_id)
                return jsonify({
                    "Message": "user deleted successfully"
                }), 200

            return jsonify({
                "Message" : "unauthorised to use this function"
            }),401

        else:
            return jsonify({
                "Message": "Cannot find user by this Id "
            }), 404


    except Exception as e :
        return jsonify({
            "Message": "Error occured ", "Error" : str(e)
        }), 500


@_id_route.route('/user/<_id>', methods = ['GET'])
@jwt_required()
def find_user(_id):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_id(_id):
            data = Tester.find_by_id(_id)
            change = json.loads(data)
            updated_array = [{**item, "_id": item["_id"]["$oid"]} for item in change]
            return updated_array, 200

        else:
            return jsonify({
                "Message": "Cannot find users by this Id "
            }),404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500

