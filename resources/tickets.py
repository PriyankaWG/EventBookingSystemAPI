from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EventsModel, AccountsModel, TicketsModel, BookingsModel
from schemas import TicketSchema, VenueSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Tickets", "ticket", description="Operations on ticket")


@blp.route("/users/<int:user_id>/bookings/<int:booking_id>/tickets/<int:ticket_id>")
class BookingList(MethodView):
    
    @blp.response(200,TicketSchema)
    def put(self,user_id,booking_id,ticket_id):
       
        ticket = TicketsModel.query.get_or_404(ticket_id)
      
        if ticket.booking_id != booking_id:
            abort(400, message="This ticket doesn't belong to this booking ID")
        
        booking=BookingsModel.query.get_or_404(booking_id)

        if booking.user_id != user_id:
            abort(400, message="This ticket doesn't belong to this user ID")

        booking.no_of_tickets= booking.no_of_tickets-1

        event = EventsModel.query.get_or_404(ticket.event_id)
        event.sold_tickets= event.sold_tickets-1

        ticket.is_booked=False
        ticket.booking_id= None
        db.session.commit()
        

        return {"message":"Ticket cancelled"}
    

    

    
