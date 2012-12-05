# -*- coding: utf-8 -*-
"""
Copyright (c) 2011, Marcus Carlsson <carlsson.marcus@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided
with the distribution.
* Neither the name of the author nor the names of other
contributors may be used to endorse or promote products derived
from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import re
import urllib2
import time
import json

from pycri.plugins import IRCObject
from pycri.globals import g

class Spotify(IRCObject):

    logger = g.getLogger(__name__)
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
        self.logger.debug('Fetching spotify data for: {}'.format(uri))
        data = json.loads(self.call(uri))

        ret = self.format_response(data, type)

        irc.msg(channel, ret)
        return

    def format_response(self, data, type='track'):

        if type == 'artist':
            ret = u"» {0} » {1}".format(data['artist']['name'], data['artist']['href'])
        elif type == 'album':
            ret = u"» {0} [{1}] » {2}".format(data['album']['artist'], data['album']['name'], data['album']['href'])
        else:
            ret = u"» {0} - {1} [{2}] ({3}) » {4}".format(
                data['track']['artists'][0]['name'],
                data['track']['name'],
                data['track']['album']['name'],
                self.timeconversion(float(data['track']['length'])),
                data['track']['href']
            )
        return ret.encode('utf8')

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
