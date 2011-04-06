# This is my hello world code in python :)
import socket
import re
import time
from plugin import Plugin, IrcConfig


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
    # useful in plugins which defines their own
    # initializations
    doInit = True


    def __init__(self):
        #load the plugins
        self.plugins = [IrcConfig()]
        self.__main()

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
                    self.__sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")

                elif re.search("Nickname is already in use",buffer) and not self.isAuthenticated:
                    self.IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.__sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")
                elif re.search("Erroneous Nickname",buffer) and not self.isAuthenticated:
                    self.IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.__sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")                    
                elif re.search("This nickname is registered",buffer) and not self.isAuthenticated:
                    self.IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.__sendMessage("NICK " + self.IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.IrcNick + " \"" + self.IrcNick + ".com\" \"" + self.IrcServer + "\" :" + self.IrcNick + " robot\r\n")

                elif re.search("End of /MOTD command",buffer) and not self.isAuthenticated:
                    self.isAuthenticated = True
                    self.__sendMessage("JOIN #" + self.IrcRoom + "\r\n")

                elif re.search("PING :",buffer):
                    self.__sendMessage(buffer.replace("PING","PONG"))

                elif re.search("PRIVMSG #" + self.IrcRoom + " :",buffer):

                    #handle room message here
                    pass

                elif re.search("JOIN :#" + self.IrcRoom,buffer):
                    #greet new user

                    nick = self.__extractNick(buffer)
                    
                    if self.IrcNick != nick:
                        self.__sendMessage("PRIVMSG #" + self.IrcRoom + " :Magandang " + self.__getMeridiem() + " sa iyo " + nick + "\r\n")
                        


    def __sendMessage(self,msg):
        self.socket.send(msg.encode())
    
    def __extractNick(self,str):

        tempStr = str.split(":")
        tempStr = tempStr[1].split("!")
        return tempStr[0]    	  
			
        
    def __getMeridiem(self,**kwargs):

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
    def notifyPlugins (self, event):
        for p in self.plugins:
            p.beforeInit(self)
run = PYTHONIRC()
