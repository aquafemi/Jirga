from google.appengine.ext import db
import webapp2
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga, ModVote
from model.Question import Question
from model.Vote import Vote

class MainHandler(sessions_module.BaseSessionHandler):

    def post(self):
        user = self.getuser()
        if(user is not None):
            questionKey = self.request.get('questionId')
            jirgaKey = self.request.get('jirga')
            voteNum = int(self.request.get('voteNum'))
            question = Question.all().filter('qId',questionKey).get()
            jirga = Jirga.all().filter('jirgaId',jirgaKey).get()
            if (question is not None) and (jirga is not None)and (user.username == question.author):
                for v in question.votes:
                        vc = Vote.get(v)
                        if vc.number == voteNum:
                            voters = User.get(vc.users)
                            modVotes = ModVote.get(jirga.modVotes)
                            for voter in voters:
                                for modVote in modVotes:
                                    print(modVote.user)
                                    print(voter.username)
                                    if(voter.username == modVote.user):
                                        modVote.reward += 1
                                        modVote.put()
                                        self.redirect("/viewResults/"+jirga.jirgaId+"/"+question.qId)
            else:
                self.redirect("/viewResults/"+jirga.jirgaId+"/"+question.qId)
        else:
            self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/chooseWinner', MainHandler)], config=sessions_module.myconfig_dict, debug=True)