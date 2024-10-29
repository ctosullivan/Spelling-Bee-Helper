import sys

class Tool:
    def __init__(self) -> None:
        pass

class TextFileReader:
    '''
    A context manager to handle file opening, reading and closure.

    # Source - https://realpython.com/python-magic-methods/#handling-setup-and-teardown-with-context-managers
    '''


    def __init__(self, file_path, encoding="utf-8") -> None:
        self.file_path = file_path
        self.encoding = encoding

    def __enter__(self):
        try:
            self.file_obj = open(self.file_path, mode="r", encoding=self.encoding)
            return self.file_obj
        
        except FileNotFoundError:
            # Handle the case where the file does not exist
            print(f"Error: The file '{self.file_path}' was not found.")
            sys.exit(1)
        
        except IOError:
            # Handle any other IO-related errors
            print(f"Error: An I/O error occurred while reading the file '{self.file_path}'.")
            sys.exit(1)
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
        return True