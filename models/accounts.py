from db import db


class AccountsModel(db.Model):
    __tablename__ = "accounts"

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(), nullable=False)
    role=db.Column(db.Integer(), db.ForeignKey("roles.id"),nullable=False)

    events = db.relationship("EventsModel", back_populates="organiser", cascade="all,delete", lazy="dynamic")
    bookings = db.relationship("BookingsModel", back_populates="user", cascade="all,delete", lazy="dynamic")
    roles = db.relationship("RolesModel", back_populates="accounts")
    performers = db.relationship("PerformersModel", back_populates="accounts", cascade="all,delete")
    venues = db.relationship("VenuesModel", back_populates="organiser", cascade="all,delete", lazy="dynamic")
