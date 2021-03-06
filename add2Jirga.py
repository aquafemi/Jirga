from google.appengine.ext import db
import time
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga

class MainHandler(sessions_module.BaseSessionHandler):

    #post:
    #jirga ID
    #user name to add
    def post(self):
        user = self.getuser()
        if(user is not None):
            #check if user has permission to add target user to jirga
            #user can add if owner of private jirga
            #user can add if adding self to public jirga
            targetJirga = self.request.get('jirga')
            targetJ = Jirga.all().filter('jirgaId',targetJirga).get()
            if(targetJ is not None):
                #jirga was found
                targetUser = self.request.get('user')
                targetU = User.all().filter('username',targetUser).get()
                if targetU is not None and targetU.key() not in targetJ.members:
                    print(targetU.key)
                    #user was found
                    if(targetJ.publicJirga == 0) and (targetJ.owner == user.username):
                        #private jirga but user owns it
                        flag = True;
                        for key in targetU.jirgas:
                            if key == targetJ.key:
                                print(key() + "    -     " + targetJ.key())
                                flag = False
                        if flag:
                            targetU.jirgas.append(targetJ.key())
                        targetJ.members.append(targetU.key())
                        targetJ.put()
                        targetU.put()
                        #todo get rid of these time.sleeps start having better data routes
                        time.sleep(1)
                        self.redirect("/jirgaSettings/"+targetJ.jirgaId)
                    elif(targetJ.publicJirga == 1) and (targetU.username == user.username):
                        #public jirga, user is adding self
                        user.jirgas.append(targetJ.key())
                        targetJ.members.append(targetU.key())
                        user.put()
                        targetJ.put()
                        time.sleep(1)
                        self.redirect("/jirgaSettings/"+targetJ.jirgaId)
                    else:
                        #insufficient permissions
                        self.response.write("FAIL - insufficient permissions")
                else:
                   #user was not found
                    self.redirect("/jirgaSettings/"+targetJ.jirgaId)
            else:
                #jirga was found
                self.response.write("FAIL - invalid jirga")
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/add2Jirga', MainHandler)], config=sessions_module.myconfig_dict, debug=True)