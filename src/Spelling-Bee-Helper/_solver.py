from _tools import Tool

class Solver(Tool):
    def __init__(self) -> None:
        super().__init__()
        pass

    def test_solver(self, database):
        
        #Regex credit - https://stackoverflow.com/a/78411195
        reg = "(?=.*E)^[NIETY]{4,}$"
        # Define the allowed range of letters (example: 'abcdefg') and the mandatory letter (example: 'a')
        allowed_letters = 'inty'
        mandatory_letter = 'E'

        # Query to select words that:
        # 1. Contain the mandatory letter.
        # 2. Only contain letters from the allowed set.
        query = """
            SELECT word, num_letters, status, status_date
            FROM spelling_bee
            WHERE word REGEXP ?  -- Must contain only allowed letters
        """

        # Execute the query
        database.cur.execute(query, (''.join(reg),))

        # Fetch all matching rows
        matching_words = database.cur.fetchall()

        # Print the results
        for row in matching_words:
            print(row)
