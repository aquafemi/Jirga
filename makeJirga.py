from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User,Session
import uuid

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self):
        template_params = {}
        render_template(self,"makeJirga.html",template_params)
    #post:
    #jirga name
    #whether it is public or private
    def post(self):
        

app = webapp2.WSGIApplication([('/makeJirga', MainHandler)], config=sessions_module.myconfig_dict, debug=True)