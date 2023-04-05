from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import EventsModel, AccountsModel, TicketsModel, PerformersModel, VenuesModel, BookingsModel
from schemas import PlainEventSchema, TicketSchema, EventSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Events", "event", description="Operations on event")


@blp.route("/events")
class EventList(MethodView):
    @blp.response(200,PlainEventSchema(many=True))
    def get(self):
        return EventsModel.query.all()


@blp.route("/organisers/<int:organiser_id>/events")
class EventList(MethodView):
    
    @blp.response(200,PlainEventSchema(many=True))
    def get(self,organiser_id):
        organiser = AccountsModel.query.get_or_404(organiser_id)
        return organiser.events.all()
    

    @blp.arguments(EventSchema)  
    @blp.response(201,EventSchema)
    def post(self, event_data, organiser_id):
   
        # if EventsModel.query.filter(
        #     EventsModel.organiser_id != organiser_id OR
        #     EventsModel.name != event_data["name"], OR
        #     EventsModel.date != event_data["date"], OR
        #     EventsModel.time != event_data["time"], OR
        #     EventsModel.venue_id != event_data["venue_id"]).first():
        #     abort(400, message="Same event already exists.")


        if not VenuesModel.query.filter(VenuesModel.id == event_data["venue_id"]).first():
            abort(400, message="Venue does not exist.")

        if not PerformersModel.query.filter(
            PerformersModel.acc_id == event_data["performer_id"]).first():
            abort(400, message="Performer does not exist.")

        if PerformersModel.query.filter(
            PerformersModel.acc_id == event_data["performer_id"], PerformersModel.is_booked==True).first():
            abort(400, message="Performer already booked.")
        
        venue=VenuesModel.query.get_or_404(event_data["venue_id"])

        if (event_data["total_tickets"]>venue.no_of_tickets):
            abort(400, message="Too many tickets for the venue")


        event = EventsModel(**event_data, organiser_id = organiser_id)
        organiser = AccountsModel.query.get_or_404(organiser_id)
        performer = PerformersModel.query.filter(PerformersModel.acc_id==event_data["performer_id"]).first()
        performer.is_booked=True

        if organiser.role != 1:
            abort(401, message="This ID is not an organiser")


        try:
            db.session.add(event)
            db.session.commit()
            organiser.events.append(event)


        except SQLAlchemyError:
            abort(
                500,
                message="Error in posting event"
            )

        
        for t in range(event_data["total_tickets"]):
            
            ticket=TicketsModel(
                event_id = event.id,
                seat_id = t+1,
                is_booked = False )

            
            try:
                db.session.add(ticket)
                db.session.commit()
                event.tickets.append(ticket)

            except SQLAlchemyError:
                abort(
                    500,
                    message="Error in posting ticket",
                )

        return event



@blp.route("/organisers/<int:organiser_id>/events/<int:event_id>")
class EventList(MethodView):
    
    @blp.response(200,EventSchema)
    def get(self,organiser_id,event_id):
        event = EventsModel.query.get_or_404(event_id)

        if not EventsModel.query.filter(event.organiser_id == organiser_id).first():
            abort(400, message=f"Event {event_id} is not registered by account {organiser_id}.")

        return event
    
    
    @blp.response(202)
    def delete(self, organiser_id, event_id):
        event = EventsModel.query.get_or_404(event_id)

        if event.organiser_id != organiser_id:
            abort(400, message=f"Event {event_id} is not registered by account {organiser_id} .")

        organiser = AccountsModel.query.get_or_404(organiser_id)

        tickets  = TicketsModel.query.filter(TicketsModel.event_id == event_id).all()

        bookings = BookingsModel.query.filter(BookingsModel.event_id == event_id).all()

        for b in bookings:

            user= AccountsModel.query.filter(AccountsModel.id==b.user_id).first()
            
            try:
                db.session.delete(b)
                db.session.commit()
                user.bookings.remove(b)

            except SQLAlchemyError:
                abort(
                    500,
                    message="Error in removing ticket",
                )

        for t in tickets:
            
            try:
                db.session.delete(t)
                db.session.commit()

            except SQLAlchemyError:
                abort(
                    500,
                    message="Error in removing ticket",
                )


        try:
            db.session.delete(event)
            db.session.commit()
            organiser.events.remove(event)

        except SQLAlchemyError:
            abort(500, message="An error occurred while removing event.")

       

        return {"message": "Event has been deleted"}
    


@blp.route("/organisers/<int:organiser_id>/events/<int:event_id>/check_profit")
class EventList(MethodView):
    
    @blp.response(200)
    def get(self,organiser_id,event_id):
        
        event = EventsModel.query.get_or_404(event_id)
        
        if (event.organiser_id != organiser_id):
            abort(400, message=f"Event {event_id} is not registered by account {organiser_id}.")

        venue= VenuesModel.query.filter(VenuesModel.id==event.venue_id).first()
        performer= PerformersModel.query.filter(PerformersModel.acc_id==event.performer_id).first()

        profit=(event.ticket_price*event.sold_tickets)-(venue.price + performer.price)

        return profit
    


@blp.route("/events/<int:event_id>")
class EventList(MethodView):
    
    @blp.response(200,PlainEventSchema)
    def get(self,event_id):
        
        event = EventsModel.query.get_or_404(event_id)

        if(event.total_tickets==event.sold_tickets):
            abort(200, message="No tickets left")

        # tickets_left=TicketsModel.query.filter(TicketSchema.event_id==event_id).all()

        
        return event
    

