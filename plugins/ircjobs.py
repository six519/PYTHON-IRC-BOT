import urllib
from HTMLParser import HTMLParser
from urlshortener import GoogleShortener
import re
from plugin import Plugin

class JobsDbParser(HTMLParser):
    latest = []
    current = {}
    is_job = False
    def __init__(self):
        self.latest = []
        self.current = {'link': '', 'title': ''}
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and attrs:
            name,link = attrs[0]
            if re.search(r"bt-jobd", link):
                self.current['link'] = 'http://bestjobs.ph/' + link
                self.is_job = True
            
    #print link
    def handle_data(self,data):
        if self.is_job:
            self.current['title'] = self.current['title'] + data.strip()
            
    def handle_endtag(self, tag):
        if tag == 'a' and self.is_job:
            self.is_job = False
            self.current = {'link': '', 'title': ''}
            self.latest.append(self.current)
        pass

class IrcJobs(Plugin):
    def __init__(self):
        pass
    def onPriv(self, irc, channel, nick, msg):
        #start parsing
        msg = irc.extractMsg(msg)
        if msg != '!jobs':
            return
        url = "http://bestjobs.ph/bt-joblist.htm?Bqd=&Bqd=%2BSC003&Bqd=%2BTM003&BqdPalabras=freelance+php&x=14&y=14"
        data = {}
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"}
        resp = urllib.urlopen(url)
        doc = resp.read()
        p = JobsDbParser()
        p.feed(doc)
        
        for i in p.latest:
            s = GoogleShortener()
            s.shorten_and_do(i['link'], self.pretty_print, i, channel, irc)
        
    def pretty_print(self, url, obj, channel, irc):
        cmd = "PRIVMSG #%s :%s [ %s ]\r\n" % (channel, obj['title'], url)
        irc.sendMessage(cmd, False)
        
