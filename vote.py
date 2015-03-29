from google.appengine.ext import db
import time
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga
from model.Question import Question
from model.Vote import Vote

class MainHandler(sessions_module.BaseSessionHandler):

    #post:
    #jirga name
    #whether it is public or private
    def post(self):
        user = self.getuser()
        if(user is not None):

            questionKey = self.request.get('questionKey')
            jirgaKey = self.request.get('jirgaId')
            question = Question.all().filter('qId',questionKey).get()
            jirga = Jirga.all().filter('jirgaId',jirgaKey).get()
            voteNum = int(self.request.get('voteselect'))
            vote = True
            if (question is not None) and (jirga is not None)and (user.key() in jirga.members):
                for voter in question.voted:
                    if str(user.key()) == str(voter):
                        print("user:" + str(user.key()) + " voter:" + str(voter))
                        time.sleep(1)
                        self.redirect("/viewResults/"+jirga.jirgaId+"/"+question.qId)
                        vote = False

                if(vote):
                    for v in question.votes:
                        vc = Vote.get(v)
                        print(vc.number)
                        if vc.number == voteNum:
                            vc.users.append(user.key())
                            vc.count += 1
                            vc.put()
                            question.voted.append(user.key())
                            question.put()
                            time.sleep(1)
                            self.redirect("/viewResults/"+jirga.jirgaId+"/"+question.qId)
            else:
                self.redirect("/viewResults/"+jirga.jirgaId+"/"+question.qId)
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/vote', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
