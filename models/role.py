from db import db


class RolesModel(db.Model):
    __tablename__ = "roles"

    id= db.Column(db.Integer, primary_key=True)
    role= db.Column(db.String(), nullable=False, unique=True)
    
    accounts = db.relationship("AccountsModel", back_populates="roles")
    