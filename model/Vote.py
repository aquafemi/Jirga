from google.appengine.ext import db

class Vote(db.Model):
    answer = db.StringProperty()
    number = db.IntegerProperty()
    count = db.IntegerProperty()
    users = db.ListProperty(db.Key)