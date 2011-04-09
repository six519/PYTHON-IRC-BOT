from plugin import Plugin
import threading
import sys
class IrcConsole(Plugin,threading.Thread):
    irc = None
    done = False
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        self.message("--Starting Console----\n--You can send raw commands from this console")
        while not self.done:
            cmd = self.getUserInput()
            self.handleCommand(cmd)
    def getUserInput(self, default=""):
        sys.stdout.flush()
        line = raw_input(">>: ")
        if len(line.strip()) > 0:
            return line.strip()
        return default
    def message(self, msg):
        print ">>:", msg, "\n"
    def handleCommand(self, command):
        cmd = command.strip()
        if len(cmd) == 0:
            return
        if cmd == "exit":
            self.done = True
            return
        if (self.irc.isConnected):
            self.irc.sendMessage(cmd + "\r\n")
    
    def onRecv(self, irc, msg):
        msg = msg.strip()
        print "\r<<",msg
    def init(self, irc):
        # we can start here, but i choose to start when
        # we've already joined a channel
        self.irc = irc
        self.start()
    def shutdown(self, irc):
        self.done = True
        print "\nShutting console down..."
