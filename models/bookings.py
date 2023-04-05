from db import db


class BookingsModel(db.Model):
    __tablename__ = "bookings"

    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("accounts.id"),nullable=False)
    no_of_tickets= db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"),nullable=False)

    
    user = db.relationship("AccountsModel", back_populates="bookings")
    tickets=db.relationship("TicketsModel", back_populates="bookings")
    event = db.relationship("EventsModel", back_populates="bookings")
    




