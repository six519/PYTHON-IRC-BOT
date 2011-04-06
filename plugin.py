class Plugin:
    def __init__(self):
        pass
    def beforeInit(self, irc):
        pass
    def afterChannelJoin(self, irc):
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
