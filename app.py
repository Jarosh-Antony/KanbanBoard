from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import datetime

app=Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///kanbandb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

import summary

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


@app.route("/boards/<int:userID>")
def boards(userID):
    boards=Boards.query.filter_by(userID=userID).all()
    uName=Users.query.filter_by(id=userID).first().name
    return render_template("home.html",boards=boards,userID=userID,name=uName)

 
@app.route("/",methods=["GET","POST"])
def index():
    message=''
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
    
  
@app.route("/<int:userID>/addBoard",methods=["GET","POST"])
def createBoard(userID):
    if request.method=="GET":
        return render_template("createBoard.html",userID=userID)
    else :
        name=request.form["name"]
        board=Boards.query.filter_by(userID=userID,name=name).first()
        if board==None:
            newBoard=Boards(name=name,userID=userID)
            db.session.add(newBoard)
            db.session.commit()
            return redirect(url_for("board",boardID=newBoard.id))
        return render_template("createBoard.html",userID=userID,alert='t',name=name)


@app.route("/board/<int:boardID>/delete")
def deleteBoard(boardID):
    board=Boards.query.filter_by(id=boardID).first()
    userID=board.userID
    db.session.delete(board)
    db.session.commit()
    return redirect(url_for("boards",userID=userID))


@app.route("/board/<int:boardID>/update",methods=["GET","POST"])
def updateBoard(boardID):
    board=Boards.query.filter_by(id=boardID).first()
    userID=board.userID
    if request.method=="GET":
        return render_template("updateBoard.html",board=board)
    else :
        name=request.form["name"]
        b=Boards.query.filter_by(userID=userID,name=name).first()
        if b==None or b.id==board.id :
            board.name=request.form['name']
            db.session.commit()
            return redirect(url_for("boards",userID=userID))
        return render_template("updateBoard.html",board=board,name=name,alert='t')
    


@app.route("/board/<int:boardID>",methods=["GET","POST"])
def board(boardID):
    lists=Lists.query.filter_by(boardID=boardID).all()
    cards=dict()
    Ccards=dict()
    DT=str(datetime.datetime.now())
    for list in lists:
        c=Cards.query.filter_by(listID=list.id).all()
        for card in c:
            if card.completed=='NO':
                if list.id not in cards:
                    cards[list.id]=[]
                cards[list.id].append(card)
            else :
                if list.id not in Ccards:
                    Ccards[list.id]=[]
                Ccards[list.id].append(card)
    return render_template("board.html",lists=lists,cards=cards,Ccards=Ccards,boardID=boardID,DT=DT)
    
    
@app.route("/list/<int:boardID>/new",methods=["GET","POST"])
def newList(boardID):
    if request.method=="GET":
        return render_template("newList.html",boardID=boardID)
    
    else :
        name=request.form['name']
        list=Lists.query.filter_by(boardID=boardID,name=name).first()
        if list==None:
            newList=Lists(name=name,boardID=boardID)
            db.session.add(newList)
            db.session.commit()
            return redirect(url_for("board",boardID=boardID))
        return render_template("newList.html",boardID=boardID,alert='t',name=name)


@app.route("/<int:boardID>/list/<int:listID>/delete",methods=["GET","POST"])
def deleteList(boardID,listID):
    if request.method=="GET":
        cards=Cards.query.filter_by(listID=listID).first()
        if cards != None:
            return render_template("deleteList.html",boardID=boardID,listID=listID)
        else:
            reply='del'
    else :
        reply=request.form['action']
    if reply=='del':
        list=Lists.query.filter_by(id=listID).first()
        db.session.delete(list)
        db.session.commit()
        return redirect(url_for("board",boardID=boardID))
    elif reply=='move':
        return redirect(url_for("moveList",boardID=boardID,listID=listID))
    else :
        return redirect(url_for("board",boardID=boardID))



@app.route("/<int:boardID>/list/<int:listID>/update",methods=["GET","POST"])
def updateList(boardID,listID):
    list=Lists.query.filter_by(id=listID).first()
    if request.method=="GET":
        return render_template("updateList.html",boardID=boardID,list=list)
    else :
        name=request.form['name']
        l=Lists.query.filter_by(boardID=boardID,name=name).first()
        if l==None or l.id==list.id:
            list.name=name
            db.session.commit()
            return redirect(url_for("board",boardID=boardID))
        return render_template("updateList.html",boardID=boardID,list=list,alert='t',name=name)
        
        
@app.route("/<int:boardID>/card/<int:listID>/moveAll",methods=["GET","POST"])
def moveList(boardID,listID):
    lists=Lists.query.filter_by(boardID=boardID).all()
    if request.method=="GET":
        return render_template("moveAllCards.html",listID=listID,boardID=boardID,lists=lists)
    cards=Cards.query.filter_by(listID=listID).all()
    Tlist=int(request.form['listID'])
    Tcards=Cards.query.filter_by(listID=Tlist).all()
    Ttitle=[]
    for card in Tcards:
        Ttitle.append(card.title)
    alert='f'
    for card in cards:
        if card.title in Ttitle:
            alert='t'
        else :
            card.listID=Tlist
    if alert=='f':
        list=Lists.query.filter_by(id=listID).first()
        db.session.delete(list)
    db.session.commit()
    if alert=='t':
        return render_template("moveAllCards.html",listID=listID,boardID=boardID,lists=lists,alert=alert)
    return redirect(url_for("board",boardID=boardID))
    

@app.route("/<int:boardID>/card/<int:listID>/new",methods=["GET","POST"])
def newCard(boardID,listID):
    if request.method=="GET":
        return render_template("newCard.html",listID=listID,boardID=boardID)
    
    else :
        title=request.form['title']
        content=request.form['content']
        deadline=request.form['deadline'].replace('T',' ')
        card=Cards.query.filter_by(listID=listID,title=title).first()
        if card==None:
            createdD=str(datetime.datetime.now())
            modifiedD=createdD
            newCard=Cards(title=title,content=content,deadline=deadline,listID=listID,createdD=createdD,modifiedD=modifiedD)
            db.session.add(newCard)
            db.session.commit()
            return redirect(url_for("board",boardID=boardID))
        fr=request.form
        return render_template("newCard.html",listID=listID,boardID=boardID,alert='t',fr=fr,title=title)


@app.route("/<int:boardID>/card/<int:cardID>/completed",methods=["GET","POST"])
def completedCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    card.completed='YES'
    card.completedD=str(datetime.datetime.now())
    db.session.commit()
    return redirect(url_for("board",boardID=boardID))


@app.route("/<int:boardID>/card/<int:cardID>/details",methods=["GET","POST"])
def detailCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    list=Lists.query.filter_by(id=card.listID).first().name
    return render_template("details.html",card=card,list=list,boardID=boardID)
    
    
@app.route("/<int:boardID>/card/<int:cardID>/incompleted",methods=["GET","POST"])
def incompletedCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    card.completed='NO'
    card.modifiedD=str(datetime.datetime.now())
    db.session.commit()
    return redirect(url_for("board",boardID=boardID))


@app.route("/<int:boardID>/card/<int:cardID>/delete",methods=["GET","POST"])
def deleteCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for("board",boardID=boardID))


@app.route("/<int:boardID>/card/<int:cardID>/update",methods=["GET","POST"])
def updateCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    if request.method=="GET":
        return render_template("updateCard.html",boardID=boardID,card=card)
    else :
        title=request.form['title']
        content=request.form['content']
        deadline=request.form['deadline'].replace('T',' ')
        c=Cards.query.filter_by(listID=card.listID,title=title).first()
        if c==None or c.id==card.id:
            card.title=title
            card.content=content
            card.deadline=deadline
            card.modifiedD=str(datetime.datetime.now())
            db.session.commit()
            return redirect(url_for("board",boardID=boardID))
        fr=request.form
        return render_template("updateCard.html",boardID=boardID,card=card,alert='t',title=title)


@app.route("/<int:boardID>/card/<int:cardID>/move",methods=["GET","POST"])
def moveCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    lists=Lists.query.filter_by(boardID=boardID).all()
    if request.method=="GET":
        return render_template("moveCard.html",boardID=boardID,card=card,lists=lists)
    else :
        listID=int(request.form['listID'])
        c=Cards.query.filter_by(listID=listID,title=card.title).first()
        if c==None or listID==card.listID:
            card.listID=listID
            db.session.commit()
            return redirect(url_for("board",boardID=boardID))
        return render_template("moveCard.html",boardID=boardID,card=card,lists=lists,alert='t',title=card.title)

@app.route("/back/<int:boardID>")
def backBoards(boardID):
    userID=Boards.query.filter_by(id=boardID).first().userID
    return redirect(url_for("boards",userID=userID))



if __name__ =='__main__':
    app.run()
    app.debug=True