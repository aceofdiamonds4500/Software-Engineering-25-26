# Transcriptive Database

## Details
Contained is the collective library of really fast code that will give and get data for Transcriptive's database. A working DLL is coming soon in cycle 2, as well as more functions to get the data

## main.c
### init()
/**
* init: creates the database tables
*
* @return: sqlite return code
*
**/
## query_insert.h
### insert_transcript()
/**
* insert_transcript: takes your transcript input and delicately places it in the database
*
* @desc:        description
* @specialty:   medical specialty
* @sample_name: sample name
* @transcript:  transcript
* @keywords:    keywords
*
* @return: sqlite return code
*
**/
### insert_userdata()
/**
* insert_userdata: literally the same thing as insert_transcript with diff vars
*
* @name: the doctor's name
* @hospital: the hospital the doctor is associated with
*
* @return: sqlite return code
*
**/
## query_select.h
### make_statement()
/**
* make_statement: creates your statement, basically input sanitization
*
* @db: the database you opened
* @sql: your input query
* @id: the id that you want to bind to your statement
* TODO: make more versatile or add version that allows text binding
*
* @return: sqlite3_stmt* data type, essentially builds the text into a full query
*
**/
### select_transcript()
/**
* select_transcript: gives you the info about the transcript exactly how it's organized in the .csv
*
* @id: the id of the entry that you want to access
*
* @return: char* containing entire string of an entry without leading ID
*
**/
### COMING SOON: select_userdata()
### COMING SOON: select_transcript_lastvalue()
