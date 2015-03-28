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
                    obj3 = {
                        'key':question.key(),
                        'title':question.questionString,
                        'author':question.author
                    }
                    votes = Vote.get(question.votes)
                    for vote in votes:
                        obj4 = {
                            'vote':vote.number,
                            'answer':vote.answer,
                            'count':vote.count
                        }
                        obj3.update(obj4)
                    obj2.update(obj3)
                result.update(obj2)
            self.response.out.write(json.dumps(result))
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/getMyJirgas', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
