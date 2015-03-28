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

    #post:
    #jirga name
    #whether it is public or private
    def post(self):
        user = self.getuser()
        if(user is not None):
            jirgaKey = self.request.get('jirgaKey')
            jirga = Jirga.get(jirgaKey)
            questionKey = self.request.get('questionKey')
            question = Question.get(questionKey)
            if user.key not in question.voted && user.key is in jirga.members:
                voteNum = self.request.get('voteNum')
                vote = Vote.get(Question.votes.index(voteNum-1))
                vote.users.append(user.key)
                vote.count += 1
                vote.put()
                question.voted.append(user.key)
                question.put()
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/vote', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
