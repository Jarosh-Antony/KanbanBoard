from flask import render_template
from flask import request, redirect, url_for
import datetime

from __main__ import app,db
from Models import Cards,Lists,Boards,Users


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
    