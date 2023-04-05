from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from db import db
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from models import AccountsModel
from schemas import AccountSchema
from blocklist import BLOCKLIST

blp = Blueprint("Accounts", "accounts", description="Operations on accounts")


@blp.route("/register")
class AccountRegister(MethodView):
   
    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, user_data):
        if AccountsModel.query.filter(AccountsModel.username == user_data["username"]).first():
            abort(400, message="Username already exists")

        user = AccountsModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            role=user_data["role"]
        )
        
       
        db.session.add(user)
        db.session.commit()
        
    
        return user
    


@blp.route("/login")
class UserLogin(MethodView):

    
    @blp.arguments(AccountSchema)
    @blp.response(200, AccountSchema)
    def post(self, user_data):
        user = AccountsModel.query.filter(
            AccountsModel.username == user_data["username"]
        ).first()



        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # access_token = create_access_token(identity=user.id, fresh=True)
            # refresh_token = create_refresh_token(user.id)
            # return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return user

        abort(401, message="Invalid credentials.")


# @blp.route("/refresh")
# class TokenRefresh(MethodView):
#     @jwt_required(refresh=True)
#     def post(self):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         jti = get_jwt()["jti"]
#         BLOCKLIST.add(jti) #Refresh token can only be used once
#         return {"access_token": new_token}

# @blp.route("/logout")
# class UserLogout(MethodView):
#     @jwt_required()
#     def post(self):
#         jti=get_jwt()["jti"]
#         BLOCKLIST.add(jti)
#         return ("message"== "Successfully logged out")
