"""
Weather Scraper
Group Members: Calvin Anglo, Choie Llamas
Project Milestone: 1
Created: 2022-11-24
Updated: 2022-11-30
"""

import logging
from dbcm import DBCM


class DBOPerations():
    """
    This class fetches, saves, initializes, and purges a database.
    """
    def fetch_data(self, start, end):
        """
        This method will return data for the plotting class. Choie
        """
        try:
            dates = []

            start_date = start + "-01-01"
            end_date = end + "-12-31"

            dates.append(start_date)
            dates.append(end_date)

            with DBCM("weather.sqlite") as cursor:
                sql = "select * from weather_data where date(sample_date) between ? and ? order by date(sample_date) asc"
                database_data = cursor.execute(sql, dates).fetchall()

            return database_data
        except Exception as error:
            logger.error(error)

    def save_data(self, data, location):
        """
        This method will save new data to the DB. Calvin
        """
        try:

            data_location = location
            weather_data = []
            print(weather_data)
            for date, temps in data.items():

                list_data = []
                list_data.append(date.strip())
                list_data.append(data_location)

                for _, temp_value in temps.items():

                    list_data.append(temp_value)

                weather_data.append(list_data)

            with DBCM("weather.sqlite") as cursor:
                sql = """insert into weather_data (sample_date,location,max_temp,min_temp,avg_temp)
                    select $x,$y,$c,$v,$b where not exists
                    (select 1 from weather_data where sample_date=$x and location=$y
                    and min_temp=$c and max_temp=$v and avg_temp=$b)"""

                cursor.executemany(sql, weather_data)

        except Exception as error:
            logger.error(error)

    def initialize_db(self):
        """
        This method initializes the database if one does not exist. Calvin
        """
        try:
            with DBCM("weather.sqlite") as cursor:
                sql = """Create table if not exists weather_data
                        (id integer primary key autoincrement not null,
                        sample_date text not null,
                        location text not null,
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);"""

                cursor.execute(sql)
        except Exception as error:
            logger.error(error)

    def purge_data(self):
        """
        This method purges data from the DB. Choie 
        """
        try:

            with DBCM("weather.sqlite") as cursor:
                sql = "drop table if exists samples"
                cursor.execute(sql)
        except Exception as error:
            logger.error(error)
            
    def latest(self):
        """
        This method returns the latest data from the db. Calvin
        """
        try:
            with DBCM("weather.sqlite") as cursor:
                sql = "select * from weather_data order by date(sample_date) desc limit 1"
                latest = cursor.execute(sql)

                for data in latest:

                    return data[1]

        except Exception as error:
            logger.error(error)

logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)