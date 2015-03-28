from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga
from model.Question import Question
from model.Vote import Vote

class MainHandler(sessions_module.BaseSessionHandler):
    def post(self):
        user = self.getuser()
        if user is not None:
            jirgaId = self.request.get('jirgaId')
            questionId = self.request.get('questionId')
            print(questionId)
            answerString = self.request.get('answerString')
            jirga = Jirga.all().filter('jirgaId', jirgaId).get()
            question = Question.all().filter('qId',questionId).get()
            if jirga is not None and question is not None:
                if answerString != "" and answerString is not None:
                    if question.author == user.username:
                        vote = Vote(answer=answerString,number=len(question.votes))
                        vote.put()
                        question.votes.append(vote.key())
                        question.put()
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:

                self.response.write("FAIL")
        else:

            self.response.write("FAIL - not logged in")


app = webapp2.WSGIApplication([('/makeVote', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
