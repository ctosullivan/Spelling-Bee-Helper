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
            self.cur.execute("CREATE TABLE spelling_bee(word_id INTEGER PRIMARY KEY,word TEXT UNIQUE,num_letters INT,status WORD,status_date DATE)")
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
            (10,'HUNDRED', 7, 'ALLOWED','2014-05-01'),
        ]
        self.cur.executemany("INSERT INTO spelling_bee VALUES(?, ?, ?, ?, ?)",data)
        self.bee_data.commit()

    def retrieve_test_transactions(self):
        for row in self.cur.execute("SELECT word_id, word, num_letters, status, status_date FROM spelling_bee ORDER BY status_date"):
            print(row)

    def upsert_transactions(self,word_file):

        # Split out individual transactions with DATE - a valid transaction starts with and ends with a date field
        split_regex = re.compile(r'(?=DATE:)',re.MULTILINE | re.IGNORECASE)
        word_file = re.split(split_regex,word_file.read())
        
        # Discard first item in list - empty split prior to first transaction
        word_file.pop(0)
        transactions = word_file

        #Split transaction into fields using regexes
        date_regex = re.compile(r'^DATE:\s*\n(?P<date>(?:\d{4}-(\d{2}|\d{1})-(\d{2}|\d{1}$)))', re.IGNORECASE|re.MULTILINE)
        allowed_regex = re.compile(r'^ALLOWED:\s*$', re.IGNORECASE|re.MULTILINE)
        disallowed_regex = re.compile(r'^DISALLOWED:\s*$', re.IGNORECASE|re.MULTILINE)

        for transaction in transactions:

            date = re.match(date_regex,transaction).group(1)
            allowed_transaction_text = re.search(allowed_regex,transaction)
            disallowed_transaction_text = re.search(disallowed_regex,transaction)

            if allowed_transaction_text:

                if disallowed_transaction_text and disallowed_transaction_text.span()[1]<allowed_transaction_text.span()[0]:

                    # allowed transactions are after disallowed transactions
                    allowed_transaction_span = (allowed_transaction_text.span()[1],len(transaction))

                elif disallowed_transaction_text and disallowed_transaction_text.span()[0]>allowed_transaction_text.span()[1]:

                    # allowed transactions are before disallowed transactions
                    allowed_transaction_span = (allowed_transaction_text.span()[1],disallowed_transaction_text.span()[0])
                
                else:
                    # there are no disallowed transactions
                    allowed_transaction_span = (allowed_transaction_text.span()[1],len(transaction))

            if disallowed_transaction_text:

                if allowed_transaction_text and allowed_transaction_text.span()[1]<disallowed_transaction_text.span()[0]:

                    # disallowed transactions are after allowed transactions
                    disallowed_transaction_span = (disallowed_transaction_text.span()[1],len(transaction))

                elif allowed_transaction_text and allowed_transaction_text.span()[0]>disallowed_transaction_text.span()[1]:

                    # disallowed transactions are before allowed transactions
                    disallowed_transaction_span = (disallowed_transaction_text.span()[1],allowed_transaction_text.span()[0])
                
                else:
                    # there are no allowed transactions
                    disallowed_transaction_span = (disallowed_transaction_text.span()[1],len(transaction))

            if allowed_transaction_text:
                allowed_transactions = transaction[allowed_transaction_span[0]:allowed_transaction_span[1]]
                allowed_transactions = allowed_transactions.splitlines()
                # Convert to uppercase and remove empty strings
                allowed_transactions = [i.upper() for i in allowed_transactions if i]

            if disallowed_transaction_text:
                disallowed_transactions = transaction[disallowed_transaction_span[0]:disallowed_transaction_span[1]]
                disallowed_transactions = disallowed_transactions.splitlines()
                # Convert to uppercase and remove empty strings
                disallowed_transactions = [i.upper() for i in disallowed_transactions if i]

            query = '''
                INSERT INTO spelling_bee (word, num_letters, status, status_date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(word)
                DO UPDATE SET
                    status = CASE 
                                WHEN excluded.status_date > spelling_bee.status_date 
                                AND excluded.status != spelling_bee.status
                                THEN excluded.status
                                ELSE spelling_bee.status
                            END,
                    status_date = CASE 
                                    WHEN excluded.status_date > spelling_bee.status_date 
                                    AND excluded.status != spelling_bee.status
                                    THEN excluded.status_date
                                    ELSE spelling_bee.status_date
                                END;
            '''
            if allowed_transactions:
                for i in range(0,len(allowed_transactions)):
                    word = allowed_transactions[i]
                    num_letters = len(allowed_transactions[i])
                    status = "ALLOWED"
                    self.cur.execute(query, (word, num_letters, status, date))

            if disallowed_transactions:
                for i in range(0,len(disallowed_transactions)):
                    word = disallowed_transactions[i]
                    num_letters = len(disallowed_transactions[i])
                    status = "DISALLOWED"
                    # print(word, num_letters, status, date)
                    self.cur.execute(query, (word, num_letters, status, date))

            self.bee_data.commit()