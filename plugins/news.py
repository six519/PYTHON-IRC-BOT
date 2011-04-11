from plugin import Plugin
from HTMLParser import HTMLParser
import urllib2
from urllib2 import urlopen,Request,build_opener,HTTPCookieProcessor,install_opener
from urllib import urlencode
from cookielib import LWPCookieJar
from urlshortener import GoogleShortener
import re

class PhpugphParser(HTMLParser):
    latest = []
    current = {}
    is_post = False
    is_profile = False
    def __init__(self):
        self.latest = []
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and attrs:
            name,link = attrs[0]
            if re.search(r"topicseen", link):
                self.current['link'] = link
                self.is_post = True
            if re.search(r"profile", link):
                self.is_profile = True
        if tag == 'img':
                self.is_post = False
            
    #print link
    def handle_data(self,data):
        if self.is_post:
            self.current['topic'] = data.strip()
            self.is_post = False
        if self.is_profile:
            self.is_profile = False
            self.current['by'] = data.strip()
            self.latest.append(self.current)
            self.current = {}
    def handle_endtag(self, tag):
        pass


class News(Plugin):
    def __init__(self):
        Plugin.__init__(self)
    def printLatest(self, channel, irc):
        user = self.getConfig('News', 'username')
        passwd = self.getConfig('News', 'password')
        cookie = 'cookie.jar'
        
        #login and parse the latest post
        parser = PhpugphParser()
        
        cookieJar = LWPCookieJar()
        opener = build_opener(HTTPCookieProcessor(cookieJar))
        install_opener(opener)
        data = urlencode({"user":user,"passwrd":passwd})

        f = urlopen("http://www.phpugph.com/talk/index.php?action=login2",data)
        cookieJar.save(cookie)
        f.close()
        
        cookieJar.load(cookie)
        f = urlopen("http://www.phpugph.com/talk/SSI.php?ssi_function=recentTopics")
        parser.feed(f.read().decode('utf-8','replace'))
        parser.close()
        f.close()
        
        lines = []
        latest = parser.latest
        for l in latest:
            g = GoogleShortener()
            g.shorten_and_do(l['link'], self.pretty_print, l, channel, irc)
        
    def pretty_print(self, url, obj, channel, irc):
        cmd = "PRIVMSG #%s :%s (%s) - [ %s ]\r\n" % (channel, obj['topic'], obj['by'], url)
        irc.sendMessage(cmd, False)
    def onPriv(self, irc, channel, nick, msg):
        msg = irc.extractMsg(msg)
        if msg != "!news":
            return
        str = self.printLatest(channel, irc)
