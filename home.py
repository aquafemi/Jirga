from google.appengine.ext import db
from google.appengine.ext.webapp import template
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga
from model.Question import Question
from model.Vote import Vote
import json

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)


class MainHandler(sessions_module.BaseSessionHandler):

    def get(self):
        user = self.getuser()
        if(user is not None):
            jirgas = Jirga.get(user.jirgas)
            for jirga in jirgas:
                questions = Question.get(jirga.questions)
                goodQuestions = []
                for question in questions:
                    if question is not None and user.key not in question.voted:
                        goodQuestions.append(question)
            pubJirgas = []
            pubJirga = Jirga.all().filter('publicJirga',1).get()
            pubJirgas.append(pubJirga)
            template_params = {
                'questions':goodQuestions,
                'jirgasmem':jirgas,
                'jirgaspub':pubJirgas
            }
            render_template(self,"home.html",template_params)
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/', MainHandler)], config=sessions_module.myconfig_dict, debug=True)

