from plugin import Plugin
class IrcConfig(Plugin):
    def __init__(self):
        Plugin.__init__(self)
    def beforeInit(self, irc):
        irc.IrcNick     = self.getConfig('IrcConfig', 'nick')
        irc.IrcServer   = self.getConfig('IrcConfig', 'server')
        irc.IrcRoom     = self.getConfig('IrcConfig', 'channel')
        irc.IrcPort     = self.getConfig('IrcConfig', 'port')
        irc.doInit      = False
