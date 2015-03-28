from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga
from model.Question import Question
from model.Vote import Vote
import json

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self):
        user = self.getuser()
        if(user is not None):
            jirgas = Jirga.get(user.jirgas)
            result = {}
            self.response.headers['Content-Type'] = 'application/json'
            for jirga in jirgas:
                obj2 = {
                    'name': jirga.title,
                    'key': jirga.jirgaId,
                }
                questions = Question.get(jirga.questions)
                for question in questions:
                    if user.key not in question.voted:
                        obj3 = {
                            'key':question.key(),
                            'title':question.questionString,
                            'author':question.author
                        }
                        votes = Vote.get(question.votes)
                        for vote in votes:
                            if vote is not None:
                                obj4 = {
                                    'vote':vote.number,
                                    'answer':vote.answer,
                                    'count':vote.count
                                }
                                obj3.update(obj4)
                        obj2.update(obj3)
                        result.update(obj2)
                    #else:
                    #user has already voted skip this question

            self.response.out.write(json.dumps(result))
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/getMyQuestions', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
