#!/bin/python3 
"""from flask_sqlalchemy import SQLAlchemy
from app import app


app.config['SECRET_KEY'] = 'whoisthedeveloperinthis'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy()
db.init_app(app)

from . import models
#global User, Note
#User,Note = model(db)
#model(db)

#app.register_blueprint(auth.auth)
with app.app_context():
    db.create_all()"""