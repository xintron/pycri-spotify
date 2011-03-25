# -*- coding: utf-8 -*-
import unittest, json

import spotify

class SpotifyTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = spotify.Spotify()

    def test_call(self):
        data = self.spotify.call('spotify:track:4saID1prQzHStGA6Sa0WSN')
        self.assertRegexpMatches(data, '"released": "2011", "href": "spotify:album:3Tm6OMfXk7PffAEt4NAkmX",')

    def test_regexp_match(self):
        uris = [
            (True, 'http://open.spotify.com/track/7MtlCWAvmQ7GQvuNjsGTqh'),
            (True, 'Foo bar spotify:tRack:1yw1rRHBsdJwT3kas9MmHf'), # Test case-sensitive
            (True, 'bar spotify:track:1yw1rRHBsdJwT3kas9MmHf foosie!'),
            (False, 'https://open.spotify.com/track/7MtlCWAvmQ7GQvuNjsGTqh'),
        ]

        for test, uri in uris:
            resp = self.spotify.match_uri(uri)
            if not test:
                self.assertIsNone(resp)
            else:
                self.assertIsNotNone(resp)

    def test_artis_lookupt(self):
        data = json.loads('{"info": {"type": "artist"}, "artist": {"href": "spotify:artist:0oeUpvxWsC8bWS6SnpU8b9", "name": "The Naked And Famous"}}')
        resp = self.spotify.format_response(data, type='artist')

        self.assertEquals(u'» The Naked And Famous » spotify:artist:0oeUpvxWsC8bWS6SnpU8b9', resp)

    def test_albu_lookupm(self):
        data = json.loads('{"album": {"artist-id": "spotify:artist:2tZy2pOIM0NmloMzN1YmLa", "name": "The Morning After", "artist": "Strobelight", "external-ids": [{"type": "upc", "id": "859705393791"}], "released": "2011", "href": "spotify:album:6QdPTJl9FwijKElfxhVf40", "availability": {"territories": "AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IN IO IQ IR IS IT JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW"}}, "info": {"type": "album"}}')
        resp = self.spotify.format_response(data, type='album')

        self.assertEquals(u'» Strobelight [The Morning After] » spotify:album:6QdPTJl9FwijKElfxhVf40', resp)

    def test_track_lookup(self):
        data = json.loads('{"track": {"available": true, "album": {"released": "2010", "href": "spotify:album:3fn7GwMqZAfYLYpvZlcSCA", "name": "K\u00e4rlek I Paket - Single"}, "track-number": "1", "popularity": "0.55910", "external-ids": [{"type": "isrc", "id": "SEYTG1000101"}], "length": 218.027, "href": "spotify:track:72tmEm4EzNBf38Rv883Mth", "artists": [{"href": "spotify:artist:74iM7YzbT8YWnFFRPwMBXM", "name": "Babian"}], "availability": {"territories": "AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IN IO IQ IR IS IT JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW"}, "name": "K\u00e4rlek I Paket"}, "info": {"type": "track"}}')
        resp = self.spotify.format_response(data)

        self.assertEquals(u'» Babian - Kärlek I Paket [Kärlek I Paket - Single] (03:38) » spotify:track:72tmEm4EzNBf38Rv883Mth', resp)

