#include <stdio.h>
#include <sqlite3.h>
#include "query_insert.h"
#include "query_select.h"

int init(){
   sqlite3* DB;
   char* sql = "CREATE TABLE IF NOT EXISTS MED_DATA("
             "ID INTEGER PRIMARY KEY AUTOINCREMENT, "
               "DESC TEXT NOT NULL, "
               "MEDICAL_SPECIALTY TEXT NOT NULL, "
               "SAMPLE_NAME TEXT NOT NULL, "
               "TRANSCRIPTION TEXT NOT NULL, "
               "KEYWORDS TEXT NOT NULL);"
               "CREATE TABLE IF NOT EXISTS DOCTORS("
           "ID INTEGER PRIMARY KEY AUTOINCREMENT, "
               "NAME TEXT NOT NULL, "
               "HOSPITAL TEXT NOT NULL);";
   int rc = 0;
   rc = sqlite3_open("database.db", &DB);
   char* messageError;
   rc = sqlite3_exec(DB, sql, NULL, 0, &messageError);

   if (rc != SQLITE_OK) {
       printf("SQL error: %s\n", messageError);
       sqlite3_free(messageError);
   }
   else{
      printf("SQL OK\n");
   }
   sqlite3_close(DB);
}

int main(int argc, char** argv)
{
   init();
   return 0;
}
