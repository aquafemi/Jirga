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
        loggedIn= False
        user = self.getuser()
        if(user is not None):
            loggedIn= True
            uname = user.username
            template_params={
                'loggedIn': loggedIn,
                'user': uname
            }
        else:
            template_params={
                'loggedIn': loggedIn
            }
        render_template(self,'login.html',template_params)

    #post to login will receive:
    #username="username"
    #password="password"
    #should give user session
    def post(self):
        loggedIn= True
        username=self.request.get('username')
        password=self.request.get('password')
        android=self.request.get('android')
        use = User.all().filter('username',username)
        self.session.delete(username)





app = webapp2.WSGIApplication([('/logout', MainHandler)], config=sessions_module.myconfig_dict, debug=True)