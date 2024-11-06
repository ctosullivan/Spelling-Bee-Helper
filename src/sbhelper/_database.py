import sqlite3
import re
import sys
import pathlib

class Word_database:

    DATABASE_PATH = pathlib.Path.home() / "sbhelper"
    DATABASE_PATH.mkdir(parents=True, exist_ok=True)
    DATABASE_PATH = DATABASE_PATH / "sbhelper.db"

    def __init__(self,file_path=DATABASE_PATH) -> None | FileNotFoundError | IOError | Exception:
        '''
        Connect to existing database, or create a new database if it doesn't exist already. Also defines REGEXP function for use with SQLite database
        Raises:
            FileNotFoundError: if database file cannot be found
            IOError: if any other IO error occurs
            Exception: if any other unexpected error occurs
        '''
        try:
            self.word_data = sqlite3.connect(file_path)
            self.cur = self.word_data.cursor()
        
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            sys.exit(1)
        
        except IOError:
            print(f"Error: An I/O error occurred while reading the file {file_path}")
            sys.exit(1)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
        
        def regexp(expr, item):
            '''
            Enables REGEXP function in SQLite - credit https://stackoverflow.com/a/24053719
            '''
            reg = re.compile(expr)
            return reg.search(item) is not None
        
        self.word_data.create_function("REGEXP", 2, regexp)

    def _run_query(self, query, *query_args)-> None:
        ''' 
        Execute provided SQLite query - Credit - https://realpython.com/contact-book-python-textual/
        '''
        result = self.cur.execute(query, [*query_args])
        self.word_data.commit()
        return result

    def get_all_data(self)-> None:
        '''
        Returns all data in SQLite database
        '''
        result = self._run_query("SELECT * FROM word_data;")
        return result.fetchall()

    def initialise_database(self) -> None:
        '''
        Initialise main database table if not already done
        '''
        self.res = self.cur.execute("SELECT name FROM sqlite_master")
        result = self.res.fetchone()
        if result is None:
            self.cur.execute("CREATE TABLE word_data(word_id INTEGER PRIMARY KEY,word TEXT UNIQUE,num_letters INT,status WORD,status_date DATE)")
            self.res = self.cur.execute("SELECT name FROM sqlite_master")

    def close_database(self) -> None:
        '''
        Close database connection
        '''
        self.word_data.close()

    def upsert_transactions(self,word_file) -> None:
        '''
        Parses a text file with allowed and disallowed words to be inserted into the database (i.e. from a dictionary word list or result from a Spelling Bee). A valid transaction is in the following format:
        Date:
        YYYY-M(M)-D(D)
        Allowed:
        FOO
        Disallowed:
        BAR
        Order is irrelevant for Allowed/Disallowed words - both fields are optional however a date is mandatory at the start of the transaction.

        Valid transactions are inserted into the database using Upsert syntax - words are unique values, a word's status will only be updated if the date of the transaction is after the pre-existing transaction.

        Args:   
            word_file - a text file including valid word list transactions
        Returns: None
        '''
        split_regex = re.compile(r'(?=DATE:)',re.MULTILINE | re.IGNORECASE)
        word_file = re.split(split_regex,word_file.read())
        
        # Discard first item in list - empty split prior to first transaction
        word_file.pop(0)
        transactions = word_file

        #Split transaction into fields using regex
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
                INSERT INTO word_data (word, num_letters, status, status_date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(word)
                DO UPDATE SET
                    status = CASE 
                                WHEN excluded.status_date > word_data.status_date 
                                AND excluded.status != word_data.status
                                THEN excluded.status
                                ELSE word_data.status
                            END,
                    status_date = CASE 
                                    WHEN excluded.status_date > word_data.status_date 
                                    AND excluded.status != word_data.status
                                    THEN excluded.status_date
                                    ELSE word_data.status_date
                                END;
            '''
            if allowed_transactions:
                for i in range(0,len(allowed_transactions)):
                    word = allowed_transactions[i]
                    num_letters = len(allowed_transactions[i])
                    status = "ALLOWED"
                    self.cur.execute(query, (word, num_letters, status, date))
                self.word_data.commit()
            if disallowed_transactions:
                for i in range(0,len(disallowed_transactions)):
                    word = disallowed_transactions[i]
                    num_letters = len(disallowed_transactions[i])
                    status = "DISALLOWED"
                    self.cur.execute(query, (word, num_letters, status, date))
                self.word_data.commit()

        