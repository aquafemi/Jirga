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
        loggedIn= False
        username=self.request.get('username')
        password=self.request.get('password')
        use = User.all().filter('username',username)
        if use.count() == 1:
            #user found
            user = use.get()
            if(user.password == password):
                i = uuid.uuid1()
                sess = Session(user=user.username,sessId=str(i))
                sess.put()
                self.session['sessId']=str(i)
                loggedIn = True
                template_params={'loggedIn':loggedIn}
                render_template(self,'login.html',template_params)
            else:
                #no user found/something went wrong
                loginError = True
                template_params={
                    'loggedIn': loggedIn,
                    'loginError': loginError,
                }
                render_template(self,'login.html',template_params)
        else:
            #no user found/something went wrong
            loginError = True
            template_params={
                'loggedIn': loggedIn,
                'loginError': loginError,
            }
            render_template(self,'login.html',template_params)



app = webapp2.WSGIApplication([('/login', MainHandler)], config=sessions_module.myconfig_dict, debug=True)