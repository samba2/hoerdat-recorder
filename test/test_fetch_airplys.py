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
        expected = ['MDR Figaro - Sonntag', 
                '  1. Feb 2015 07:05', 
                ' (angekündigte Länge:    55:00)']

        self.assertEqual(expected, self.parser.make_transmission_info_list(tables[0]))
        

    def test_first_airplay(self):
        airplay = self.parser.fetch_airplays(self.test_file)[0]
        self.assertEqual("Die haarsträubenden Abenteuer des Detektivs Dick Dickson 1: Jagd nach dem Niespulver", airplay.title)
        self.assertEqual("MDR Figaro", airplay.station)
        self.assertEqual('07:05 01.02.2015', airplay.date)
        self.assertEqual(55, airplay.length)

