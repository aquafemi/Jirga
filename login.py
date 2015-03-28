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
        android=self.request.get('android')
        use = User.all().filter('username',username)
        if use.count() == 1:
            #user found
            user = use.get()
            if(user.password == password):
                i = uuid.uuid1()
                sess = Session(user=user.username,sessId=str(i))
                sess.put()
                self.session['sessId']=str(i)
                badPass = False
                loggedIn = True
                template_params={'loggedIn':loggedIn,
                                'user': user.username}
                render_template(self,'login.html',template_params)
            else:
                #no user found/something went wrong
                loginError = True
                template_params={
                    'loggedIn': loggedIn,
                    'loginError': loginError,
                }
                render_template(self,'login.html',template_params)

            if android is not None and (android)==1:
                if(badPass):
                    self.response.write("FAIL-BADPASS")
                if(loginError):
                    self.response.write("FAIL-LOGINERROR")
                else:
                    self.response.write("OK")
            else:
                self.redirect("/")

        else:
            if android is not None and (android)==1:
                self.response.write("FAIL-BADNAME")
            else:
                #no user found/something went wrong
                loginError = True
                template_params={
                    'loggedIn': loggedIn,
                    'loginError': loginError,
                }
                render_template(self,'login.html',template_params)



app = webapp2.WSGIApplication([('/login', MainHandler)], config=sessions_module.myconfig_dict, debug=True)