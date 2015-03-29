from google.appengine.ext import db
import time
import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User, Session
from model.Jirga import Jirga
import uuid


def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)


class MainHandler(sessions_module.BaseSessionHandler):
    def get(self):
        template_params = {}
        render_template(self, "makeJirga.html", template_params)

    # post:
    #jirga name
    #whether it is public or private
    def post(self):
        user = self.getuser()
        if (user is not None):
            jirgaName = self.request.get('jirgaName')
            privacyOption = self.request.get('privacyOption')
            if privacyOption == "option1":
                i = uuid.uuid1()
                newJirga = Jirga(title=jirgaName, owner=user.username, publicJirga=1, jirgaId=str(i))
                newJirga.put()
                user.jirgas.append(newJirga.key())
                user.put()
                time.sleep(1)
                self.redirect("/")
            elif privacyOption == "option2":
                i = uuid.uuid1()
                newJirga = Jirga(title=jirgaName, owner=user.username, publicJirga=0, jirgaId=str(i))
                newJirga.put()
                user.jirgas.append(newJirga.key())
                user.put()
                time.sleep(1)
                self.redirect("/")
            else:
                self.response.write("FAIL - privacy not selected")
        else:
            self.response.write("FAIL - not logged in")


app = webapp2.WSGIApplication([('/makeJirga', MainHandler)], config=sessions_module.myconfig_dict, debug=True)