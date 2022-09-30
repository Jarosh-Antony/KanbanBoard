from flask import render_template
from flask import request, redirect, url_for
import datetime
import matplotlib.pyplot as plt

from __main__ import app,db
from Models import Cards,Lists,Boards,Users

 
@app.route("/<int:boardID>/summary",methods=["GET","POST"])
def summary(boardID):
   
    tasks=dict()
    tasks['dlcross']=[]
    tasks['todo']=[]
    tasks['ontime']=[]
    tasks['late']=[]
    time=str(datetime.datetime.now())
    lists=Lists.query.filter_by(boardID=boardID).all()
    
    if request.method=="POST":
        listID=int(request.form['listID'])
        cards=Cards.query.filter_by(listID=listID).all()
    else:
        listID=-1
        cards=db.session.query(Cards).filter(Cards.listID==Lists.id).join(Lists.query.filter_by(boardID=boardID)).all()
        
    
    for card in cards:
        list=card.ldetail.name
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
    
    if total>0:
        sizes=[]
        colors=[]
        if c>0:
            sizes.append(c/total)
            colors.append((0.0,0.5882352941176471,0.0))
        if d>0:
            sizes.append(d/total)
            colors.append((0.5882352941176471,0.5725490196078431,0.0))
        if a>0:
            sizes.append(a/total)
            colors.append('r')
        if b>0:
            sizes.append(b/total)
            colors.append('b')
        
        fig1,ax1 = plt.subplots()
        ax1.pie(sizes,colors=colors,autopct='%1.1f%%')
        ax1.axis('equal')

        plt.savefig("static/pieTasks.jpg")
    return render_template("summary.html",tasks=tasks,boardID=boardID,listID=listID,lists=lists,total=total,list=list)
        
    
    