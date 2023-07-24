from mongoengine import Document, StringField,Q,EmailField
from flask import request,json,jsonify
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,create_access_token,get_jwt_identity,jwt_required

bcrypt = Bcrypt()

class Tester(Document):
    _id = StringField()
    name = StringField(min_length= 3, max_length=20)
    email = EmailField(required=True, min_length= 3, max_length= 20)
    password = StringField(required= True, min_length= 3, max_length=100)


    def to_json(self):
        {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }


    @classmethod
    def add_users(cls):
        user = request.get_json()
        if user:
            hashed_password = bcrypt.generate_password_hash(user['password']).decode('utf-8')
            data = Tester(
                name = user['name'],
                email = user['email'],
                password = hashed_password
            )
            data.save()

        return None



    @classmethod
    def find_by_email(cls, email):
        find = cls.objects(email__contains=email)
        if find:
            find_data = json.dumps(find)
            return find_data

        return None



    @classmethod
    def find_by_id(cls,_id):
        find_id = ObjectId(_id)
        data = cls.objects(Q(_id=find_id))
        if data:
            return json.dumps(data)

        return None



    @classmethod
    def delete_by_id(cls, _id):
        find_id = ObjectId(_id)
        data = cls.objects(Q(_id=find_id))
        if data:
            data.delete()

        return None


    @classmethod
    def update_by_id(cls, _id):
        find_id = ObjectId(_id)
        data = cls.objects(Q(_id=find_id))
        if data:
            body = request.get_json()
            if 'password' in body:
                hashed_password = bcrypt.generate_password_hash(body['password']).decode('utf-8')
                body['password'] = hashed_password

            data.update(**body)
            
        return None


    @classmethod
    def register(cls):
        data = request.get_json()
        if data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            body = Tester(
                email = data['email'],
                password = hashed_password
            )

            body.save()

        return None


    @classmethod
    def find_by_name(cls,name):
        find_name = cls.objects(name__contains = name)
        if find_name:
            data = json.dumps(find_name)
            return data
        
        return None

    

    @classmethod
    def update_by_name(cls,name):
        data = cls.objects(name__contains=name)
        if data:
            body = request.get_json()
            if 'password' in body:
                hashed_password = bcrypt.generate_password_hash(body['password']).decode('utf-8')
                body['password'] = hashed_password

            data.update(**body)

        return None



    @classmethod
    def delete_by_name(cls, name):
        data =  cls.objects(name__contains = name)
        if data:
            data.delete()

        return None



    @classmethod
    def update_by_email(cls,email):
        data = cls.objects(email__contains = email)
        if data:
            body = request.get_json()
            if 'password' in body:
                hashed_password = bcrypt.generate_password_hash(body['password']).decode('utf-8')
                body['password'] = hashed_password

            data.update(**body)
            
        return data
    
    
    
    @classmethod
    def delete_by_email(cls,email):
        data = cls.objects(email__contains = email)
        if data:
            data.delete()
            
        return None


