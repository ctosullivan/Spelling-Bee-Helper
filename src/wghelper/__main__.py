from wghelper._helper import Helper
from wghelper._solver import Solver
from wghelper._interface import Interface
from wghelper._database import Word_database
from wghelper._tools import TextFileReader

def main():
    '''
    Primary program entrypoint
    '''
    word_data = Word_database()
    sb_helper = Helper()
    solver = Solver()
    interface = Interface()

    word_data.initialise_database()
    cli_args = interface.parse_args()
    if cli_args[0]=="SBSOLVE":
        solutions=solver.sb_solver(word_data, cli_args[1],cli_args[2])
        if solutions:
            print("SOLUTION:")
            for word in solutions:
                print(word[0])
    # with TextFileReader("../../data/Scrabble word list.txt") as file:
    #     word_data.upsert_transactions(file)
    # word_data.insert_test_transactions()
    # test_helper.test_helper(word_data, "CA",5)
    # 
    # word_data.retrieve_test_transactions()
    word_data.close_database()

if __name__ == "__main__":
    main()
