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
        This method handles the start tag of the scraper.
        """
        try: 
            if tag == "tr":
                self.inTr = True
            if tag == "td":
                self.inTd = True
                
            if tag == "th" and attrs[0][1] == "row":
                self.inDate = True
                # self.inTr = True
            
            if tag == "abbr" and self.inDate == True:
                self.date = attrs[0][1]

            if tag == "li" and len(attrs) > 1 and attrs[1][1] == "previous":
                self.has_link = True

            if tag == "a" and attrs[0][1] == "prev" and self.has_link == True:
                self.link = attrs[1][1]

            if tag == "li" and len(attrs) > 1 and attrs[1][1] == "previous disabled":
                self.has_link = False
        except Exception as error:
            logger.error("Error")
            
    def handle_endtag(self,tag):
        """
        This method handles the end tag of the scraper.
        """
        try: 
            if tag == "tr":
                self.inTr = False

                if self.date != "Average" and self.date != "Extreme":
                    if (len(self.date)) != 0:
                        date2 = self.date
                        # 2018-05-1
                        dateformat = datetime.strptime(date2, "%B %d, %Y").strftime("%Y-%m-%d")
                        self.date = dateformat

                        self.weather[self.date] = {
                            "Max": float(self.row[0]), 
                            "Min": float(self.row[1]), 
                            "Mean": float(self.row[2])
                            }
                        print("Working on " + self.date +"...")
                        # print("working on row " + self.row[0] +"...")
                    print(self.date)
            
                self.row = []

            elif tag == "td":
                self.inTd = False
            elif tag == "abbr":
                self.inDate = False

        except Exception as error:
            logger.error("Error")
            

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

