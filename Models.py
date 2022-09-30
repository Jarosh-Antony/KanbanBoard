
from sqlalchemy.orm import relationship

from __main__ import db



class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email=db.Column(db.String,nullable=False,unique=True)
    name = db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    Boards = db.relationship("Boards", cascade="all,delete", backref="Users")



class Boards(db.Model):
    __tablename__ = "Boards"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    userID=db.Column(db.Integer,db.ForeignKey("Users.id"),nullable=False)
    Lists = db.relationship("Lists", cascade="all,delete", backref="Boards")



class Lists(db.Model):
    __tablename__ = "Lists"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    boardID=db.Column(db.Integer,db.ForeignKey("Boards.id"),nullable=False)
    Cards = db.relationship("Cards", cascade="all,delete", backref="Lists")
     



class Cards(db.Model):
    __tablename__ = "Cards"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title=db.Column(db.String,nullable=False)
    content = db.Column(db.String)
    deadline=db.Column(db.String)
    completed=db.Column(db.String,nullable=False,default='NO')
    listID = db.Column(db.Integer,db.ForeignKey("Lists.id"),nullable=False)
    createdD=db.Column(db.String,nullable=False)
    modifiedD=db.Column(db.String,nullable=False)
    completedD=db.Column(db.String)
    ldetail=db.relationship("Lists",viewonly=True)

