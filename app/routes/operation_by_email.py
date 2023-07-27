from app_config import jsonify,request,Blueprint,jwt_required,get_jwt_identity,create_access_token,create_refresh_token
from app.Models.user import Tester
import json


email_route = Blueprint('routes', __name__)


@email_route.route('/api/testing/by_email/<email>', methods = ['GET'])
@jwt_required()
def get_user(email):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_email(email) :
            data = Tester.find_by_email(email)
            change = json.loads(data)
            updated_array = [{**item, "_id": item["_id"]["$oid"]} for item in change]
            return updated_array, 200


        else:
            return jsonify({
                "Message": "Did not find user to by this email "
            }), 404


    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500



@email_route.route('/api/testing/update_by_email/<email>', methods = ['PUT'])
@jwt_required()
def update_by_email(email):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_email(email):
            if current_user[1] == "admin" :
                Tester.update_by_email(email)
                return jsonify({
                    "Message": "user updated successfully"
                }), 200

            return jsonify({
                "Message" : "unauthorized to use this function "
            })

        return jsonify({
            "Message": "cannot update user by this email"
        }), 404

    except Exception as e:
        return jsonify({
            "ERROR" : "error occured",
            "Message" : str(e)
        })



@email_route.route('/api/testing/delete_by_email/<email>', methods = ['DELETE'])
@jwt_required()
def delete_by_email(email):
    try:
        current_user = get_jwt_identity()
        if Tester.find_by_email(email):
            if current_user[1] == "admin":
                Tester.delete_by_email(email)
                return jsonify({
                    "Message": "user deleted successfully"
                }), 200

            return jsonify({
                "Message" : "unauthorized to use this function"
            }),401


        else:
            return jsonify({
                "Message": "Cannot find user by this email "
            }), 404


    except Exception as e :
        return jsonify({
            "Message": "Error occured ", "Error" : str(e)
        }), 500


