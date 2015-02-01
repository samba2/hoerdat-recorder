#!/usr/bin/python3

from bs4 import BeautifulSoup
import re
import datetime

class Parser():

    def fetch_airplays(self, file_name):
    
        airplays = []
        for table in self.retrieve_airplay_tables(file_name):
            airplay = Airplay()
            airplay.title = self.find_title(table)
  
            info_list = self.make_transmission_info_list(table)
            airplay.station = self.find_station(info_list)
            airplay.date = self.find_date(info_list)
            airplay.length = self.find_length(table)
            airplay.url = self.find_url(table)
            airplay.author = self.find_right_column(table, 'Autor(en):')
            airplay.production = self.find_right_column(table, 'Produktion:')
            airplay.genre = self.find_genre(table)
            airplay.description = self.find_right_column(table, 'Inhaltsangabe:')

            airplays.append(airplay)
    
        return airplays


    def retrieve_airplay_tables(self, file_name):

        # the tables containing the data are the ones without a css class
        def filter_airplay_tables(tag):
            return tag.name == "table" and not tag.has_attr('class')
    
        with open(file_name, encoding="iso-8859-1") as file_handle:
            soup = BeautifulSoup(file_handle)
        
        return soup.find_all(filter_airplay_tables)


    def find_right_column(self, table, search_string):
        def match_left_column(tag):
            return tag.name == "tr" and tag.td and tag.td.text == search_string

        right_column = table.find_all(match_left_column)
        if not right_column:
            return None
                        
        cell = right_column[0].find_all('td')[1].text

        return self.beautify(cell)
    

    def make_transmission_info_list(self, table):
        cell = self.find_right_column(table, 'Sendetermine:')
        return cell.strip().split(',')


    def find_title(self, table):
        return self.beautify(table.find_all("th")[0].text)


    def find_station(self, info_list):
        return info_list[0].split('-')[0].strip()

    
    def find_date(self, info_list):
        return self.convert_to_atd_format(info_list[1])


    def find_length(self, table):
        result = re.search(r"angekündigte Länge:\s+(\d{1,2}):\d\d", self.find_right_column(table, 'Sendetermine:'))

        if result is None:
            return 0

        return int(result.group(1))


    # create list of streams containing title and href, return the prevered one
    def find_url(self, table):
        stream_links = table.find_all("div", class_="streams")[0].find_all("a")

        streams = []
        for link in stream_links:
                streams.append(link.attrs)

        return self.choose_stream(streams)


    def find_genre(self, table):
        genre_text = self.find_right_column(table, 'Genre(s):')

        if genre_text is None:
            return genre_text

        return genre_text.split(' ')


    def convert_to_atd_format(self, raw_date_string):
        month_name_to_number = { 
                'Jan' : 1, 'Feb' : 2, 'Mär' : 3, 'Apr' : 4, 'Mai' : 5, 
                'Jun' : 6, 'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Okt' : 10, 
                'Nov' : 11, 'Dez' : 12 }

        date_elements = re.sub('\.', '', raw_date_string).strip().split(' ')
        time = date_elements[3].split(':')

        date = datetime.datetime(int(date_elements[2]), 
                                 int(month_name_to_number[date_elements[1]]), 
                                 int(date_elements[0]), 
                                 int(time[0]), 
                                 int(time[1]))

        return date.strftime("%H:%M %d.%m.%Y")


    def choose_stream(self, streams):

        def find_stream(search_string):
            for stream in streams:
                if search_string in stream['title']:
                    return stream['href']

            return None

        url = find_stream("MP3")
        if url is not None:
            return url

        url = find_stream("Ogg Vorbis-Stream (hohe Qualität)")
        if url is not None:
            return url
        
        url = find_stream("Mediaplayer")
        if url is not None:
            return url

        return streams[0]['href']


    def beautify(self, text):
        text = text.strip()
        text = re.sub(' +', ' ', text)
    
        return text


class Airplay():
    def __init__(self):
        self.title = None
        self.station = None
        self.date = None
        self.length = None
        self.url = None
        self.author = None
        self.production = None
        self.genre = []
        self.description = None
