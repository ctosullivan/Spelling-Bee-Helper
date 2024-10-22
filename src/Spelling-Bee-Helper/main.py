from _database import Bee_database
from _helper import Helper
from _solver import Solver

if __name__ == "__main__":
    bee_data = Bee_database()
    test_helper = Helper()
    test_solver = Solver()
    bee_data.initialise_database()
    # bee_data.insert_test_transactions()
    bee_data.retrieve_test_transactions()
    # test_helper.test_helper(bee_data)
    # test_solver.test_solver(bee_data)
    # print(bee_data.import_words("../../data/word_list.txt"))
    bee_data.close_database()