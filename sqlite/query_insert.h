#include <stdio.h>
#include <sqlite3.h>

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
int insert_transcript(const char *desc, 
                      const char *specialty,
                      const char *sample_name,
                      const char *transcript,
                      const char *keywords)
{
   sqlite3* db;
   char* sql = "INSERT INTO MED_DATA (DESC, MEDICAL_SPECIALTY, SAMPLE_NAME, TRANSCRIPTION, KEYWORDS) VALUES (?, ?, ?, ?, ?);";
   int rc;
   sqlite3_stmt *stmt;
   
   rc = sqlite3_open("database.db", &db);
   if(rc)
   {
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
   if(rc != SQLITE_OK)
   {
      fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   // you need to bind all of them one at a time. pls try and make it a for loop i dare u
   sqlite3_bind_text(stmt, 1, desc, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 2, specialty, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 3, sample_name, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 4, transcript, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 5, keywords, -1, SQLITE_STATIC);

   rc = sqlite3_step(stmt);
   if(rc != SQLITE_DONE)
   {
     fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
   }

   long id = sqlite3_last_insert_rowid(db); 
   
   sqlite3_finalize(stmt); 
   sqlite3_close(db);
   return 0;
}

/**
* insert_userdata: literally the same thing as insert_transcript with diff vars
*
* @name: the doctor's name
* @hospital: the hospital the doctor is associated with
*
* @return: sqlite return code
*
**/
int insert_userdata(const char *name,
                    const char *hospital)
{
   sqlite3* db;
   char* sql = "INSERT INTO DOCTORS (NAME, HOSPITAL) VALUES (?, ?);";
   int rc;
   sqlite3_stmt *stmt;      

   rc = sqlite3_open("database.db", &db);
   if(rc)
   {
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return(0);
   }
   

   rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
   if(rc != SQLITE_OK)
   {
      fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
      return(0);
   }

   sqlite3_bind_text(stmt, 1, name, -1, SQLITE_STATIC);
   sqlite3_bind_text(stmt, 2, hospital, -1, SQLITE_STATIC);

   rc = sqlite3_step(stmt);
   if(rc != SQLITE_DONE)
   {
     fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
   }

   long id = sqlite3_last_insert_rowid(db); 
   
   sqlite3_finalize(stmt); 
   sqlite3_close(db);
   return 0;
}
