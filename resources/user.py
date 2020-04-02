from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('email',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('role',type=str,required=True,help="This field cannot be blank.")
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'],data['email'],data['role'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):

    def get(self, user_id):
        #check if is_admin exist if not discontinue function
        claims = get_jwt_claims()         
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User Not Found'}, 404

        # hard coded return as .json() is not compatiable with user model and sqlalchemy
        return {'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'role': user.role}, 200
        

    @jwt_required
    def delete(self, user_id):
        #check if is_admin exists - if not discontinue function
        claims = get_jwt_claims()         
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message", "Unable to delete User"}, 404 
        user.delete_from_db()
        return {"Message": "User deleted"}, 200

#pull all users - for debugging purposes disable before production
class Users(Resource):
    @jwt_required
    def get(self):
        #check if is_admin exists - if not discontinue function
        claims = get_jwt_claims() 
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

        return {'Users': [user.json() for user in UserModel.query.all()]}

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True) 
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401       