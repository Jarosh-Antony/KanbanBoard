from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///kanbandb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()


import Models
import Summary,User,Board,List,Card


@app.route("/")
def index():
    return render_template("home.html")


if __name__ =='__main__':
    app.run()
    
    
    
