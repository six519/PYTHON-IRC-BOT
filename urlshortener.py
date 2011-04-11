import urllib2
import threading
import json
class GoogleShortener(threading.Thread):
    longurl = ""
    callback = None
    args = None
    def __init__(self):
        threading.Thread.__init__(self)
    def shorten_and_do(self, longurl, callback, *args):
        self.longurl = longurl
        self.callback = callback
        self.args = args
        self.start()
    def run(self):
        s = self.shorten(self.longurl)
        self.callback(s, *self.args)
    def shorten(self, longurl):
        service_url = 'https://www.googleapis.com/urlshortener/v1/url'
        data = '{"longUrl": "%s"}' % (longurl,)
        headers = {'Content-type': 'application/json'}

        req = urllib2.Request(service_url, data, headers)
        resp = urllib2.urlopen(req)
        doc = resp.read()
        v = json.loads(doc)
        return v['id']
