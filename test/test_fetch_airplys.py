import unittest
from hoerdatrecorder.fetch_airplays import Parser, Airplay

class TestParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "test/data/hoerdat_query_2015-02-01.html"
        self.parser = Parser()

    def test_beautify(self):
        self.assertEqual("a b c d", self.parser.beautify("  a   b c    d   "))

    def test_got_list(self):
        self.assertEqual(10, len(self.parser.fetch_airplays(self.test_file)))

    def test_convert_to_atf_format(self):
        self.assertEqual("07:05 01.02.2015", 
                         self.parser.convert_to_atd_format("  1. Feb 2015 07:05"))

    def test_retrieve_airplay_tables(self):
      tables = self.parser.retrieve_airplay_tables(self.test_file)
      self.assertEqual(10, len(tables))
    
    def test_make_transmission_info_list(self):
        tables = self.parser.retrieve_airplay_tables(self.test_file)

        list = self.parser.make_transmission_info_list(tables[0])
        self.assertTrue('MDR Figaro - Sonntag' in list)
        self.assertTrue(' 1. Feb 2015 07:05' in list)


    def test_choose_stream(self):
        streams = [{'title' : 'MDR Figaro-Realplayer-Stream',
                    'href' : 'http://reallink'},
                   {'title' : 'MDR Figaro-Windows Mediaplayer-Stream',
                    'href' : 'http://mediaplayerlink'},
                   {'title' : 'MDR Figaro-MP3-Stream',
                    'href' : 'http://mp3link'},
                   {'title' : 'MDR Figaro-Ogg Vorbis-Stream (hohe Qualität)',
                    'href' : 'http://ogglink_high'},
                   {'title' : 'MDR Figaro-Ogg Vorbis-Stream (mittlere Qualität)',
                    'href' : 'http://ogglink_low'}]

        self.assertEqual('http://mp3link', self.parser.choose_stream(streams))

        del streams[2] # remove MP3
        self.assertEqual('http://ogglink_high', self.parser.choose_stream(streams))

        del streams[2] # remove ogg high
        self.assertEqual('http://mediaplayerlink', self.parser.choose_stream(streams))
        del streams[1] # remove mediaplayer

        # default
        self.assertEqual('http://reallink', self.parser.choose_stream(streams))



    def test_first_airplay(self):
        airplay = self.parser.fetch_airplays(self.test_file)[0]
        self.assertEqual("Die haarsträubenden Abenteuer des Detektivs Dick Dickson 1: Jagd nach dem Niespulver", airplay.title)
        self.assertEqual("MDR Figaro", airplay.station)
        self.assertEqual('07:05 01.02.2015', airplay.date)
        self.assertEqual(55, airplay.length)

        expected = 'http://avw.mdr.de/livestreams/mdr_figaro_live_128.m3u'
        self.assertEqual(expected, airplay.url)

        self.assertEqual('Hans Pfeiffer', airplay.author)

        expected = 'DDR 1961 32 Min. (Mono) - Originalhörspiel dt.'
        self.assertEqual(expected, airplay.production)

        self.assertTrue('Kinderhörspiel' in airplay.genre)
        self.assertTrue('Krimi' in airplay.genre)
        self.assertTrue('Komödie' in airplay.genre)

        self.assertTrue('Der berühmte Privatdetektiv Dickson' in airplay.description)
        self.assertTrue('Polizei und der Gangster auf sich.' in airplay.description)
