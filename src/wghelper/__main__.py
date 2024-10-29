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
    helper = Helper()
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
    elif cli_args[0]=="SBHELPER":
        solutions = helper.sb_helper(word_data, cli_args[1],cli_args[2])
        if solutions:
            print("RESULTS:")
            for word in solutions:
                print(word[0])
    elif cli_args[0]=="FILE_IMPORT":
        file_path = cli_args[1]
        with TextFileReader(file_path) as file:
            word_data.upsert_transactions(file)

    word_data.close_database()

if __name__ == "__main__":
    main()
