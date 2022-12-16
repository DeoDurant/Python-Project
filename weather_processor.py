"""
Weather Scraper
Group Members: Calvin Anglo, Choie Llamas
Project Milestone: 1
Created: 2022-11-24
Updated: 2022-11-30
"""

import logging
from db_operations import DBOPerations
from scrape_weather import WeatherScraper

class WeatherProcessor():
    """
    This class prompts the user for input to scrape data from a website. Choie & Calvin
    """
    def user_choice(self):
        """
        This method prompts the user and calls other methods to scrape. Choie & Calvin
        """
        try:
            letters = ['u','f']
            error_flag = False

            while error_flag is False:
                user_input = input("Update ['u'] or Full ['f']? Enter your choice: ")
                lowercase_input = user_input.lower()

                if lowercase_input in letters:
                    if lowercase_input == "u":
                        self.update_choice()

                    elif lowercase_input == "f":
                        self.full_choice()
                else:
                    print("Error, you can only the letters in the brackets")

        except Exception as error:
            logger.error(error)

    def full_choice(self):
        """
        This method will scrape all of the data from a website as far back as it can. Choie & Calvin
        """
        try:
            weather_info = WeatherScraper()
            database = DBOPerations()
            database.initialize_db()
            weather_info.start_scraper()
            print("Saving to database")
            print(weather_info.get_weather())
            database.save_data(weather_info.get_weather(), "Winnipeg, MB")
            print("Data has been fully updated")
        except Exception as error:
            logger.error(error)

    def update_choice(self):
        """
        This method updates and saves the database. Choie & Calvin
        """
        try:
            weather_info = WeatherScraper()
            database = DBOPerations()
            database.initialize_db()
            latest_database = database.latest()
            print("Saving to database")
            weather_info.start_scraper(latest_database)

            database.save_data(weather_info.weather_data, "Winnipeg, MB")
            print("Database has been updated!")
        except Exception as error:
            logger.error(error)

logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

var1 = WeatherProcessor()
var1.user_choice()