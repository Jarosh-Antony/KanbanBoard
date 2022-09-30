from flask import render_template
from flask import request, redirect, url_for
import datetime

from __main__ import app,db
from Models import Cards,Lists,Boards,Users





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
    


@app.route("/board/<int:boardID>")
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
