from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
from model.Jirga import Jirga
import sessions_module
from model.User import User,Session
import uuid

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self,jirgaId):
        loggedIn= False
        user = self.getuser()
        if(user is not None):
            jirga = Jirga.all().filter('jirgaId', jirgaId).get()
            public = jirga.publicJirga
            if(public == 0):
                #private jirga
                template_params = {
                    'public':public,
                }
            else:
                #public
                if(user in jirga.members):
                    #user is a member
                    member = 1
                else:
                    #user is not a member
                    member = 0
                template_params = {
                    'public':public,
                    'member':member
                }
            member = User.get(jirga.members)
            obj2={'members':member}
            template_params.update(obj2)
            template_params.update({'user':user})
            template_params.update({'jirga':jirga})
            render_template(self,"jirgaSettings.html",template_params)
        else:
            self.response.write("FAIL - you need to be logged in for this")
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
        else:
            #no user found/something went wrong
            loginError = True
            template_params={
                'loggedIn': loggedIn,
                'loginError': loginError,
            }
            render_template(self,'login.html',template_params)



app = webapp2.WSGIApplication([('/jirgaSettings/(.*?)', MainHandler)], config=sessions_module.myconfig_dict, debug=True)