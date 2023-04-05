from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import  AccountsModel, VenuesModel
from schemas import  VenueSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Venues", "venue", description="Operations on venue")



@blp.route("/organisers/<string:organiser_id>/venues")
class VenueList(MethodView):

    @blp.response(200,VenueSchema(many=True))
    def get(self,organiser_id):
        organiser = AccountsModel.query.get_or_404(organiser_id)
        return organiser.venues.all()
    

    @blp.arguments(VenueSchema)  
    @blp.response(201,VenueSchema)
    def post(self, venue_data,organiser_id):
   
        # if VenuesModel.query.filter(
        #     VenuesModel.organiser_id == organiser_id, 
        #     VenuesModel.name == venue_data["name"]) .first():
        #     abort(400, message="Same venue already exists.")



        venue = VenuesModel(**venue_data, organiser_id = organiser_id)
        organiser = AccountsModel.query.get_or_404(organiser_id)

        if(organiser.role != 1):
            abort(401,
                message="This ID is not an organiser")

        try:
            db.session.add(venue)
            db.session.commit()
            organiser.venues.append(venue)

        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return venue



# @blp.route("/organisers/<string:organiser_id>/venues/<string:venue_id>")
# class VenueList(MethodView):

#     @blp.response(200, VenueSchema)
#     def get(self,organiser_id,venue_id):

#         venue = VenuesModel.query.get_or_404(venue_id)
#         print (venue.organiser_id)
#         print (organiser_id)

#         if venue.organiser_id != organiser_id:
#             abort(400, message=f"Venue {venue_id} is not under organiser {organiser_id}.")

#         return venue
    
    # @blp.response(202)
    # def delete(self, organiser_id, venue_id,):
    #     venue = VenuesModel.query.get_or_404(venue_id)

    #     if not (venue.organiser_id == organiser_id):
    #         abort(400, message=f"Venue {venue_id} is not under organiser {organiser_id} .")

    #     organiser = AccountsModel.query.get_or_404(organiser_id)


    #     try:
    #         db.session.delete(venue)
    #         db.session.commit()
    #         organiser.events.remove(venue)

    #     except SQLAlchemyError:
    #         abort(500, message="An error occurred while deleting venue.")

    #     return {"message": "Venue has been deleted"}
    



