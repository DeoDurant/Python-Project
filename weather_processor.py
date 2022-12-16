import logging
from db_operations import DBOPerations
from scrape_weather import WeatherScraper

class WeatherProcessor():
    """
    This class prompts the user for input to scrape data from a website.
    """
    def user_choice(self):
        """
        This method prompts the user and calls other methods to scrape.
        """
        try: 
            letters = ['u','f','s']
            error_flag = False

            while error_flag  == False:
                user_input = input("Update ['u'], Full ['f'], or Skip ['s']? Enter your choice: ")
                lowercase_input = user_input.lower()
                
                if lowercase_input in letters:
                    if lowercase_input == "d":
                        self.download_choice()

                    elif lowercase_input == "u":
                        self.update_choice()

                    elif lowercase_input == "f":
                        self.full_choice()
                        
                    elif lowercase_input == "s":
                        self.lowercase_choice()
                else:
                    print("Error, you can only the letters in the brackets")

        except Exception as error:
            logger.error(error)

    def full_choice(self):
        """
        This method will scrape all of the data from a website as far back as it can.
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
            logger.error("Error")



    def update_choice(self):
        """
        This method updates and saves the database.
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
            logger.error("Error")


    def year_choice(self):
        """
        This method prompts the user to enter a from year and to year.
        """
        self.user_input1 = input("Enter a from year (YYYY): ")
        self.user_input2 = input("Enter a to year (YYYY): ")

    def month_choice(self):
        """
        This method prompts the user to enter the month.
        """
        pass


logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

var1 = WeatherProcessor()
var1.user_choice()

