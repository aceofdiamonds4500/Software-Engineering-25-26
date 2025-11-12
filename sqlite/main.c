#include <stdio.h>
#include <sqlite3.h>
#include "query_insert.h"
#include "query_select.h"

/**
* init: creates the database tables
*
* @return: sqlite return code
*
**/
int init(){
   sqlite3* DB;
   char* sql = "CREATE TABLE MED_DATA("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT, "
               "DESC TEXT NOT NULL, "
               "MEDICAL_SPECIALTY TEXT NOT NULL, "
               "SAMPLE_NAME TEXT NOT NULL, "
               "TRANSCRIPTION TEXT NOT NULL, "
               "KEYWORDS TEXT NOT NULL);"
               "CREATE TABLE DOCTORS("
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

// look, this shit aint going in the dll, but this is what the input variables are
   insert_transcript("A 23-year-old white female presents with complaint of allergies.", 
"Allergy / Immunology", 
"Allergic Rhinitis",
"SUBJECTIVE:,  This 23-year-old white female presents with complaint of allergies.  She used to have allergies when she lived in Seattle but she thinks they are worse here.  In the past, she has tried Claritin, and Zyrtec.  Both worked for short time but then seemed to lose effectiveness.  She has used Allegra also.  She used that last summer and she began using it again two weeks ago.  It does not appear to be working very well.  She has used over-the-counter sprays but no prescription nasal sprays.  She does have asthma but doest not require daily medication for this and does not think it is flaring up.,MEDICATIONS: , Her only medication currently is Ortho Tri-Cyclen and the Allegra.,ALLERGIES: , She has no known medicine allergies.,OBJECTIVE:,Vitals:  Weight was 130 pounds and blood pressure 124/78.,HEENT:  Her throat was mildly erythematous without exudate.  Nasal mucosa was erythematous and swollen.  Only clear drainage was seen.  TMs were clear.,Neck:  Supple without adenopathy.,Lungs:  Clear.,ASSESSMENT:,  Allergic rhinitis.,PLAN:,1.  She will try Zyrtec instead of Allegra again.  Another option will be to use loratadine.  She does not think she has prescription coverage so that might be cheaper.,2.  Samples of Nasonex two sprays in each nostril given for three weeks.  A prescription was written as well.",
"allergy / immunology, allergic rhinitis, allergies, asthma, nasal sprays, rhinitis, nasal, erythematous, allegra, sprays, allergic,");
   insert_userdata("example name", "example hospital");
   printf("%s\n", select_transcript(2));
   return (0);
}

