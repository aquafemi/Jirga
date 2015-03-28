import json
from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User, Session
from model.Jirga import Jirga
from model.Question import Question
from model.Vote import Vote
from google.appengine.ext.webapp import template
import uuid

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)

class MainHandler(sessions_module.BaseSessionHandler):
    def get(self):
        user = self.getuser()
        if(user is not None):
            jirgas = Jirga.get(user.jirgas)
            template_params = {'jirgas':jirgas}
            render_template(self,"askJirga.html",template_params)
        else:
            self.response.write("FAIL - not logged in")

    def post(self):
        user = self.getuser()
        if user is not None:
            jirgaId = self.request.get('jirgaId')
            questionString = self.request.get('questionString')
            jirga = Jirga.all().filter('jirgaId', jirgaId).get()
            if jirga is not None:
                if questionString != "" and questionString is not None:
                    if jirga.publicJirga == 1 or jirga.owner == user.username:
                        i = uuid.uuid1()
                        question = Question(questionString=questionString, author=user.username,qId=(str(i)))
                        question.put()
                        jirga.questions.append(question.key())
                        jirga.put()
                        self.response.out.write(question.qId)
                    else:
                        self.response.write("FAIL - insufficient permissions")
                else:
                    self.response.write("FAIL - invalid question - " + questionString)
            else:
                self.response.write("FAIL - invalid jirga")
        else:
            self.response.write("FAIL - not logged in")


app = webapp2.WSGIApplication([('/makeQuestion', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
