from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga
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
        user = self.getuser()
        if(user is not None):
            jirgaName = self.request.get('jirgaName')
            public = self.request.get('option1')
            private = self.request.get('option2')
            if public is not None:
                i = uuid.uuid1()
                newJirga = Jirga(title=jirgaName,owner=user.username,publicJirga=1,jirgaId=str(i))
                newJirga.put()
                user.jirgas.append(newJirga.key())
                user.put()
                #TODO render stuff
                self.response.write("Success")
            elif private is not None:
                i = uuid.uuid1()
                newJirga = Jirga(title=jirgaName,owner=user.username,publicJirga=0,jirgaId=str(i))
                newJirga.put()
                user.jirgas.append(newJirga.key())
                user.put()
                #TODO render stuff
                self.response.write("Success")
            else:
                self.response.write("FAIL - privacy not selected")
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/makeJirga', MainHandler)], config=sessions_module.myconfig_dict, debug=True)