from _tools import Tool

class Helper(Tool):
    def __init__(self):
        super().__init__()
        pass

    def test_helper(self, database):
        first_two_letters = 'NI'
        query = """
        SELECT word, num_letters, status, status_date
        FROM spelling_bee
        WHERE word LIKE ?
        """

        # Use the 'first_two_letters' with a wildcard '%'
        database.cur.execute(query, (first_two_letters + '%',))

        # Fetch all matching rows
        matching_words = database.cur.fetchall()

        # Print the results
        for row in matching_words:
            print(row)