from db import db


class PerformersModel(db.Model):
    __tablename__ = "performers"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    acc_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    price=db.Column(db.Integer, nullable=False)
    is_booked=db.Column(db.Boolean, nullable=False)

    accounts = db.relationship("AccountsModel", back_populates="performers")
    # bookings = db.relationship("AccountsModel", back_populates="accounts", cascade="all,delete", lazy="dynamic")
    event = db.relationship("EventsModel", back_populates="performer")
