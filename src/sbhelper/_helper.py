from sbhelper._tools import Tool

class Helper(Tool):
    def __init__(self) -> None:
        super().__init__()
        pass

    def sb_helper(self, database, first_letters=str, length=int) -> list:
        '''
        Spelling Bee helper function to provide a list of allowed words with a given length and given starting letters
        Args:
            database: word list database
            first letters(str) - beginning letters of word
            length(int) - number of letters for result words
        Returns:
            list of matching words
        '''

        query = """
        SELECT word, num_letters, status, status_date
        FROM word_data
        WHERE word LIKE ? AND num_letters = ? AND status != 'DISALLOWED'
        """

        # Use the 'first_two_letters' with a wildcard '%'
        database.cur.execute(query, (first_letters + '%',length))

        matching_words = database.cur.fetchall()

        return matching_words