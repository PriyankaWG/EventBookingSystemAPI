from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EventsModel, AccountsModel, PerformersModel
from schemas import AccountSchema, PerformerSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Performer", "performer", description="Operations on performer")


@blp.route("/register/performers/<int:performer_id>")
class PerformerList(MethodView):

    @blp.arguments(PerformerSchema)  
    @blp.response(201,PerformerSchema)
    def post(self, performer_data, performer_id):
        
        performer=AccountsModel.query.get_or_404(performer_id)

        if performer.role==3:
            p=PerformersModel(
            acc_id = performer.id,
            price=performer_data["price"],
            is_booked=performer_data["is_booked"]
            )

            db.session.add(p)
            db.session.commit()
            return performer
        

        
