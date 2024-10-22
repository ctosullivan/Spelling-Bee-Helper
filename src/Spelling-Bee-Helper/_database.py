import sqlite3
import re

class Bee_database:
    def __init__(self) -> None:
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
            self.cur.execute("CREATE TABLE spelling_bee(word_id INT,word TEXT PRIMARY KEY,num_letters INT,status WORD,status_date DATE)")
            self.res = self.cur.execute("SELECT name FROM sqlite_master")
            result = self.res.fetchone()

    def close_database(self):
        self.bee_data.close()

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

    def insert_update_transactions(self,word_file):

        # Split out individual transactions with DATE - a valid transaction starts with and ends with a date field
        split_regex = re.compile(r'(?=DATE:)',re.MULTILINE | re.IGNORECASE)
        word_file = re.split(split_regex,word_file.read())
        # Discard first item in list - empty split prior to first transaction
        word_file.pop(0)
        transactions = word_file

        #Split transaction into fields using regexes
        date_regex = re.compile(r'^DATE:\n(?P<date>(?:\d{4}-(\d{2}|\d{1})-(\d{2}|\d{1}$)))', re.IGNORECASE|re.MULTILINE)

        allowed_regex = re.compile(r'^ALLOWED:\s*(?P<allowed>(?:\s*\w+\n?\s*)+$)', re.IGNORECASE|re.MULTILINE)

        disallowed_regex = re.compile(r'^DISALLOWED:\s*\n(?P<disallowed>(?:\s*\w+\s*)+$)', re.IGNORECASE|re.MULTILINE)

        for transaction in transactions:
            date = re.match(date_regex,transaction).group(1)
            allowed_transactions = re.findall(allowed_regex,transaction)[0]
            disallowed_transactions = re.findall(disallowed_regex,transaction)[0]
            split_allowed_transactions = re.split(r'\n',allowed_transactions)
            split_disallowed_transactions = re.split(r'\n',disallowed_transactions)
            allowed_words = []
            disallowed_words = []
            for item in split_allowed_transactions:
                if item != "":
                    allowed_words.append(item.upper())
            for item in split_disallowed_transactions:
                if item != "":
                    disallowed_words.append(item.upper())
            print(date,allowed_words,disallowed_words)