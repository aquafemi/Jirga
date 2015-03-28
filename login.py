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
        loggedIn= False
        if self.session.get('user'):
            loggedIn= True
            user = str(self.session.get('user'))
            template_params={
                'loggedIn': loggedIn,
                'user': user
            }
            render_template(self,'login.html',template_params)
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
            self.session['user']= user
            self.redirect('/login')
        else:
            #no user found/something went wrong
            self.redirect('/login')
            template_params={
                'loggedIn': loggedIn,
                'loginError': True
            }
            render_template(self,'login.html',template_params)



app = webapp2.WSGIApplication([('/login', MainHandler)], config=sessions_module.myconfig_dict, debug=True)