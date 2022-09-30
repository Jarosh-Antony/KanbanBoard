from flask import render_template
from flask import request, redirect, url_for
import datetime

from __main__ import app,db
from Models import Cards,Lists,Boards,Users


    


@app.route("/<int:boardID>/card/<int:listID>/new",methods=["GET","POST"])
def newCard(boardID,listID):
    if request.method=="GET":
        return render_template("newCard.html",listID=listID,boardID=boardID)
    
    else :
        title=request.form['title']
        content=request.form['content']
        deadline=request.form['deadline'].replace('T',' ')
        deadline+=':00.000000'
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


@app.route("/<int:boardID>/card/<int:cardID>/details")
def detailCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    deadline=datetime.datetime.strptime(card.deadline,'%Y-%m-%d %H:%M:%S.%f')
    createdD=datetime.datetime.strptime(card.createdD,'%Y-%m-%d %H:%M:%S.%f')
    current=datetime.datetime.now()
    if card.completed=='YES':
        completedD=datetime.datetime.strptime(card.completedD,'%Y-%m-%d %H:%M:%S.%f')
    
    
    if deadline<createdD and card.completedD=="YES":
        allotted=(createdD-deadline).total_seconds()
        elapsed=(completedD-deadline).total_seconds()
        
    elif deadline<createdD:
        allotted=(createdD-deadline).total_seconds()
        elapsed=(current-deadline).total_seconds()
        
    elif card.completed=='NO':
        allotted=(deadline-createdD).total_seconds()
        elapsed=(current-createdD).total_seconds()
    
    else :
        allotted=(deadline-createdD).total_seconds()
        elapsed=(completedD-createdD).total_seconds()
    
    if allotted>elapsed:
        Awidth=100
        Ewidth=(elapsed/allotted)*100
        pos=Ewidth*0.3-0.8
    
    else :
        Ewidth=100
        Awidth=(allotted/elapsed)*100
        pos=Awidth*0.3-0.8
        
    list=Lists.query.filter_by(id=card.listID).first().name
    return render_template("details.html",card=card,list=list,boardID=boardID,Awidth=Awidth,Ewidth=Ewidth,pos=pos)
    
    
@app.route("/<int:boardID>/card/<int:cardID>/incompleted")
def incompletedCard(boardID,cardID):
    card=Cards.query.filter_by(id=cardID).first()
    card.completed='NO'
    card.modifiedD=str(datetime.datetime.now())
    db.session.commit()
    return redirect(url_for("board",boardID=boardID))


@app.route("/<int:boardID>/card/<int:cardID>/delete")
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
            card.deadline=deadline+':00.000000'
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
