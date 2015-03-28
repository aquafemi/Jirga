import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User


def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self):
        print("yo")
        if self.session.get('user'):
            self.response.out.write('User is already logged in')
        else:
            self.response.out.write('User is not logged in')
    #post to login will receive:
    #username="username"
    #password="password"
    #should give user session
    def post(self):
        username=self.request.get('username')
        password=self.request.get('username')
        #uquery=User.all.

app = webapp2.WSGIApplication([('/login', MainHandler)], config=sessions_module.myconfig_dict, debug=True)