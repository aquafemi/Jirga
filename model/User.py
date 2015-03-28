from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    public_jirgas = db.ListProperty(db.Key)