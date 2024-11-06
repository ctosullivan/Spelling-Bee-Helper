# Python Spelling Bee Helper

A simple CLI tool to help solve NYTime Spelling Bee puzzles.

The program initiates a SQLite database located in user's home/sbhelper directory

## Usage:

usage: sbhelper (-h) (-s (SBSOLVE)) (-sh (SBHELPER)) (-f (FILEIMPORT))

CLI tool to help solve various word games using logical and regular expressions

## Options:

-h, --help show this help message and exit

-s (SBSOLVE), --sbsolve (SBSOLVE)
Spelling Bee solver - enter the puzzle letters in the following format: "CentreLetter OtherLetters"

Provides a full solution for a provided Spelling Bee puzzle using words stored in database

-sh (SBHELPER), --sbhelper (SBHELPER)
Spelling Bee helper - enter the starting letters followed by the word length in the following format: "AB 5"

Lists words beginning with the specified letters from the database

-f (FILEIMPORT), --fileimport (FILEIMPORT) Specify the path for the file you want to import in brackets
Imports a word list text file in the following format:

DATE:
YYYY-M(M)-D(D)
ALLOWED:
(optional)
DISALLOWED:
(optional)

Example word list:

DATE:
2024-01-01

ALLOWED:
TUNIC
TABLE
FOO
BAR

DISALLOWED:
TOMATO

The word TOMATO would not appear in future results until specifically whitelisted again by adding a new wordfile and listing it as an allowed word,

Valid word transactions are inserted into the database using Upsert syntax - words are unique values, a word's status will only be updated if the date of the transaction is after the pre-existing transaction.

Example usage:

Installation: pip install sbhelper

View help: sbhelper -h

Insert transactions from file: sbhelper -f "some_file.txt"

Spelling Bee solver: sbhelper -s "A BCDEFG"

Spelling Bee helper: sbhelper -sh "AB 5"
