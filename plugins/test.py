from plugin import Plugin
class Test(Plugin):
    def __init__(self):
        Plugin.__init__(self)
    def beforeInit(self, irc):
        print "Hello World... I'm a plugin"

