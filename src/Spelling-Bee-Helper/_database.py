import sqlite3
import re

class Bee_database:
    def __init__(self):
        '''
        Connect to existing database, or create a new one if it doesn't exist already
        '''
        self.bee_data = sqlite3.connect("../../data/Spelling_Bee_Data.db")
        self.cur = self.bee_data.cursor()
        
        # Enable RE in SQLite - credit https://stackoverflow.com/a/24053719

        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None
        
        self.bee_data.create_function("REGEXP", 2, regexp)

    def initialise_database(self):
        '''
        Initialise database table if not already done
        '''
        self.res = self.cur.execute("SELECT name FROM sqlite_master")
        result = self.res.fetchone()
        if result is None:
            self.cur.execute("CREATE TABLE spelling_bee(word_id,word,num_letters,status,status_date)")
            self.res = self.cur.execute("SELECT name FROM sqlite_master")
            result = self.res.fetchone()

    def insert_test_transactions(self):
        data = [
            # Schema: word_id, word, num_letters, status, status_date
            (1, 'TEN', 3, 'ALLOWED','2014-05-01'),
            (2, 'TWENTY', 6, 'ALLOWED','2014-05-01'),
            (3, 'THIRTY', 6, 'ALLOWED','2014-05-01'),
            (4, 'FORTY', 5, 'ALLOWED','2014-05-01'),
            (5, 'FIFTY', 5, 'ALLOWED','2014-05-01'),
            (6, 'SIXTY', 5, 'ALLOWED','2014-05-01'),
            (7, 'SEVENTY', 7, 'ALLOWED','2014-05-01'),
            (8, 'EIGHTY', 6, 'ALLOWED','2014-05-01'),
            (9, 'NINETY', 6, 'ALLOWED','2014-05-01'),
            (10,'HUNDRED', 7, 'DISALLOWED','2024-05-01'),
        ]
        self.cur.executemany("INSERT INTO spelling_bee VALUES(?, ?, ?, ?, ?)",data)
        self.bee_data.commit()

    def retrieve_test_transactions(self):
        for row in self.cur.execute("SELECT word, status_date FROM spelling_bee ORDER BY status_date"):
            print(row)

    def close_database(self):
        self.bee_data.close()



    def import_words(self,word_list):
        '''
        Opens a file (word_list) and returns the file content
        '''
        try:
            # Open the file in read mode
            with open(word_list, 'r') as file:
                return file.read()
        
        except FileNotFoundError:
            # Handle the case where the file does not exist
            print(f"Error: The file '{word_list}' was not found.")
            return -1
        
        except IOError:
            # Handle any other IO-related errors
            print(f"Error: An I/O error occurred while reading the file '{word_list}'.")
            return -1
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            return -1
        