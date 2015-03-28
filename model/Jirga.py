from google.appengine.ext import db

class Jirga(db.Model):
    title = db.StringProperty()
    members = db.ListProperty(db.Key)
    owner = db.StringProperty() #username of the owner
    questions = db.ListProperty(db.Key)
    publicJirga = db.IntegerProperty() #0 if private, 1 if public
    jirgaId = db.StringProperty()