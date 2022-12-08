from dbcm import DBCM
import logging
import sqlite3

class DBOPerations():

    def fetch_data(self, start, end):

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
            logger.error("Error")
        
    def save_data(self, data, location):

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
            logger.error("Error")
            
    def initialize_db(self):
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
            logger.error("Error")

    def purge_data(self):

        try:

            with DBCM("weather.sqlite") as cursor:
                sql = "drop table if exists samples"
                cursor.execute(sql)
        except Exception as error:
            logger.error("Error")

    


logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)