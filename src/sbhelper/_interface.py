import argparse
import sys
from sbhelper._constants import ValidationError
import re

class Interface:
    def __init__(self) -> None:
        '''
        Interface initialises argparser and parses/validates CLI args provided
        '''
        self.argparser = argparse.ArgumentParser(
        prog='Spelling Bee Helper',
        description='Tool to help solve NYT Spelling Bee puzzles using a user-defined database',
        epilog='CLI tool to help solve NYT Spelling Bee puzzles'
        )
        self.argparser.add_argument('-s','--sbsolver',type=str,help='Spelling Bee solver - enter the puzzle letters in the following format: "CentreLetter OtherLetters"')

        self.argparser.add_argument('-sh','--sbhelper',type=str,help='Spelling Bee helper - enter the starting letters followed by the word length in the following format: "AB 5"')

        self.argparser.add_argument('-f','--fileimport',type=str,help='Import a word list text file in the following format DATE: YYYY-M(M)-D(D) ALLOWED: (optional) DISALLOWED (optional). Specify the path for the file you want to import')

        self.argparser.add_argument('-g','--getdata',help="Prints all data in the database",action='store_true')

        self.argparser.add_argument('-v','--version',help='Displays the current program version',action='store_true')

        self.args = self.argparser.parse_args()
    
    def parse_args(self) -> list | ValidationError:
        '''
        Parses command line arguments received, performs validation and returns an array representing the arguments received - first element in the array returned represents the command received
        Raises:
            ValidationError if CLI args fail validation tests
        Returns:
            Array representing CLI args received
        '''
        alpha_regex = re.compile(r'^[a-zA-Z]+$')

        if self.args.getdata:
            getdata_parsed = []
            getdata_parsed.insert(0,"GET_DATA")
            return getdata_parsed

        if self.args.fileimport:
            file_import_parsed = []
            file_import_parsed.insert(0,"FILE_IMPORT")
            file_import_parsed.insert(1,f'{self.args.fileimport}')
            return file_import_parsed

        if self.args.sbsolver:
            sbsolve_parsed = self.args.sbsolver.split(" ")
            if not all(re.fullmatch(alpha_regex,i) for i in sbsolve_parsed):
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

        if self.args.sbhelper:
            sbhelper_parsed = self.args.sbhelper.split()
            if len(sbhelper_parsed)>2 or len(sbhelper_parsed)<2:
                raise ValidationError('Please enter a valid query for the puzzle helper e.g: "AB 5"')
            
            elif not alpha_regex.fullmatch(sbhelper_parsed[0]):
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
            
        if self.args.version:
            version_parsed = ["VERSION"]
            return version_parsed        
        else:
            sys.exit("No arguments provided - try sbhelper -h for help")