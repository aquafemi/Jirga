from google.appengine.ext import db

class Question(db.Model):
    questionString = db.StringProperty()
    votes = db.ListProperty(db.Key)
    author = db.StringProperty()
    voted = db.ListProperty(db.Key)
    #comments = db.ListProperty(db.Key)
