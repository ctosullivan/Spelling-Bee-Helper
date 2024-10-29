import argparse
import sys
from wghelper._constants import ValidationError

class Interface:
    def __init__(self) -> None:
        self.argparser = argparse.ArgumentParser(
        prog='Word Game Helper',
        description='Tool to help solve various word games using logical and regular expressions',
        epilog='CLI tool to solve various word games',
        )
        self.argparser.add_argument('-s','--sbsolve',nargs='?',help='Spelling Bee solver - enter the puzzle letters in the following format: "CentreLetter OtherLetters"')

        self.argparser.add_argument('-sh','--sbhelper',nargs='?',help='Spelling Bee helper - enter the starting letters followed by the word length in the following format: "AB 5"')

        self.argparser.add_argument('-f','--fileimport',nargs='?',help='Import a word list text file in the following format DATE: YYYY-M(M)-D(D) ALLOWED: (optional) DISALLOWED (optional). Specify the path for the file you want to import')

        # Credit to https://stackoverflow.com/a/12818237 - unknown arguments are ignored so that output can be passed to other commands
        self.args = self.argparser.parse_known_args()
    
    def parse_args(self) -> str:
        '''
        Parses command line arguments received, performs validation and returns an array representing the arguments received - first element in the array returned is the command received
        '''
        file_import = getattr(self.args[0],"fileimport")
        if file_import:
            file_import_parsed = []
            file_import_parsed.insert(0,"FILE_IMPORT")
            file_import_parsed.insert(1,fr'{file_import}')

            return file_import_parsed

        sbsolve = getattr(self.args[0],"sbsolve")
        if sbsolve:
            sbsolve_parsed = sbsolve.split(" ")
       
            if not all(i.isalpha() for i in sbsolve_parsed):
                raise ValidationError('Please enter only letters separated by one space for the puzzle input e.g: "A BCDEFG"')
            
            elif len(sbsolve_parsed[0])>1:
                raise ValidationError('Only one letter should be entered for puzzles centre letter, followed by a space and then the remaining letters e.g: "A BCDEFG')
            
            elif len(sbsolve_parsed)>2 or len(sbsolve_parsed)<2:
                raise ValidationError('Please enter a valid value for the puzzle letters e.g: "A BCDEFG"')
            else:
                sbsolve_parsed.insert(0,"sbsolve")
                # Convert to uppercase and remove any empty strings
                sbsolve_parsed = [i.upper() for i in sbsolve_parsed if i]
                return sbsolve_parsed
        
        sbhelper = getattr(self.args[0],"sbhelper")
        if sbhelper:
            sbhelper_parsed = sbhelper.split(" ")
         
            if len(sbhelper_parsed)>2 or len(sbhelper_parsed)<2:
                raise ValidationError('Please enter a valid query for the puzzle helper e.g: "AB 5"')
            
            elif not sbhelper[0].isalpha():
                raise ValidationError('Please enter only letters separated by one space for the helper letters input e.g: "AB 5"')
            
            elif not sbhelper_parsed[1].isdigit():
                raise ValidationError('Please enter only digits preceded by one space for the helper length input e.g: "AB 5"')
                
            elif len(sbhelper_parsed[0])<1:
                raise ValidationError('Please enter a valid query for the puzzle helper e.g: "AB 5"')
            
            else:
                sbhelper_parsed.insert(0,"sbhelper")
                # Convert to uppercase and remove any empty strings
                sbhelper_parsed = [i.upper() for i in sbhelper_parsed if i]
                # Convert length to int
                sbhelper_parsed[2] = int(sbhelper_parsed[2])
                return sbhelper_parsed