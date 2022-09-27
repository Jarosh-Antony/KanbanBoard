from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import datetime
import matplotlib.pyplot as plt

from __main__ import app as a
from app import db,Cards,Lists,Boards,Users

 
@a.route("/<int:boardID>/summary",methods=["GET","POST"])
def summary(boardID):
   
    tasks=dict()
    tasks['dlcross']=[]
    tasks['todo']=[]
    tasks['ontime']=[]
    tasks['late']=[]
    time=str(datetime.datetime.now())[:16]
    lists=Lists.query.filter_by(boardID=boardID).all()
    
    try:
        listID=int(request.form['listID'])
    except:
        listID=-1
    if listID==-1:
        cards=db.session.query(Cards).filter(Cards.listID==Lists.id).join(Lists).all()
    else :
        
        cards=Cards.query.filter_by(listID=listID).all()
    for card in cards:
        if card.completed=='YES':
            if card.deadline<card.completedD:
                tasks['late'].append(card)
            else :
                tasks['ontime'].append(card)
        else :
            if card.deadline<time:
                tasks['dlcross'].append(card)
            else :
                tasks['todo'].append(card)

    a=len(tasks['dlcross'])
    b=len(tasks['todo'])
    c=len(tasks['ontime'])
    d=len(tasks['late'])
    total=a+b+c+d
    sizes = [c/total,d/total,a/total,b/total]
    
    colors=[(0.0,0.5882352941176471,0.0),(0.5882352941176471,0.5725490196078431,0.0),'r','b']
    fig1,ax1 = plt.subplots()
    ax1.pie(sizes,colors=colors,autopct='%1.1f%%')
    ax1.axis('equal')

    plt.savefig("static/pieTasks.jpg")
    return render_template("summary.html",tasks=tasks,boardID=boardID,listID=listID,lists=lists)
        
    
    