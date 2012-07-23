from plugin import Plugin
import time
class IrcGreeter(Plugin):
    def __init__(self):
        Plugin.__init__(self)
    def onJoin(self, irc, channel, nick, msg):
        # this is the bot joining
        if irc.IrcNick == nick :
           return
        #cowgreet?
        gmt_offset = int(self.getConfig('IrcGreeter', 'gmt_offset'))
        msg = "Magandang %s sa iyo %s" % (self.getMeridiem(HoursToAdd=gmt_offset), nick)
        msgs = []
        do_cowgreet = self.getConfigBoolean('IrcGreeter', 'cowgreet')

        if do_cowgreet:
            for i in irc.plugins:
                if i.__class__.__name__ == 'IrcCow':
                    msgs = i.do('cowsay', msg)

        else:
            msgs.append(msg)

        for i in msgs:
            irc.sendMessage("PRIVMSG #%s :%s\r\n" %(channel, i))
    def getMeridiem(self,**kwargs):
        nowTime = time.localtime()

        try:
            nowTime = time.localtime(time.time() + (kwargs['HoursToAdd'] * 3600))
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
