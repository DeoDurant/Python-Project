"""
Weather Scraper
Group Members: Calvin Anglo, Choie Llamas
Project Milestone: 1
Created: 2022-11-24
Updated: 2022-12-16
"""
import sqlite3

class DBCM():
    """This class is a context manager for the weather app. Choie & Calvin """

    def __init__(self, connect, cursor):
        """ Initialize the class with a connection parameter. Choie & Calvin """ 
        self.connect = connect
        self.cursor = cursor

    def __enter__(self):
        """This method is called when the context manager is entered using the "with" statement. Choie & Calvin"""
        self.connect = sqlite3.connect(self.connect)
        # Create a connection to the SQLite database using the connection string provided
        self.cursor = self.connect.cursor()
        # Create a cursor to execute SQL commands on the connection
        return self.cursor
        # Return the cursor to the calling code to be used for executing SQL commands

    def __exit__(self, exc_type, exc_value, exc_trace):
        """ This method is called when the context manager is exited using the "with" statement. Choie & Calvin """
        self.connect.commit()
        # Commit any pending transactions to the database
        self.cursor.close()
        # Close the cursor
        self.connect.close()
        # Close the connection