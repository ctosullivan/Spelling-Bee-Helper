from wghelper._tools import Tool

class Helper(Tool):
    def __init__(self) -> None:
        super().__init__()
        pass

    def test_helper(self, database, first_letters, length):

        query = """
        SELECT word, num_letters, status, status_date
        FROM word_data
        WHERE word LIKE ? AND num_letters = ? AND status != 'DISALLOWED'
        """

        # Use the 'first_two_letters' with a wildcard '%'
        database.cur.execute(query, (first_letters + '%',length))

        # Fetch all matching rows
        matching_words = database.cur.fetchall()

        # Print the results
        for row in matching_words:
            print(row)