#include <stdio.h>
#include <sqlite3.h>

int insert_transcript(const char *desc, const char *specialty, const char *sample_name, const char *transcript, const char *keywords)
{
   sqlite3* db;
   char* sql = "INSERT INTO MED_DATA (DESC, MEDICAL_SPECIALTY, SAMPLE_NAME, TRANSCRIPTION, KEYWORDS) VALUES (?, ?, ?, ?, ?);";
   int rc;
   sqlite3_stmt *stmt;
   rc = sqlite3_open("database.db", &db);
   if(rc){
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
   if(rc != SQLITE_OK){
      fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   sqlite3_bind_text(stmt, 1, desc, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 2, specialty, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 3, sample_name, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 4, transcript, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 5, keywords, -1, SQLITE_STATIC);

   rc = sqlite3_step(stmt);
   if(rc != SQLITE_DONE){
      fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
   }

   sqlite3_finalize(stmt);
   sqlite3_close(db);
   return 0;
}

int insert_userdata(const char *name, const char *hospital)
{
   sqlite3* db;
   char* sql = "INSERT INTO DOCTORS (NAME, HOSPITAL) VALUES (?, ?);";
   int rc;
   sqlite3_stmt *stmt;
   rc = sqlite3_open("database.db", &db);
   if(rc){
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
   if(rc != SQLITE_OK){
      fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   sqlite3_bind_text(stmt, 1, name, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 2, hospital, -1, SQLITE_STATIC);

   rc = sqlite3_step(stmt);
   if(rc != SQLITE_DONE){
      fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
   }

   sqlite3_finalize(stmt);
   sqlite3_close(db);
   return 0;
}
