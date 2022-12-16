"""
Weather Scraper
Group Members: Calvin Anglo, Choie Llamas
Project Milestone: 1
Created: 2022-11-24
Updated: 2022-11-30
"""

from html.parser import HTMLParser
import urllib.request
from datetime import datetime
import logging

class WeatherScraper(HTMLParser):
    """
    This class scrapes data from the weather website.
    """
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
            logger.error(error)

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

            if tag == "abbr" and self.inDate is True:
                self.date = attrs[0][1]

            if tag == "li" and len(attrs) > 1 and attrs[1][1] == "previous":
                self.has_link = True

            if tag == "a" and attrs[0][1] == "prev" and self.has_link is True:
                self.link = attrs[1][1]

            if tag == "li" and len(attrs) > 1 and attrs[1][1] == "previous disabled":
                self.has_link = False
        except Exception as error:
            logger.error(error)

    def handle_endtag(self,tag):
        """
        This method handles the end tag of the scraper.
        """
        try:
            if tag == "tr":
                self.inTr = False

                #if self.date != "Average" and self.date != "Extreme":
                if self.date not in ('Average', 'Extreme'):
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
            logger.error(error)


    def handle_data(self,data):
        """
        This method handles the data in a tag.
        """
        try:
            if self.inTr is True and self.inTd is True:
                self.row.append(data)

                if len(self.row) == 3:
                    self.inTr = False
        except Exception as error:
            logger.error(error)

    def start_scraper(self):
        """
        This method scrapes data from climate.weather.gc.ca.
        """
        try:
            currentyear = datetime.now().year
            currentmonth = datetime.now().month

            #Full Link
            current_link = ("http://climate.weather.gc.ca/climate_data/daily_data_e.html?"
                    "StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day="
                    "1&Year=" + str(currentyear) + "&Month=" + str(currentmonth))

            #Link for testing
            # current_link = ("http://climate.weather.gc.ca/climate_data/daily_data_e.html?"
            #         "StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day="
            #         "1&Year=1997&Month=3")

            while self.has_link:

                with urllib.request.urlopen(current_link) as response:
                    html = str(response.read())

                self.feed(html)
                current_link = "http://climate.weather.gc.ca" + self.link

            # print(self.weather)
        except Exception as error:
            logger.error(error)

    def get_weather(self):
        """
        This method prints and returns the Min, Max, and Mean of the days that were scraped.
        """
        print(self.weather)
        return self.weather


logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# myparser = WeatherScraper()
# myparser.start_scraper()
# myparser.get_weather()