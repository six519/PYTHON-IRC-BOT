#Greeter needs the time module
import time
class Plugin:
    def __init__(self):
        pass
    def beforeInit(self, irc):
        pass
    def afterChannelJoin(self, irc):
        pass
    def onJoin(self, irc, channel, nick, msg):
        pass
    def onPriv(self, irc, channel, nick, msg):
        pass

class IrcConfig(Plugin):
    def __init__(self):
        Plugin.__init__(self)
    def beforeInit(self, irc):
        irc.IrcServer = "irc.freenode.net"
        irc.IrcPort   = "6667"
        irc.IrcRoom   = "phpugph"
        irc.IrcNick   = "modifiedBot"
        irc.doInit    = False

class IrcGreeter(Plugin):
    def __init__(self):
        Plugin.__init__(self)

    def onJoin(self, irc, channel, nick, msg):
        if irc.IrcNick != nick :
            irc.sendMessage("PRIVMSG #" + channel + " :Magandang " + self.getMeridiem() + " sa iyo " + nick + "\r\n")
    def getMeridiem(self,**kwargs):
        nowTime = time.localtime()

        try:
            nowTime = time.localtime(time.time() + (kwargs['HoursToAdd'] * 3600))
        except KeyError:
            pass
        
        try:
            nowTime = time.localtime(time.time() - (kwargs['HoursToSub'] * 3600))
        except KeyError:
            pass

        if nowTime.tm_hour == 0:
            return "hatinggabi"
        elif nowTime.tm_hour >= 1 and nowTime.tm_hour <=5:
            return "madaling araw"
        elif nowTime.tm_hour >=6 and nowTime.tm_hour <= 11:
            return "umaga"
        elif nowTime.tm_hour == 12:
            return "tanghali"
        elif nowTime.tm_hour >= 13 and nowTime.tm_hour <= 17:
            return "hapon"
        elif nowTime.tm_hour >= 18 and nowTime.tm_hour <= 23:
            return "gabi"
