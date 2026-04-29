-- MySQL dump 10.13  Distrib 9.7.0, for Linux (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	9.7.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '3cd6f7ef-42a8-11f1-b857-9ebe94973649:1-9,
c343774e-3569-11f1-87bf-56d27f183c5c:1-14';

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `DOCTOR_ID` int NOT NULL,
  `D_FIRSTNAME` varchar(255) DEFAULT NULL,
  `D_LASTNAME` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`DOCTOR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `med_data`
--

DROP TABLE IF EXISTS `med_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `med_data` (
  `PATIENT_SSN` char(9) DEFAULT NULL,
  `DOCTOR_ID` int DEFAULT NULL,
  `P_FIRSTNAME` varchar(255) NOT NULL,
  `P_LASTNAME` varchar(255) NOT NULL,
  `DESC` text NOT NULL,
  `MED_SPECIALTY` text NOT NULL,
  `SAMPLE_NAME` text NOT NULL,
  `TRANSCRIPTION` text NOT NULL,
  KEY `fk_doctor_id` (`DOCTOR_ID`),
  CONSTRAINT `fk_doctor_id` FOREIGN KEY (`DOCTOR_ID`) REFERENCES `doctors` (`DOCTOR_ID`),
  CONSTRAINT `med_data_chk_1` CHECK (((length(`PATIENT_SSN`) = 9) and regexp_like(`PATIENT_SSN`,_latin1'^[0-9]+$')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `med_data`
--

LOCK TABLES `med_data` WRITE;
/*!40000 ALTER TABLE `med_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `med_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training_data`
--

DROP TABLE IF EXISTS `training_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `training_data` (
  `DESCRIPTION` text,
  `MEDICAL_SPECIALTY` text,
  `SAMPLE_NAME` text,
  `TRANSCRIPTION` text,
  `KEYWORDS` text,
  `CONFIDENCE` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training_data`
--

LOCK TABLES `training_data` WRITE;
/*!40000 ALTER TABLE `training_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `training_data` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-28  2:27:16
