from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
from model.Question import Question
from model.Jirga import Jirga
import sessions_module
from model.User import User,Session
from model.Vote import Vote
import uuid

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self,questionId):
        loggedIn= False
        user = self.getuser()
        if(user is not None):
            question = Question.all().filter('qId', questionId).get()
            votes = Vote.get(question.votes)
            template_params = {
                'question': question,
                'votes': votes
            }
            
            render_template(self,"viewQuestion.html",template_params)
        else:
            self.response.write("FAIL - you need to be logged in for this")



app = webapp2.WSGIApplication([('/viewQuestion/(.*?)', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
