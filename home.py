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
            jirgas = Jirga.all()
            newlist=[]
            goodQuestions = []
            pubJirgas = []
            for jirga in jirgas:
                if jirga is not None and (user.key() in jirga.members or jirga.owner == user.username):
                    newlist.append(jirga)
                    for qkey in jirga.questions:
                        question = Question.get(qkey)
                        if question is not None and user.key not in question.voted:
                            goodQuestions.append(question)
                elif jirga is not None and jirga.publicJirga==1:
                    pubJirgas.append(jirga)

            #check to avoid throwing unbounderror when no jirgas
            #todo - make this give a warning when no jirgas
            if len(newlist) < 1:
                template_params = {
                    'jirgasmem':newlist,
                    'jirgaspub':pubJirgas,
                    'questions':goodQuestions
                }
            else:
                template_params = {
                    'questions':goodQuestions, #throws exception when goodQuestions not initialized (due to no Jirgas)
                    'jirgasmem':jirgas,
                    'jirgaspub':pubJirgas
                }
            render_template(self,"home.html",template_params)
        else:
            self.redirect("/login")

app = webapp2.WSGIApplication([('/', MainHandler)], config=sessions_module.myconfig_dict, debug=True)

