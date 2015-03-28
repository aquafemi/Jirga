from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User, Session
from model.Jirga import Jirga
from model.Question import Question
from model.Vote import Vote


class MainHandler(sessions_module.BaseSessionHandler):
    def post(self):
        user = self.getuser()
        if user is not None:
            jirgaId = self.request.get('jirgaId')
            questionString = self.request.get('answerString')
            jirga = Jirga.all().filter('jirgaId', jirgaId).get()
            if jirga is not None:
                if questionString != "" and questionString is not None:
                    if jirga.public == 1 or jirga.owner == user.username:
                        question = Question(questionString=questionString, author=user.username)
                        question.put()
                        jirga.questions.add(question.key())
                        jirga.put()
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:
                self.response.write("FAIL")
        else:
            self.response.write("FAIL - not logged in")


app = webapp2.WSGIApplication([('/makeQuestion', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
