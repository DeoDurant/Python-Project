"""
Weather Scraper
Group Members: Calvin Anglo, Choie Llamas
Project Milestone: 1
Created: 2022-11-24
Updated: 2022-11-24
"""
from html.parser import HTMLParser
import urllib.request
from datetime import datetime
import logging


class WeatherScraper(HTMLParser):
    def __init__(self):
        try:
            HTMLParser.__init__(self)
            self.inTBody = False
            self.inTr = False
            self.inDate = False
            self.inTd = False
            self.inabbr = False
            self.date = ""
            self.row = []
            self.weather = {}
            self.has_link = True
            self.link = ""
        except Exception as error:
            logger.error("Error")
        
    def handle_starttag(self, tag, attrs):
        """
        
        """
        if tag.__eq__('tbody'):
            self.tbody = True
        if tag.__eq__('tr'):
            self.tr = True
        if tag.__eq__('td'):
            if(self.count_td <= 3):
                self.td = True
            else:
                self.td = False
            
    def handle_endtag(self, tag):
        """
        
        """
        if tag.__eq__('tbody'):
            self.tbody = False
        if tag.__eq__('tr'):
            self.tr = False
        if tag.__eq__('td'):
            self.td = False
            

    def handle_data(self, data):
        if self.tbody and self.tr and self.td:
            self.count_td += 1
            if self.count_td == 1:
                self.daily_temps.update({"max": data})
            elif self.count_td == 2:
                self.daily_temps.update({"min": data})
            elif self.count_td == 3:
                self.daily_temps.update({"mean": data})
                self.count_td = 0
                
            # if self.count_td == 1:
            #     self.daily_temps.update({"max": data})
            # elif self.count_td == 2:
            #     self.daily_temps.update({"min": data})
            # elif self.count_td == 3:
            #     self.daily_temps.update({"mean": data})
            
        print(self.daily_temps)
            
        # 
        #     self.daily_temps.update({"max": data})
        #     self.daily_temps.update({"min": data})
        #     self.daily_temps.update({"mean": data})
            

logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

