from flask import render_template
from flask import request, redirect, url_for
import datetime

from __main__ import app,db
from Models import Cards,Lists,Boards,Users

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        valid=False if Users.query.filter_by(email=email,password=password).first()==None else True
        if(valid):
            userID=Users.query.filter_by(email=email).first().id
            return redirect(url_for("boards",userID=userID))
        
        return render_template("login.html",alert='t')
    return render_template("login.html")
        

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    email=request.form["email"]
    name=request.form["name"]
    password=request.form["password"]
    fr=request.form
    try:
        newUser=Users(email=email,name=name,password=password)
        db.session.add(newUser)
        db.session.commit()
    except:
        return render_template("register.html",alert='t',fr=fr)
        
    return redirect(url_for("boards",userID=newUser.id))

  
@app.route("/<int:userID>/settings",methods=["GET","POST"])
def settings(userID):
    user=Users.query.filter_by(id=userID).first()
    if request.method=="GET":
        return render_template("settings.html",user=user)
    user.name=request.form["name"]
    user.password=request.form["password"]
    db.session.commit()   
    return redirect(url_for("boards",userID=user.id))


@app.route("/<int:userID>/delete")
def delete(userID):
    user=Users.query.filter_by(id=userID).first()
    db.session.delete(user)
    db.session.commit()   
    return redirect(url_for("index"))
    
    
@app.route("/boards/<int:userID>")
def boards(userID):
    boards=Boards.query.filter_by(userID=userID).all()
    uName=Users.query.filter_by(id=userID).first().name
    return render_template("boards.html",boards=boards,userID=userID,name=uName)



@app.route("/back/<int:boardID>")
def backBoards(boardID):
    userID=Boards.query.filter_by(id=boardID).first().userID
    return redirect(url_for("boards",userID=userID))


