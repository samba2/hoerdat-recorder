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

            airplays.append(airplay)
    
        return airplays


    def retrieve_airplay_tables(self, file_name):

        # the tables containing the data are the ones without a css class
        def filter_airplay_tables(tag):
            return tag.name == "table" and not tag.has_attr('class')
    
        with open(file_name, encoding="iso-8859-1") as file_handle:
            soup = BeautifulSoup(file_handle)
        
        return soup.find_all(filter_airplay_tables)


    def make_transmission_info_list(self, table):
        return self.make_info_string(table).strip().split(',')


    def make_info_string(self, table):
        def filter_transmission_info(tag):
            return tag.name == "tr" and tag.td and tag.td.text == 'Sendetermine:'

        return table.find_all(filter_transmission_info)[0].find_all('td')[1].contents[0]

    
    def find_title(self, table):
        return self.beautify(table.find_all("th")[0].text)

    
    def find_station(self, info_list):
        return info_list[0].split('-')[0].strip()

    
    def find_date(self, info_list):
        return self.convert_to_atd_format(info_list[1])


    def find_length(self, table):
        result = re.search(r"angekündigte Länge:\s+(\d{1,2}):\d\d", self.make_info_string(table))

        if result is None:
            return 0

        return int(result.group(1))


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
