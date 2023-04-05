from db import db


class TicketsModel(db.Model):
    __tablename__ = "tickets"

    id= db.Column(db.Integer, primary_key=True)
    event_id=db.Column(db.Integer, db.ForeignKey("events.id"),nullable=False)
    seat_id= db.Column(db.Integer, nullable=False)
    is_booked=db.Column(db.Boolean, nullable=False)
    booking_id= db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable = True)

    bookings=db.relationship("BookingsModel", back_populates="tickets")
    events=db.relationship("EventsModel", back_populates="tickets")



