from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    jirgas = db.ListProperty(db.Key)

class Session(db.Model):
    sessId = db.StringProperty()
    user = db.StringProperty()