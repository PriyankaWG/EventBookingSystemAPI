from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EventsModel, AccountsModel, BookingsModel, TicketsModel
from schemas import BookingSchema, TicketSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Bookings", "booking", description="Operations on booking")



@blp.route("/user/<int:user_id>/bookings")
class BookingList(MethodView):
    
    @blp.response(200,BookingSchema(many=True))
    def get(self,user_id):
        user = AccountsModel.query.get_or_404(user_id)
        return user.bookings.all()
    
    
    @blp.arguments(BookingSchema) 
    @blp.response(201,description="Booking created")
    def post(self, user_id, booking_data):
        event=EventsModel.query.get_or_404(booking_data("event_id"))

        if EventsModel.query.filter(event.total_tickets-event.sold_tickets < booking_data["no_of_tickets"]).first():
            abort(400, message= "Not enough tickets left")

        booking =BookingsModel(**booking_data, user_id=user_id)
        
        
        user=AccountsModel.query.get_or_404(user_id)
        
        tickets = TicketsModel.query.filter(TicketsModel.event_id==booking_data("event_id"), TicketsModel.is_booked==False).all()

        for t in range(booking_data["no_of_tickets"]):

            tickets[t].is_booked = True
            tickets[t].booking_id = booking_data["id"]

        try:
            db.session.add(booking)
            db.session.commit()
            user.bookings.append(booking)

        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        event.sold_tickets= event.sold_tickets+booking_data["no_of_tickets"]

        return
    

    
@blp.route("/user/<int:user_id>/bookings/<int:booking_id>")
class BookingList(MethodView):
    
    @blp.response(200, TicketSchema)
    def get(self,user_id, booking_id):

        booking= BookingsModel.query.get_or_404(booking_id)

        if booking.user_id != user_id:
            abort(400, message=f"No such booking under you")

        tickets = TicketsModel.query.filter(TicketsModel.booking_id == booking_id).all()

        return tickets
    

    @blp.response(202, TicketSchema)
    def delete(self,user_id, booking_id):
        booking= BookingsModel.query.get_or_404(booking_id)
        user=AccountsModel.query.get_or_404(user_id)

        if booking.user_id != user_id:
            abort(400, message=f"No such booking under you")

        

        tickets = TicketsModel.query.filter(TicketsModel.booking_id==booking_id).all()

        for t in range(booking.no_of_tickets):

            tickets[t].is_booked = False
            tickets[t].booking_id = 'NULL'

        try:
            db.session.delete(booking)
            db.session.commit()
            user.bookings.delete(booking)

        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        

        print("Booking deleted")
        return 
    

    
