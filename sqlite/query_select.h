#include <stdio.h>
#include <sqlite3.h>
#include <string.h>
#include <stdlib.h>

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
sqlite3_stmt* make_statement(sqlite3* db, char *sql, int id)
{
   int rc; 
   sqlite3_stmt *stmt;

   rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
   if(rc != SQLITE_OK)
   {
      fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
      return NULL;
   } 

   //puts the ID in the query
   sqlite3_bind_int(stmt, 1, id);
   if (rc != SQLITE_OK) {
      fprintf(stderr, "Failed to bind parameter: %s\n", sqlite3_errmsg(db));
      sqlite3_finalize(stmt);
      return NULL;
   }
 
   return stmt;
}

/**
* select_transcript: gives you the info about the transcript exactly how it's organized in the .csv
* 
* @id: the id of the entry that you want to access
*
* @return: char* containing entire string of an entry without leading ID
*
**/
char* select_transcript(int id)
{      
   if (id < 1)
   {
      return NULL;
   }
   sqlite3* db;
   char *sql = "SELECT * FROM MED_DATA WHERE ID=(?)";
   int rc;

   rc = sqlite3_open("database.db", &db);
   if(rc)
   {
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return NULL;
   }

   sqlite3_stmt *stmt = make_statement(db, sql, id);
   if(stmt == NULL)
   {
      fprintf(stderr, "SQLite error: cannot make statement\n");
      return NULL;      
   }

   rc = sqlite3_step(stmt);
   if(rc != SQLITE_DONE && rc != SQLITE_ROW)
   {
      fprintf(stderr, "SQLite code: %s\n", sqlite3_errmsg(db));
   } 

   //test, printf("%s\n", (const char*)sqlite3_column_text(stmt,1));

   //takes the size of the transcript + space for ", " between each entry
   size_t entry_size = strlen((const char*)sqlite3_column_text(stmt,1))+2+ 
                       strlen((const char*)sqlite3_column_text(stmt,2))+2+ 
                       strlen((const char*)sqlite3_column_text(stmt,3))+2+ 
                       strlen((const char*)sqlite3_column_text(stmt,4))+2+ 
                       strlen((const char*)sqlite3_column_text(stmt,5))+ 1;
 
   char* full_transcript = malloc(entry_size);  // Heap allocation
   if (!full_transcript) {
      sqlite3_finalize(stmt);
      sqlite3_close(db);
      return NULL;
   }

   full_transcript[0] = '\0'; 

   for(int i = 0; i < 5; i++)
   {
      strncat(full_transcript,(const char*)sqlite3_column_text(stmt,i+1),entry_size - strlen(full_transcript) - 1);
      if(i < 4)
      {
         strncat(full_transcript,", ",entry_size - strlen(full_transcript) - 1);
      }
   }
   //test, printf("%s\n",full_transcript);

   char* output = full_transcript;
   free(full_transcript);
   sqlite3_finalize(stmt);

   return output;
}
