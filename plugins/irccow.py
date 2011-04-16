import subprocess
import re
from plugin import Plugin
class IrcCow(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        pass
    def do(self, type, msg):
        #remove  possible commandline arguments
        msg = re.sub(r"-.", "", msg)
        p = subprocess.Popen([type, msg], stdout=subprocess.PIPE)
        out,err = p.communicate()
        return out.split("\n")
    def onPriv(self, irc, channel, nick, msg):
        msg = irc.extractMsg(msg).strip()
        match = re.match(r"^!(cowsay|cowthink)\s(.*)", msg)
        if(match is None):
            return 
        type,msg = match.groups()
        str = self.do(type, msg)
    
        for s in str:
            cmd = "PRIVMSG #%s :%s\r\n" % (channel, s)
            print cmd
            irc.sendMessage(cmd)

