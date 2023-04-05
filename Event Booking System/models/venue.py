from db import db


class VenuesModel(db.Model):
    __tablename__ = "venues"

    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True ,nullable=False)
    address = db.Column(db.String, unique=True)
    price = db.Column(db.Integer, nullable=False)
    no_of_tickets = db.Column(db.Integer, nullable=False)
    organiser_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)

    events=db.relationship("EventsModel", back_populates="venues", cascade="all,delete")
    organiser=db.relationship("AccountsModel",back_populates="venues" )
