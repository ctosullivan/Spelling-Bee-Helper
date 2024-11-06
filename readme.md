# Python Spelling Bee Helper

A simple CLI to help NYTime Spelling Bee puzzles.

The program initiates a SQLite database in the following relative directory to the installation: ../../data

## Usage:

usage: sbhelper (-h) (-s (SBSOLVE)) (-sh (SBHELPER)) (-f (FILEIMPORT))

CLI tool to help solve various word games using logical and regular expressions

### Options:

-h, --help show this help message and exit

-s (SBSOLVE), --sbsolve (SBSOLVE)
Spelling Bee solver - enter the puzzle letters in the following format: "CentreLetter OtherLetters"

-sh (SBHELPER), --sbhelper (SBHELPER)
Spelling Bee helper - enter the starting letters followed by the word length in the following format: "AB 5"

-f (FILEIMPORT), --fileimport (FILEIMPORT)
Import a word list text file in the following format:
DATE: YYYY-M(M)-D(D) ALLOWED: (optional)
DISALLOWED (optional). Specify
the path for the file you want to import
