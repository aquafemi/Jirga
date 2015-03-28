from google.appengine.ext import db

class Jirga(db.Model):
    members = db.ListProperty(db.Key)
    owner = db.ListProperty(db.Key)
    questions = db.ListProperty(db.Key)
    publicJirga = db.IntegerProperty() #0 if private, 1 if public