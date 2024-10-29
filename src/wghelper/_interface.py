import argparse
import sys
from wghelper._constants import ValidationError

class Interface:
    def __init__(self) -> None:
        self.argparser = argparse.ArgumentParser(
        prog='Word Game Helper',
        description='Helps solve various word games using logical and regular expressions',
        epilog='Helps solve various word games',
        )
        self.argparser.add_argument('-s','--sbsolve',nargs='?',help='Spelling Bee solver - enter the puzzle letters in the following format: "CentreLetter OtherLetters"')

        # Credit to https://stackoverflow.com/a/12818237 - unknown arguments are ignored so that output can be passed to other commands
        self.args = self.argparser.parse_known_args()
    
    def parse_args(self) -> str:
        '''
        Parses command line arguments received, performs validation and returns an array representing the arguments received - first element in the array returned is the command received
        '''
        sbsolve = getattr(self.args[0],"sbsolve")
        sbsolve_parsed = sbsolve.split(" ")

        if sbsolve == None:
            raise ValidationError('Please enter a valid value for the puzzle letters e.g: "A BCDEFG"')
            
        elif not all(i.isalpha() for i in sbsolve_parsed):
            raise ValidationError('Please enter only letters separated by one space for the puzzle input e.g: "A BCDEFG"')
        
        elif len(sbsolve_parsed[0])>1:
            raise ValidationError('Only one letter should be entered for puzzles centre letter, followed by a space and then the remaining letters e.g: "A BCDEFG')
        
        elif len(sbsolve_parsed)>2 or len(sbsolve_parsed)<2:
            raise ValidationError('Please enter a valid value for the puzzle letters e.g: "A BCDEFG"')
        else:
            sbsolve_parsed.insert(0,"sbsolve")
            # Convert to uppercase and remove any empty strings
            sbsolve_parsed = [i.upper() for i in sbsolve_parsed if i]
            print(sbsolve_parsed)
            return sbsolve_parsed