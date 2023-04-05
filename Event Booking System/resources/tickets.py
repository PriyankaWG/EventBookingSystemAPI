from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EventsModel, AccountsModel, TicketsModel
from schemas import TicketSchema, VenueSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Tickets", "ticket", description="Operations on ticket")


@blp.route("/users/<int:user_id>/bookings/<int:booking_id>/tickets/<int:ticket>")
class BookingList(MethodView):
    
    @blp.response(200,TicketSchema)
    def delete(self,user_id,booking_id,ticket_id):
        user = AccountsModel.query.get_or_404(user_id)
        ticket = TicketsModel.query.get_or_404(ticket_id)

        if ticket.booking_id != booking_id:
            abort(400, message="This ticket doesn't belong to this booking ID")

        ticket.is_booked=False
        ticket.booking_id='NULL'


        return 
    

    

    
