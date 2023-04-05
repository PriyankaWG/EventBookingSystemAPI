from db import db


class EventsModel(db.Model):
    __tablename__ = "events"

    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue_id = db.Column(db.String, unique=True, nullable=False)
    performer_id = db.Column(db.Integer, db.ForeignKey("performers.acc_id"),nullable=False)
    organiser_id = db.Column(db.Integer, db.ForeignKey("accounts.id"),nullable=False)
    ticket_price = db.Column(db.Integer,nullable=False)
    total_tickets = db.Column(db.Integer, db.ForeignKey("venues.no_of_tickets"))
    sold_tickets = db.Column(db.Integer)


    organiser = db.relationship("AccountsModel", back_populates="events")
    venues = db.relationship("VenuesModel", back_populates="events")
    performer = db.relationship("PerformersModel", back_populates="event")
    tickets=db.relationship("TicketsModel", back_populates="events", lazy="dynamic")
    bookings=db.relationship("BookingsModel", back_populates="event")