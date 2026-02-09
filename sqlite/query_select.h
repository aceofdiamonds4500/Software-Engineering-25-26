#include <stdio.h>
#include <sqlite3.h>
#include <string.h>
#include <stdlib.h>

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

   sqlite3_bind_int(stmt, 1, id);
   if (rc != SQLITE_OK) {
      fprintf(stderr, "Failed to bind parameter: %s\n", sqlite3_errmsg(db));
      sqlite3_finalize(stmt);
      return NULL;
   }
   return stmt;
}

char* select_transcript(int id)
{
   if (id < 1) return NULL;
   sqlite3* db;
   char *sql = "SELECT * FROM MED_DATA WHERE ID=(?)";
   int rc;
   rc = sqlite3_open("database.db", &db);
   if(rc){
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return NULL;
   }

   sqlite3_stmt *stmt = make_statement(db, sql, id);
   if(stmt == NULL){
      fprintf(stderr, "SQLite error: cannot make statement\n");
      return NULL;
   }

   rc = sqlite3_step(stmt);
   if(rc != SQLITE_DONE && rc != SQLITE_ROW){
      fprintf(stderr, "SQLite code: %s\n", sqlite3_errmsg(db));
   }

   size_t entry_size = 0;
   for(int i = 0; i < 5; i++){
      const unsigned char* col = sqlite3_column_text(stmt, i+1);
      if(col) entry_size += strlen((const char*)col) + 2;
   }
   entry_size += 1;

   char* full_transcript = malloc(entry_size);
   if (!full_transcript) {
      sqlite3_finalize(stmt);
      sqlite3_close(db);
      return NULL;
   }
   full_transcript[0] = '\0';

   for(int i = 0; i < 5; i++){
      const unsigned char* col = sqlite3_column_text(stmt, i+1);
      if(col) strncat(full_transcript, (const char*)col, entry_size - strlen(full_transcript) - 1);
      if(i < 4) strncat(full_transcript, ", ", entry_size - strlen(full_transcript) - 1);
   }

   char* output = full_transcript;
   free(full_transcript);
   sqlite3_finalize(stmt);
   return output;
}
