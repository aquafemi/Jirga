from google.appengine.ext import db

class Vote(db.Model):
    answer = db.StringProperty()
    count = db.IntegerProperty()