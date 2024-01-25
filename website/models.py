"""def models(db):
    from flask_login import UserMixin
    from sqlalchemy.sql import func
    class Note(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        data = db.Column(db.String(10000))
        date = db.Column(db.DateTime(timezone=True), default=func.now())
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(150), unique=True)
        password = db.Column(db.String(150))
        first_name = db.Column(db.String(150))
        last_name = db.Column(db.String(150))
        phone_number = db.Column(db.String(20))
    return User
    #notes = db.relationship('Note')
    #return [User, Note]
    def __init__(self, email, password, first_name,last_name,phone_number):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
"""