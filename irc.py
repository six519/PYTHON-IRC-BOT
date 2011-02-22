# This is my hello world code in python :)
import socket
import re
import time

class PYTHONIRC:

    __IrcServer = ""
    __IrcPort = "6667"
    __IrcNick = ""
    __IrcRoom = ""
    __socket = None
    __isConnected = False
    __isAuthenticated = False


    def __init__(self):
        self.__main()

    def __main(self):
        self.__IrcServer = self.__getUserInput("Please Enter Irc Server Address")

        if self.__getUserInput("Do you want to change the Irc Port? The default port is " + self.__IrcPort + ". Enter y to change") == "y":
            self.__IrcPort = self.__getUserInput("Please enter port number")

        self.__IrcNick = self.__getUserInput("Please enter Irc nick")
        self.__IrcRoom = self.__getUserInput("Please enter Irc channel")
        self.__connect()

    def __getUserInput(self,msg):


        while True:
            line = input("\n" + msg + ": ")

            if len(line.strip()) > 0:
                return line.strip()
                break;

    def __connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.__socket.connect((self.__IrcServer,int(self.__IrcPort)))
            self.__isConnected = True
            self.__receiveMessages()
            
        except (socket.gaierror,socket.error) as err:
            print("Connection error. The following error occur:",err)

            if self.__getUserInput("Restart application? Enter y to restart") == "y":
                self.__main()


    def __receiveMessages(self):
        while self.__isConnected == True:
            buffer = self.__socket.recv(1024)
            buffer = buffer.decode("utf-8")

            if buffer == "":
                self.__isConnected = False
                self.__isAuthenticated = False

            else:
                print(buffer)

                if re.search("Checking Ident",buffer) and not self.__isAuthenticated:
                    self.__sendMessage("NICK " + self.__IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.__IrcNick + " \"" + self.__IrcNick + ".com\" \"" + self.__IrcServer + "\" :" + self.__IrcNick + " robot\r\n")

                elif re.search("Nickname is already in use",buffer) and not self.__isAuthenticated:
                    self.__IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.__sendMessage("NICK " + self.__IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.__IrcNick + " \"" + self.__IrcNick + ".com\" \"" + self.__IrcServer + "\" :" + self.__IrcNick + " robot\r\n")
                elif re.search("Erroneous Nickname",buffer) and not self.__isAuthenticated:
                    self.__IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.__sendMessage("NICK " + self.__IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.__IrcNick + " \"" + self.__IrcNick + ".com\" \"" + self.__IrcServer + "\" :" + self.__IrcNick + " robot\r\n")                    
                elif re.search("This nickname is registered",buffer) and not self.__isAuthenticated:
                    self.__IrcNick = self.__getUserInput("Please enter new Irc nick")
                    self.__sendMessage("NICK " + self.__IrcNick + "\r\n")
                    self.__sendMessage("USER " + self.__IrcNick + " \"" + self.__IrcNick + ".com\" \"" + self.__IrcServer + "\" :" + self.__IrcNick + " robot\r\n")

                elif re.search("End of /MOTD command",buffer) and not self.__isAuthenticated:
                    self.__isAuthenticated = True
                    self.__sendMessage("JOIN #" + self.__IrcRoom + "\r\n")

                elif re.search("PING :",buffer):
                    self.__sendMessage(buffer.replace("PING","PONG"))

                elif re.search("PRIVMSG #" + self.__IrcRoom + " :",buffer):

                    #handle room message here
                    pass

                elif re.search("JOIN :#" + self.__IrcRoom,buffer):
                    #greet new user

                    tempStr = buffer.split(":")
                    tempStr = tempStr[1].split("!")
                    nick = tempStr[0]
                    
                    if self.__IrcNick != nick:
                        self.__sendMessage("PRIVMSG #" + self.__IrcRoom + " :Magandang " + self.__getMeridiem() + " sa iyo " + nick + "\r\n")
                        


    def __sendMessage(self,msg):
        self.__socket.send(msg.encode())
        
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

run = PYTHONIRC()
