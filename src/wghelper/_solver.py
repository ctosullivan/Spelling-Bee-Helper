from wghelper._tools import Tool

class Solver(Tool):
    def __init__(self) -> None:
        super().__init__()
        pass

    def sb_solver(self, database, centre_letter=str, other_letters=str) -> list:
        '''
        Function to solve a Spelling Bee puzzle using Regex
        Args:
            database: word list database
            centre letter(str) - mandatory centre letter in Spelling Bee puzzle
            other letters(str) - remaining optional letters in Spelling Bee puzzle
        Returns:
            list of matching words including word length and allowed/disallowed status            
        '''
        
        #Regex credit - https://stackoverflow.com/a/78411195

        reg = rf"^(?=.*{centre_letter})[{centre_letter}{other_letters}]{{4,}}$"

        # Query to select words that:
        # 1. Contain the mandatory letter.
        # 2. Only contain letters from the allowed set.
        # 3. Have a status that is not "DISALLOWED".
        query = """
            SELECT word, num_letters, status, status_date
            FROM word_data
            WHERE word REGEXP ?
            AND status != 'DISALLOWED'
        """

        # Execute the query
        database.cur.execute(query, (reg,))

        # Fetch all matching rows
        matching_words = database.cur.fetchall()

        # Return the results
        return matching_words
