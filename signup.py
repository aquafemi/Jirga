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

class signUpHandler(sessions_module.BaseSessionHandler):

    def get(self):
        #TODO handle case in which logged in user tries to create a user
        template_params={}
        render_template(self,'createUser.html',template_params)
    #post to create account will receive:
    #username="username"
    #password="password"
    #should give user success/failure
    def post(self):
        success = False
        template_params={}
        username=self.request.get('username')
        password=self.request.get('password')
        android=self.request.get('android')
        use = User.all().filter('username',username)
        if use.count() == 0:
            #no collisions
            nameTaken = False
            if (password is not None) and (password != ""):
                #valid password
                badPass = False
                #create user account
                usernew = User(username=username,password=password)
                usernew.put()
                success=True
                template_params={'success':success}
            else:
                #invalid password
                badPass = True
                template_params={'success':success,'badPass':badPass}
            if android is not None and (android)==1:
                if(badPass):
                    self.response.write("FAIL-BADPASS");
                else:
                    self.response.write("OK");
            else:
                render_template(self,'createUser.html',template_params)
        else:
            if android is not None and (android)==1:
                self.response.write("FAIL-BADNAME");
            else:
                #username taken
                nameTaken = True
                template_params={'success':success,'nameTaken':nameTaken}
                render_template(self,'createUser.html',template_params)



app = webapp2.WSGIApplication([('/createUser', signUpHandler)], config=sessions_module.myconfig_dict, debug=True)