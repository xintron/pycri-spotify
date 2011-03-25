# -*- coding: utf-8 -*-
import re, urllib2, time
import json

from pycri.plugins import Plugin

class Spotify(Plugin):

    apiurl = "http://ws.spotify.com/lookup/"
    apiversion = '1'

    regexp = re.compile('(http://open\.spotify\.com/|spotify:)(album|artist|track)[:/]([^\s$]+)', re.I)

    def on_privmsg(self, irc, prefix, params):
        msg = params[-1]
        m = self.match_uri(msg)

        if not m:
            return

        channel = params[0]

        type = m.group(2).lower()
        uri = 'spotify:{}:{}'.format(type, m.group(3))
        data = json.loads(self.call(uri))

        ret = self.format_response(data, type)

        irc.msg(channel, ret)
        return

    def format_response(self, data, type='track'):

        if type == 'artist':
            return u"» {0} » {1}".format(data['artist']['name'], data['artist']['href'])
        elif type == 'album':
            return u"» {0} [{1}] » {2}".format(data['album']['artist'], data['album']['name'], data['album']['href'])
        else:
            return u"» {0} - {1} [{2}] ({3}) » {4}".format(
                data['track']['artists'][0]['name'],
                data['track']['name'],
                data['track']['album']['name'],
                self.timeconversion(float(data['track']['length'])),
                data['track']['href']
            )

    def timeconversion(self, seconds):
        format = '%H:%M:%S'
        if seconds < 3600:
            format = format[3:]
        return time.strftime(format, time.gmtime(seconds))

    def match_uri(self, msg):
       return self.regexp.search(msg) 
        
        

    def call(self, uri):
        url = ''.join([self.apiurl, self.apiversion, '/?uri=', uri])
        req = urllib2.Request(url, headers={'Accept': 'application/json'})
        data = urllib2.urlopen(req).read()

        return data
