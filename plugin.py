import ConfigParser
import re

class Plugin:
    conf = None
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
    def configure(self, irc, conf):
        cp = ConfigParser.SafeConfigParser();
        try:
            fp = open(conf)
        except IOError:
            return False
        cp.readfp(fp)
        self.conf = cp
        return True
    def getConfig(self, section, cfg = None):
        try:
            if cfg == None:
                return self.conf.items(section)
            return self.conf.get(section, cfg)
        except ConfigParser.NoSectionError:
            return None
    def setConfig(self, cfg):
        self.conf = cfg
    def shutDown(self, irc):
        pass
