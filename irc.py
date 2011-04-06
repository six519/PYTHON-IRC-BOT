# @todo automate sending alternate nick
import socket
import re
from plugin import Plugin, IrcConfig, IrcGreeter

class PYTHONIRC:

    IrcServer = ""
    IrcPort = "6667"
    IrcNick = ""
    IrcRoom = ""
    socket = None
    isConnected = False
    isAuthenticated = False
    plugins = []

    # marks whether we can skip initialization
    # eg setting server/nick/channel
    # useful for plugins which defines their own
    # initializations
    doInit = True


    def __init__(self):
        try:
            #load the plugins
            self.plugins = [IrcConfig(), IrcGreeter()]
            self.__main()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        #do shutdown fn here
        print "Shutting down"
    def __main(self):
        self.notifyPlugins("beforeInit");
        if self.doInit :
            self.IrcServer = self.__getUserInput("Please Enter Irc Server Address")

            if self.__getUserInput("Do you want to change the Irc Port? The default port is " + self.IrcPort + ". Enter y to change") == "y":
                self.IrcPort = self.__getUserInput("Please enter port number", "6667")

            self.IrcNick = self.__getUserInput("Please enter Irc nick")
            self.IrcRoom = self.__getUserInput("Please enter Irc channel")
        self.__connect()

    def __getUserInput(self,msg, default=""):
        line = raw_input(msg + ": ")
        if len(line.strip()) > 0:
            return line.strip()
        return default
    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((self.IrcServer,int(self.IrcPort)))
            self.isConnected = True
            self.__receiveMessages()
            
        except (socket.gaierror,socket.error) as err:
            print("Connection error. The following error occured:",err)

            if self.__getUserInput("Restart application? Enter y to restart") == "y":
                self.__main()


    def __receiveMessages(self):
        while self.isConnected == True:
            buffer = self.socket.recv(1024)
            buffer = buffer.decode("utf-8")

            if buffer == "":
                self.isConnected = False
                self.isAuthenticated = False

            else:
                print(buffer)

                if re.search("Checking Ident",buffer) and not self.isAuthenticated:
                    self.sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")

                elif re.search("Nickname is already in use",buffer) and not self.isAuthenticated:
                    self.IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")
                elif re.search("Erroneous Nickname",buffer) and not self.isAuthenticated:
                    self.IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")                    
                elif re.search("This nickname is registered",buffer) and not self.isAuthenticated:
                    self.IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")

                elif re.search("End of /MOTD command",buffer) and not self.isAuthenticated:
                    self.isAuthenticated = True
                    self.sendMessage("JOIN #" + self.IrcRoom + "\r\n")

                elif re.search("PING :",buffer):
                    self.sendMessage(buffer.replace("PING","PONG"))

                elif re.search("PRIVMSG #" + self.IrcRoom + " :",buffer):
                    nick = self.__extractNick(buffer)
                    self.notifyPlugins("onPriv", self.IrcRoom, nick, buffer)
                elif re.search("JOIN :#" + self.IrcRoom,buffer):
                    nick = self.__extractNick(buffer)
                    self.notifyPlugins("onJoin", self.IrcRoom, nick, buffer)

    def sendMessage(self,msg):
        self.socket.send(msg.encode())
    
    def __extractNick(self,str):

        tempStr = str.split(":")
        tempStr = tempStr[1].split("!")
        return tempStr[0]    	  
			
    def notifyPlugins (self, event, *args):
        for p in self.plugins:
            getattr(p, event)(self, *args)
run = PYTHONIRC()
