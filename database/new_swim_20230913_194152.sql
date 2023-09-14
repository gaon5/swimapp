-- MySQL dump 10.13  Distrib 5.6.50, for Linux (x86_64)
--
-- Host: localhost    Database: new_swim
-- ------------------------------------------------------
-- Server version	5.6.50-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `title_id` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `state` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`admin_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  CONSTRAINT `admin_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,2,1,'John','Smith','0220489124',1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_log`
--

DROP TABLE IF EXISTS `attendance_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attendance_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `pool_id` int(11) DEFAULT NULL,
  `attendance_date` date DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `member_id` (`member_id`),
  KEY `class_id` (`class_id`),
  KEY `attendance_log_ibfk_3_idx` (`pool_id`),
  CONSTRAINT `attendance_log_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`),
  CONSTRAINT `attendance_log_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `book_class_list` (`book_class_id`),
  CONSTRAINT `attendance_log_ibfk_3` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`pool_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_log`
--

LOCK TABLES `attendance_log` WRITE;
/*!40000 ALTER TABLE `attendance_log` DISABLE KEYS */;
INSERT INTO `attendance_log` VALUES (3,26,149,1,'2023-09-13'),(6,2,92,4,'2023-09-13'),(7,3,92,4,'2023-09-13'),(8,4,90,4,'2023-09-13'),(9,1,92,4,'2023-09-13');
/*!40000 ALTER TABLE `attendance_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `available_time`
--

DROP TABLE IF EXISTS `available_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `available_time` (
  `available_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  PRIMARY KEY (`available_id`),
  KEY `foreign1_idx` (`user_id`),
  CONSTRAINT `foreign1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_time`
--

LOCK TABLES `available_time` WRITE;
/*!40000 ALTER TABLE `available_time` DISABLE KEYS */;
INSERT INTO `available_time` VALUES (4,3,'2023-09-19','06:00:00','20:00:00'),(5,3,'2023-09-22','12:00:00','20:00:00'),(7,3,'2023-09-08','06:00:00','20:00:00'),(8,3,'2023-09-07','06:00:00','20:00:00'),(11,3,'2023-09-14','06:00:00','20:00:00');
/*!40000 ALTER TABLE `available_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_class_list`
--

DROP TABLE IF EXISTS `book_class_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_class_list` (
  `book_class_id` int(11) NOT NULL AUTO_INCREMENT,
  `instructor_id` int(11) DEFAULT NULL,
  `pool_id` int(11) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `class_date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `detailed_information` text,
  `is_individual` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`book_class_id`),
  KEY `instructor_id` (`instructor_id`),
  KEY `pool_id` (`pool_id`),
  KEY `book_class_list_class_list_class_id_fk` (`class_id`),
  CONSTRAINT `book_class_list_class_list_class_id_fk` FOREIGN KEY (`class_id`) REFERENCES `class_list` (`class_id`),
  CONSTRAINT `book_class_list_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `book_class_list_ibfk_2` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`pool_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_class_list`
--

LOCK TABLES `book_class_list` WRITE;
/*!40000 ALTER TABLE `book_class_list` DISABLE KEYS */;
INSERT INTO `book_class_list` VALUES (61,9,4,2,'2023-09-07','07:00:00','08:00:00','',0),(62,1,4,7,'2023-09-04','08:30:00','09:30:00','High-impact class!',0),(63,4,3,3,'2023-09-05','06:00:00','07:00:00','',0),(64,5,4,8,'2023-09-06','08:00:00','09:00:00','Sweat it out by dancing!',0),(65,8,4,11,'2023-09-07','10:00:00','11:00:00','',0),(67,9,4,5,'2023-09-05','10:30:00','11:30:00','',0),(68,10,4,4,'2023-09-08','06:30:00','07:30:00','',0),(70,9,4,10,'2023-09-08','10:00:00','11:00:00','',0),(71,5,3,6,'2023-09-04','12:00:00','13:00:00','',0),(72,7,3,3,'2023-09-04','14:30:00','15:30:00','',0),(73,4,4,7,'2023-09-04','17:00:00','18:00:00','',0),(74,2,4,9,'2023-09-05','14:00:00','15:00:00','',0),(75,7,3,3,'2023-09-05','18:30:00','19:30:00','',0),(76,3,4,2,'2023-09-06','12:30:00','13:30:00','',0),(77,10,4,11,'2023-09-06','15:30:00','16:30:00','',0),(78,5,4,8,'2023-09-07','14:00:00','15:00:00','',0),(79,3,3,4,'2023-09-07','16:30:00','17:30:00','',0),(80,6,4,8,'2023-09-08','13:00:00','14:00:00','',0),(81,6,4,2,'2023-09-08','19:00:00','20:00:00','',0),(83,10,4,6,'2023-09-09','14:00:00','15:00:00','',0),(84,5,3,5,'2023-09-09','17:00:00','18:00:00','',0),(85,7,3,5,'2023-09-10','08:30:00','09:30:00','',0),(86,2,4,7,'2023-09-10','12:30:00','13:30:00','',0),(87,8,4,3,'2023-09-10','16:00:00','17:00:00','',0),(88,1,3,4,'2023-09-09','11:00:00','12:00:00','',0),(89,6,3,2,'2023-09-11','07:00:00','08:00:00','',0),(90,1,4,5,'2023-09-12','09:00:00','10:00:00','',0),(91,10,4,7,'2023-09-11','10:00:00','11:00:00','',0),(92,1,4,10,'2023-09-12','13:00:00','14:00:00','',0),(93,4,4,9,'2023-09-11','15:00:00','16:00:00','',0),(94,3,4,2,'2023-09-12','17:30:00','18:30:00','',0),(95,5,3,6,'2023-09-13','06:00:00','07:00:00','',0),(96,8,4,8,'2023-09-13','08:00:00','09:00:00','',0),(97,6,3,10,'2023-09-13','11:30:00','12:30:00','',0),(98,7,3,4,'2023-09-13','16:00:00','17:00:00','',0),(99,9,4,7,'2023-09-14','19:00:00','20:00:00','',0),(100,2,4,11,'2023-09-14','07:00:00','08:00:00','',0),(101,4,3,6,'2023-09-14','10:00:00','11:00:00','',0),(102,8,3,8,'2023-09-14','14:00:00','15:00:00','',0),(103,3,3,4,'2023-09-15','15:00:00','16:00:00','',0),(104,7,4,9,'2023-09-15','12:00:00','13:00:00','',0),(105,9,4,10,'2023-09-15','17:00:00','18:00:00','',0),(106,3,3,3,'2023-09-16','15:00:00','16:00:00','',0),(107,3,4,6,'2023-09-16','10:30:00','11:30:00','',0),(108,3,3,8,'2023-09-16','17:00:00','18:00:00','',0),(109,3,4,5,'2023-09-17','12:00:00','13:00:00','',0),(110,8,3,11,'2023-09-17','16:30:00','17:30:00','',0),(111,1,3,2,'2023-09-18','06:00:00','07:00:00','',0),(112,3,4,3,'2023-09-18','10:00:00','11:00:00','',0),(113,5,4,4,'2023-09-18','14:00:00','15:00:00','',0),(114,7,3,5,'2023-09-18','17:30:00','18:30:00','',0),(115,9,3,6,'2023-09-19','07:30:00','08:30:00','',0),(116,2,3,3,'2023-09-19','09:30:00','10:30:00','',0),(117,4,4,7,'2023-09-19','15:00:00','16:00:00','',0),(118,6,3,8,'2023-09-20','11:30:00','12:30:00','',0),(119,8,4,10,'2023-09-20','08:30:00','09:30:00','',0),(120,10,3,11,'2023-09-20','18:30:00','19:30:00','',0),(121,1,3,10,'2023-09-21','13:30:00','14:30:00','',0),(122,3,4,3,'2023-09-21','16:30:00','17:30:00','',0),(123,5,3,9,'2023-09-21','07:00:00','08:00:00','',0),(124,5,4,3,'2023-09-22','08:30:00','09:30:00','',0),(125,7,4,5,'2023-09-22','10:30:00','11:30:00','',0),(126,9,4,6,'2023-09-22','15:00:00','16:00:00','',0),(127,2,3,9,'2023-09-23','17:30:00','18:30:00','',0),(128,4,4,7,'2023-09-23','13:00:00','14:00:00','',0),(129,6,3,8,'2023-09-23','07:00:00','08:00:00','',0),(130,8,4,10,'2023-09-24','09:00:00','10:00:00','',0),(131,1,4,9,'2023-09-17','13:00:00','14:00:00','',0),(132,10,3,2,'2023-09-24','15:00:00','16:00:00','',0),(133,8,1,1,'2023-09-17','07:00:00','07:30:00',NULL,1),(134,5,2,1,'2023-09-16','07:00:00','07:30:00',NULL,1),(135,5,2,1,'2023-09-15','07:00:00','08:00:00',NULL,1),(136,3,1,1,'2023-09-13','07:30:00','08:00:00',NULL,1),(137,7,3,1,'2023-09-13','10:00:00','11:00:00',NULL,1),(138,7,3,1,'2023-09-14','08:30:00','09:30:00',NULL,1),(139,9,4,1,'2023-09-15','06:30:00','07:00:00',NULL,1),(140,8,1,1,'2023-09-17','09:00:00','09:30:00',NULL,1),(141,4,4,1,'2023-09-15','08:30:00','09:00:00',NULL,1),(142,2,3,1,'2023-09-15','07:30:00','08:00:00',NULL,1),(143,4,3,1,'2023-09-16','06:00:00','07:00:00',NULL,1),(144,6,2,1,'2023-09-15','07:00:00','07:30:00',NULL,1),(145,1,1,1,'2023-09-15','09:30:00','10:00:00',NULL,1),(146,7,2,1,'2023-09-15','07:00:00','07:30:00',NULL,1),(147,2,4,1,'2023-09-15','07:00:00','08:00:00',NULL,1),(148,3,2,1,'2023-09-16','07:00:00','07:30:00',NULL,1),(149,1,1,1,'2023-09-15','12:00:00','13:00:00',NULL,1),(150,3,2,1,'2023-09-15','09:00:00','09:30:00',NULL,1),(151,9,3,1,'2023-09-15','12:00:00','12:30:00',NULL,1),(152,3,3,1,'2023-09-17','09:00:00','09:30:00',NULL,1),(153,7,2,1,'2023-09-16','08:00:00','09:00:00',NULL,1),(154,9,3,1,'2023-09-15','08:30:00','09:00:00',NULL,1),(155,4,1,1,'2023-09-17','08:30:00','09:30:00',NULL,1),(156,8,4,1,'2023-09-15','06:30:00','07:30:00',NULL,1);
/*!40000 ALTER TABLE `book_class_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_list`
--

DROP TABLE IF EXISTS `book_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_list` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `pool_id` int(11) DEFAULT NULL,
  `payment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  KEY `member_id` (`member_id`),
  KEY `class_id` (`class_id`),
  KEY `instructor_id` (`instructor_id`),
  KEY `pool_id` (`pool_id`),
  KEY `payment_id` (`payment_id`),
  CONSTRAINT `book_list_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`),
  CONSTRAINT `book_list_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `book_class_list` (`book_class_id`),
  CONSTRAINT `book_list_ibfk_3` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`),
  CONSTRAINT `book_list_ibfk_4` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`pool_id`),
  CONSTRAINT `book_list_ibfk_5` FOREIGN KEY (`payment_id`) REFERENCES `payment_list` (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_list`
--

LOCK TABLES `book_list` WRITE;
/*!40000 ALTER TABLE `book_list` DISABLE KEYS */;
INSERT INTO `book_list` VALUES (2,46,103,5,3,NULL),(3,46,100,2,4,NULL),(4,46,133,8,1,4),(5,1,134,5,2,6),(7,1,135,5,2,7),(8,2,95,5,3,NULL),(9,2,136,3,1,9),(10,2,100,2,4,NULL),(11,2,97,6,3,NULL),(12,2,101,4,3,NULL),(13,2,137,7,3,10),(14,2,138,7,3,11),(15,3,139,9,4,13),(16,3,103,5,3,NULL),(17,9,106,10,3,NULL),(18,9,140,8,1,15),(19,8,100,2,4,NULL),(20,8,141,4,4,17),(21,7,103,5,3,NULL),(22,6,103,5,3,NULL),(23,6,142,2,3,20),(24,6,106,10,3,NULL),(25,5,106,10,3,NULL),(26,5,103,5,3,NULL),(27,4,103,5,3,NULL),(28,4,104,7,4,NULL),(29,22,103,5,3,NULL),(30,22,108,10,3,NULL),(31,20,103,5,3,NULL),(32,20,104,7,4,NULL),(33,20,143,4,3,25),(34,11,103,5,3,NULL),(35,11,101,4,3,NULL),(36,12,103,5,3,NULL),(37,12,131,1,4,NULL),(38,12,144,6,2,28),(39,13,102,8,3,NULL),(40,13,103,5,3,NULL),(41,13,145,1,1,30),(42,24,103,5,3,NULL),(43,24,100,2,4,NULL),(44,24,146,7,2,32),(45,25,103,5,3,NULL),(46,25,104,7,4,NULL),(47,25,147,2,4,34),(48,26,103,5,3,NULL),(49,26,148,3,2,36),(50,26,101,4,3,NULL),(51,26,149,1,1,37),(52,27,103,5,3,NULL),(53,27,100,2,4,NULL),(54,27,150,3,2,39),(55,28,103,5,3,NULL),(56,28,151,9,3,41),(57,28,97,6,3,NULL),(58,28,102,8,3,NULL),(59,29,103,5,3,NULL),(60,29,152,3,3,43),(61,29,109,2,4,NULL),(62,30,106,10,3,NULL),(63,30,104,7,4,NULL),(64,30,103,5,3,NULL),(65,31,103,5,3,NULL),(66,31,106,10,3,NULL),(67,33,103,5,3,NULL),(68,33,107,3,4,NULL),(69,34,131,1,4,NULL),(70,34,103,5,3,NULL),(71,35,103,5,3,NULL),(72,35,104,7,4,NULL),(73,36,103,5,3,NULL),(74,36,108,10,3,NULL),(75,37,103,5,3,NULL),(76,37,106,10,3,NULL),(77,38,103,5,3,NULL),(78,38,105,9,4,NULL),(79,39,103,5,3,NULL),(80,39,108,10,3,NULL),(81,39,110,8,3,NULL),(82,40,103,5,3,NULL),(83,40,110,8,3,NULL),(84,40,107,3,4,NULL),(85,40,153,7,2,54),(86,19,103,5,3,NULL),(87,19,107,3,4,NULL),(88,19,106,10,3,NULL),(89,19,154,9,3,56),(90,18,103,5,3,NULL),(91,18,109,2,4,NULL),(92,18,104,7,4,NULL),(93,17,106,10,3,NULL),(94,17,109,2,4,NULL),(95,17,131,1,4,NULL),(96,17,155,4,1,59),(97,1,97,6,3,NULL),(98,1,95,5,3,NULL),(100,2,92,1,4,NULL),(101,3,92,1,4,NULL),(102,1,90,1,4,NULL),(103,4,90,1,4,NULL),(104,1,92,1,4,NULL),(106,49,156,8,4,63);
/*!40000 ALTER TABLE `book_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `region_id` int(11) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`city_id`),
  KEY `city_id` (`region_id`),
  CONSTRAINT `city_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (1,1,'Dargaville'),(2,1,'Kaikohe'),(3,1,'Kaitaia'),(4,1,'Kawakawa'),(5,1,'Kerikeri'),(6,1,'Mangawhai'),(7,1,'Maungaturoto'),(8,1,'Paihia'),(9,1,'Whangarei'),(10,2,'Albany'),(11,2,'Auckland City'),(12,2,'Botany Downs'),(13,2,'Clevedon'),(14,2,'Franklin'),(15,2,'Great Barrier Island'),(16,2,'Helensville'),(17,2,'Henderson'),(18,2,'Hibiscus Coast'),(19,2,'Kumeu'),(20,2,'Mangere'),(21,2,'Manukau'),(22,2,'New Lynn'),(23,2,'North Shore'),(24,2,'Onehunga'),(25,2,'Papakura'),(26,2,'Pukekohe'),(27,2,'Remuera'),(28,2,'Waiheke Island'),(29,2,'Waitakere'),(30,2,'Waiuku'),(31,2,'Warkworth'),(32,2,'Wellsford'),(33,3,'Cambridge'),(34,3,'Coromandel'),(35,3,'Hamilton'),(36,3,'Huntly'),(37,3,'Matamata'),(38,3,'Morrinsville'),(39,3,'Ngaruawahia'),(40,3,'Ngatea'),(41,3,'Otorohanga'),(42,3,'Paeroa'),(43,3,'Raglan'),(44,3,'Taumarunui'),(45,3,'Taupo'),(46,3,'Te Awamutu'),(47,3,'Te Kuiti'),(48,3,'Thames'),(49,3,'Tokoroa/Putaruru'),(50,3,'Turangi '),(51,3,'Waihi'),(52,3,'Whangamata'),(53,3,'Whitianga'),(54,4,'Katikati'),(55,4,'Kawerau'),(56,4,'Mt. Maunganui'),(57,4,'Opotiki'),(58,4,'Papamoa'),(59,4,'Rotorua'),(60,4,'Tauranga'),(61,4,'Te Puke'),(62,4,'Waihi Beach'),(63,4,'Whakatane'),(64,5,'Gisborne'),(65,5,'Ruatoria'),(66,6,'Hastings'),(67,6,'Napier'),(68,6,'Waipukurau'),(69,6,'Wairoa'),(70,7,'Hawera'),(71,7,'Mokau'),(72,7,'New Plymouth'),(73,7,'Opunake'),(74,7,'Stratford'),(75,8,'Ohakune'),(76,8,'Taihape'),(77,8,'Waiouru'),(78,8,'Whanganui'),(79,8,'Bulls'),(80,8,'Dannevirke'),(81,8,'Feilding'),(82,8,'Levin'),(83,8,'Manawatu'),(84,8,'Marton'),(85,8,'Pahiatua'),(86,8,'Palmerston North'),(87,8,'Woodville'),(88,9,'Kapiti'),(89,9,'Lower Hutt City'),(90,9,'Porirua'),(91,9,'Upper Hutt City'),(92,9,'Wellington City'),(93,10,'Golden Bay'),(94,10,'Motueka'),(95,10,'Murchison'),(96,10,'Nelson'),(97,11,'Blenheim'),(98,11,'Marlborough Sounds'),(99,11,'Picton'),(100,12,'Greymouth'),(101,12,'Hokitika'),(102,12,'Westport'),(103,13,'Akaroa'),(104,13,'Amberley'),(105,13,'Ashburton'),(106,13,'Belfast'),(107,13,'Cheviot'),(108,13,'Christchurch City'),(109,13,'Darfield'),(110,13,'Fairlie'),(111,13,'Ferrymead'),(112,13,'Geraldine'),(113,13,'Halswell'),(114,13,'Hanmer Springs'),(115,13,'Kaiapoi'),(116,13,'Kaikoura'),(117,13,'Lyttelton'),(118,13,'Mt Cook'),(119,13,'Rangiora'),(120,13,'Rolleston'),(121,13,'Selwyn'),(122,14,'Kurow'),(123,14,'Oamaru'),(124,14,'Timaru'),(125,14,'Twizel'),(126,14,'Waimate'),(127,15,'Alexandra'),(128,15,'Balclutha'),(129,15,'Cromwell'),(130,15,'Dunedin'),(131,15,'Lawrence'),(132,15,'Milton'),(133,15,'Palmerston'),(134,15,'Queenstown'),(135,15,'Ranfurly'),(136,15,'Roxburgh'),(137,15,'Tapanui'),(138,15,'Wanaka'),(139,16,'Bluff'),(140,16,'Edendale'),(141,16,'Gore'),(142,16,'Invercargill'),(143,16,'Lumsden'),(144,16,'Otautau'),(145,16,'Riverton'),(146,16,'Stewart Island'),(147,16,'Te Anau'),(148,16,'Tokanui'),(149,16,'Winton');
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_list`
--

DROP TABLE IF EXISTS `class_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_list` (
  `class_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_list`
--

LOCK TABLES `class_list` WRITE;
/*!40000 ALTER TABLE `class_list` DISABLE KEYS */;
INSERT INTO `class_list` VALUES (1,'Individual Lesson'),(2,'Aqua Aerobics'),(3,'Water Yoga'),(4,'Hydro Tone'),(5,'Aqua Deep'),(6,'Hydro Health'),(7,'Aqua Combat'),(8,'Aqua Zumba'),(9,'Aqua Jogging'),(10,'Aqua Cardio Blast'),(11,'Aqua Pilates'),(12,'Aqua Running');
/*!40000 ALTER TABLE `class_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instructor` (
  `instructor_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `title_id` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `detailed_information` text,
  `state` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`instructor_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  CONSTRAINT `instructor_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

LOCK TABLES `instructor` WRITE;
/*!40000 ALTER TABLE `instructor` DISABLE KEYS */;
INSERT INTO `instructor` VALUES (1,3,1,'Nicholas','Smith','021526534','Hi I am Nicholas',1),(2,4,2,'Emily','Johnson','02023456789','Detailed info for instructor 2',1),(3,5,1,'Michael','Brown','02034567890','Detailed info for instructor 3',1),(4,6,2,'Sarah','Davis','02045678901','Detailed info for instructor 4',1),(5,7,1,'David','Wilson','02056789012',' Info for instructor 5',1),(6,8,2,'Jessica','Martinez','02067890123','Detailed info for instructor 6',1),(7,9,1,'Daniel','Jones','02078901234','Detailed info for instructor 7',1),(8,10,2,'Olivia','Taylor','02089012345','Detailed info for instructor 8',1),(9,11,1,'Christopher','Anderson','02090123456','Detailed info for instructor 9',1),(10,12,2,'Sophia','White','02001234567','Detailed info for instructor 10',1),(16,151,1,'Jamieson','Papatoie','0220578841',NULL,0),(17,155,1,'Poer','Eorpw','0330592454',NULL,1);
/*!40000 ALTER TABLE `instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member` (
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `title_id` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `detailed_information` text,
  `city_id` int(11) DEFAULT NULL,
  `region_id` int(11) DEFAULT NULL,
  `street_name` varchar(255) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `health_information` text,
  `state` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`member_id`),
  KEY `user_id` (`user_id`),
  KEY `title_id` (`title_id`),
  KEY `city_id` (`city_id`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `member_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
  CONSTRAINT `member_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`),
  CONSTRAINT `member_ibfk_3` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`),
  CONSTRAINT `member_region_region_id_fk` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,13,1,'David','Jones','0213456734','None',2,1,'1, sample street','2020-02-04','None',1),(2,14,1,'Emma','Smith','0204567890',NULL,2,1,'2, sample street','2019-03-15',NULL,1),(3,15,1,'Sophia','Johnson','0205678901',NULL,2,1,'3, sample street','2018-04-26',NULL,1),(4,16,1,'Liam','Brown','0206789012',NULL,2,1,'4, sample street','2017-05-07',NULL,1),(5,17,1,'Olivia','Davis','0207890123',NULL,2,1,'5, sample street','2016-06-18',NULL,1),(6,18,1,'Noah','Wilson','0208901234',NULL,2,1,'6, sample street','2015-07-29',NULL,1),(7,19,1,'Ava','Martinez','0209012345',NULL,2,1,'7, sample street','2014-08-10',NULL,1),(8,20,1,'Mia','Jones','0200123456',NULL,2,1,'8, sample street','2013-09-21',NULL,1),(9,21,1,'Ethan','Anderson','0201234567',NULL,2,1,'9, sample street','2012-10-02',NULL,1),(10,22,1,'Isabella','White','0202345678',NULL,2,1,'10, sample street','2011-11-13',NULL,1),(11,23,1,'William','Smith','0203456789',NULL,2,1,'11, sample street','2010-12-24',NULL,1),(12,24,1,'Sophia','Johnson','0204567890',NULL,2,1,'12, sample street','2009-01-04',NULL,1),(13,25,1,'Liam','Brown','0205678901',NULL,2,1,'13, sample street','2008-02-15',NULL,1),(14,26,1,'Olivia','Davis','0206789012',NULL,2,1,'14, sample street','2007-03-28',NULL,1),(15,27,1,'Noah','Wilson','0207890123',NULL,2,1,'15, sample street','2006-04-08',NULL,1),(16,28,1,'Ava','Martinez','0208901234',NULL,2,1,'16, sample street','2005-05-19',NULL,1),(17,29,1,'Mia','Jones','0209012345',NULL,2,1,'17, sample street','2004-06-30',NULL,1),(18,30,1,'Ethan','Anderson','0200123456',NULL,2,1,'18, sample street','2003-08-11',NULL,1),(19,31,1,'Isabella','White','0201234567',NULL,2,1,'19, sample street','2002-09-22',NULL,1),(20,32,1,'William','Smith','0202345678',NULL,2,1,'20, sample street','2001-11-03',NULL,1),(21,33,1,'Sophia','Johnson','0203456789',NULL,2,1,'21, sample street','2000-12-14',NULL,1),(22,34,1,'Liam','Brown','0204567890',NULL,2,1,'22, sample street','1999-01-25',NULL,1),(23,35,1,'Olivia','Davis','0205678901',NULL,2,1,'23, sample street','1998-03-07',NULL,1),(24,36,1,'Noah','Wilson','0206789012',NULL,2,1,'24, sample street','1997-04-18',NULL,1),(25,37,1,'Ava','Martinez','0207890123',NULL,2,1,'25, sample street','1996-05-30',NULL,1),(26,38,1,'Mia','Jones','0208901234',NULL,2,1,'26, sample street','1995-07-10',NULL,1),(27,39,1,'Ethan','Anderson','0209012345',NULL,2,1,'27, sample street','1994-08-21',NULL,1),(28,40,1,'Isabella','White','0200123456',NULL,2,1,'28, sample street','1993-09-01',NULL,1),(29,41,1,'William','Smith','0201234567',NULL,2,1,'29, sample street','1992-10-12',NULL,1),(30,42,1,'Sophia','Johnson','0202345678',NULL,2,1,'30, sample street','1991-11-23',NULL,1),(31,43,1,'Liam','Brown','0203456789',NULL,2,1,'31, sample street','1990-12-04',NULL,1),(32,44,1,'Olivia','Davis','0204567890',NULL,2,1,'32, sample street','1989-01-15',NULL,0),(33,45,1,'Noah','Wilson','0205678901',NULL,2,1,'33, sample street','1988-02-26',NULL,1),(34,46,1,'Ava','Martinez','0206789012',NULL,2,1,'34, sample street','1987-04-07',NULL,1),(35,47,1,'Mia','Jones','0207890123',NULL,2,1,'35, sample street','1986-05-18',NULL,1),(36,48,1,'Ethan','Anderson','0208901234',NULL,2,1,'36, sample street','1985-06-29',NULL,1),(37,49,1,'Isabella','White','0209012345',NULL,2,1,'37, sample street','1984-08-10',NULL,1),(38,50,1,'William','Smith','0200123456',NULL,2,1,'38, sample street','1983-09-21',NULL,1),(39,51,1,'Sophia','Johnson','0201234567',NULL,2,1,'39, sample street','1982-11-01',NULL,1),(40,52,1,'Liam','Brown','0202345678',NULL,2,1,'40, sample street','1981-12-12',NULL,1),(46,150,1,'Na','Gao','0273889725','',121,13,'5, Marble Court','2023-09-03','',1),(47,152,1,'Agent','Nick','021526533',NULL,108,13,'211 Wainoni Road','2001-02-22',NULL,1),(48,153,3,'Jamieson','Yasip','0220464891',NULL,121,13,'23, Bannab St','1999-09-03',NULL,1),(49,154,2,'Na','Gao','0283889725','None',121,13,'5 MARBLE COURT','2023-09-01','None',1);
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `news` text,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`news_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES (3,'Welcome to Waikirikiri Swim Centre! Hope to see everyone soon.','2023-09-12 23:37:05'),(4,'Try out our different pools or attend one of the classes we have to offer.','2023-09-12 23:42:05'),(5,' Here to share important water safety reminders, especially during the summer months, to ensure that everyone enjoys the pool responsibly.','2023-09-12 23:42:27'),(6,'Enjoy the weekend with the family at Waikirikiri Swim Centre. ','2023-09-13 00:42:44'),(8,'Remember these tips: The area close by a pool is often slippery – so walk, don\'t run, around the pool. Always obey the pool\'s safety rules and listen to the instructions of lifeguards. Play it safe.','2023-09-13 00:44:00'),(9,'We also offer individual lessons so you can have uninterrupted attention from your instructor.','2023-09-13 00:45:48'),(11,'welcome to swim centre!','2023-09-13 21:54:11');
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_due`
--

DROP TABLE IF EXISTS `payment_due`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_due` (
  `due_id` int(11) NOT NULL AUTO_INCREMENT,
  `payment_id` int(11) DEFAULT NULL,
  `member_id` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`due_id`),
  KEY `payment_due_member_member_id_fk` (`member_id`),
  KEY `payment_due_payment_list_payment_id_fk` (`payment_id`),
  CONSTRAINT `payment_due_member_member_id_fk` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`),
  CONSTRAINT `payment_due_payment_list_payment_id_fk` FOREIGN KEY (`payment_id`) REFERENCES `payment_list` (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_due`
--

LOCK TABLES `payment_due` WRITE;
/*!40000 ALTER TABLE `payment_due` DISABLE KEYS */;
INSERT INTO `payment_due` VALUES (2,3,46,'2023-09-13','2023-12-12'),(3,5,1,'2023-09-13','2024-03-11'),(4,8,2,'2023-09-13','2024-03-11'),(5,12,3,'2023-09-13','2024-03-11'),(6,14,9,'2023-09-13','2024-09-07'),(7,16,8,'2023-09-13','2023-12-12'),(8,18,7,'2023-09-13','2023-10-13'),(9,19,6,'2023-09-13','2024-03-11'),(10,21,5,'2023-09-13','2024-03-11'),(11,22,4,'2023-09-13','2023-12-12'),(12,23,22,'2023-09-13','2024-03-11'),(13,24,20,'2023-09-13','2024-09-07'),(14,26,11,'2023-09-13','2024-03-11'),(15,27,12,'2023-09-13','2023-12-12'),(16,29,13,'2023-09-13','2024-03-11'),(17,31,24,'2023-09-13','2024-03-11'),(18,33,25,'2023-09-13','2024-03-11'),(19,35,26,'2023-09-13','2024-09-07'),(20,38,27,'2023-08-19','2023-09-19'),(21,40,28,'2023-09-13','2024-03-11'),(22,42,29,'2023-09-13','2023-12-12'),(23,44,30,'2023-09-13','2024-03-11'),(24,45,31,'2023-09-13','2024-03-11'),(25,46,33,'2023-09-13','2024-09-07'),(26,47,34,'2023-09-13','2023-12-12'),(27,48,35,'2023-09-13','2024-03-11'),(28,49,36,'2023-09-13','2024-03-11'),(29,50,37,'2023-09-13','2024-03-11'),(30,51,38,'2023-09-13','2024-03-11'),(31,52,39,'2023-09-13','2024-09-07'),(32,53,40,'2023-09-13','2024-03-11'),(33,55,19,'2023-09-13','2024-03-11'),(34,57,18,'2023-09-13','2024-03-11'),(35,58,17,'2023-09-13','2024-03-11'),(36,60,16,'2023-08-18','2023-09-18'),(37,61,15,'2023-08-01','2023-09-01'),(38,62,49,'2023-09-13','2024-01-11'),(39,65,10,'2023-08-04','2023-09-04');
/*!40000 ALTER TABLE `payment_due` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_list`
--

DROP TABLE IF EXISTS `payment_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_list` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_type` varchar(50) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `payment_list_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_list`
--

LOCK TABLES `payment_list` WRITE;
/*!40000 ALTER TABLE `payment_list` DISABLE KEYS */;
INSERT INTO `payment_list` VALUES (3,46,199.5,'2023-09-13','Membership','Master card'),(4,46,44,'2023-09-13','Lesson','Credit Card'),(5,1,378,'2023-09-13','Membership','Credit Card'),(6,1,44,'2023-09-13','Lesson','Credit Card'),(7,1,80,'2023-09-13','Lesson','Credit Card'),(8,2,378,'2023-09-13','Membership','Paypal'),(9,2,44,'2023-09-13','Lesson','Paypal'),(10,2,80,'2023-09-13','Lesson','Paypal'),(11,2,80,'2023-09-13','Lesson','Credit Card'),(12,3,378,'2023-09-13','Membership','Master card'),(13,3,44,'2023-09-13','Lesson','Credit Card'),(14,9,714,'2023-09-13','Membership','Master card'),(15,9,44,'2023-09-13','Lesson','Master card'),(16,8,199.5,'2023-09-13','Membership','Credit Card'),(17,8,44,'2023-09-13','Lesson','Credit Card'),(18,7,70,'2023-09-13','Membership','Master card'),(19,6,378,'2023-09-13','Membership','Credit Card'),(20,6,44,'2023-09-13','Lesson','Credit Card'),(21,5,378,'2023-09-13','Membership','Master card'),(22,4,199.5,'2023-09-13','Membership','Paypal'),(23,22,378,'2023-09-13','Membership','Credit Card'),(24,20,714,'2023-09-13','Membership','Credit Card'),(25,20,80,'2023-09-13','Lesson','Credit Card'),(26,11,378,'2023-09-13','Membership','Master card'),(27,12,199.5,'2023-09-13','Membership','Paypal'),(28,12,44,'2023-09-13','Lesson','Credit Card'),(29,13,378,'2023-09-13','Membership','Credit Card'),(30,13,44,'2023-09-13','Lesson','Credit Card'),(31,24,378,'2023-09-13','Membership','Credit Card'),(32,24,44,'2023-09-13','Lesson','Credit Card'),(33,25,378,'2023-09-13','Membership','Master card'),(34,25,80,'2023-09-13','Lesson','Paypal'),(35,26,714,'2023-09-13','Membership','Master card'),(36,26,44,'2023-09-13','Lesson','Credit Card'),(37,26,80,'2023-09-13','Lesson','Master card'),(38,27,70,'2023-08-19','Membership','Credit Card'),(39,27,44,'2023-09-13','Lesson','Master card'),(40,28,378,'2023-09-13','Membership','Credit Card'),(41,28,44,'2023-09-13','Lesson','Credit Card'),(42,29,199.5,'2023-09-13','Membership','Master card'),(43,29,44,'2023-09-13','Lesson','Credit Card'),(44,30,378,'2023-09-13','Membership','Paypal'),(45,31,378,'2023-09-13','Membership','Credit Card'),(46,33,714,'2023-09-13','Membership','Master card'),(47,34,199.5,'2023-09-13','Membership','Credit Card'),(48,35,378,'2023-09-13','Membership','Master card'),(49,36,378,'2023-09-13','Membership','Credit Card'),(50,37,378,'2023-09-13','Membership','Master card'),(51,38,378,'2023-09-13','Membership','Credit Card'),(52,39,714,'2023-09-13','Membership','Credit Card'),(53,40,378,'2023-09-13','Membership','Credit Card'),(54,40,80,'2023-09-13','Lesson','Credit Card'),(55,19,378,'2023-09-13','Membership','Credit Card'),(56,19,44,'2023-09-13','Lesson','Credit Card'),(57,18,378,'2023-09-13','Membership','Credit Card'),(58,17,378,'2023-09-13','Membership','Credit Card'),(59,17,80,'2023-09-13','Lesson','Master card'),(60,16,70,'2023-08-19','Membership','Credit Card'),(61,15,70,'2023-08-01','Membership','Credit Card'),(62,49,70,'2023-09-13','Membership','Master Card'),(63,49,80,'2023-09-13','Lesson','Paypal'),(64,49,199.5,'2023-09-13','Membership','Credit Card'),(65,10,70,'2023-08-04','Membership','Credit Card');
/*!40000 ALTER TABLE `payment_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pool`
--

DROP TABLE IF EXISTS `pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool` (
  `pool_id` int(11) NOT NULL AUTO_INCREMENT,
  `pool_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pool_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pool`
--

LOCK TABLES `pool` WRITE;
/*!40000 ALTER TABLE `pool` DISABLE KEYS */;
INSERT INTO `pool` VALUES (1,'Olympic Pool'),(2,'Family Pool'),(3,'Hydrotherapy Pool'),(4,'Training Pool');
/*!40000 ALTER TABLE `pool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region` (
  `region_id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Northland'),(2,'Auckland'),(3,'Waikato'),(4,'Bay Of Plenty'),(5,'Gisborne'),(6,'Hawke\'s Bay'),(7,'Taranaki'),(8,'Manawatu - Whanganui'),(9,'Wellington'),(10,'Nelson Bays'),(11,'Marlborough'),(12,'West Coast'),(13,'Canterbury'),(14,'Timaru - Oamaru'),(15,'Otago'),(16,'Southland');

UNLOCK TABLES;

--
-- Table structure for table `title`
--

DROP TABLE IF EXISTS `title`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `title` (
  `title_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`title_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `title`
--

LOCK TABLES `title` WRITE;
/*!40000 ALTER TABLE `title` DISABLE KEYS */;
INSERT INTO `title` VALUES (1,'Mr.'),(2,'Ms.'),(3,'Miss.');
/*!40000 ALTER TABLE `title` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_account`
--

DROP TABLE IF EXISTS `user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_account` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_member` tinyint(1) DEFAULT '0',
  `is_instructor` tinyint(1) DEFAULT '0',
  `is_admin` tinyint(1) DEFAULT '0',
  `is_root` tinyint(1) DEFAULT '0',
  `register_date` date DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_account`
--

LOCK TABLES `user_account` WRITE;
/*!40000 ALTER TABLE `user_account` DISABLE KEYS */;
INSERT INTO `user_account` VALUES (1,'root','root@root.com','$2b$12$rZ/oMfPkT9q16IWgGJ9n6.e5xynS7f9elfPmPiR.TbEBo2yTkc2Dq',0,0,0,1,'2023-08-08'),(2,'admin1','admin1@swim.com','$2b$12$Nah0JJ/68QX.UTzOoTUoh.zthmvCeDobEu006434MIgvuBd7iSX66',0,0,1,0,'2023-08-08'),(3,'instructor1','instructor1@swim.com','$2b$12$oDXQCoNIilAw3xPJzfnK5uNzhzKA6Tk7CXuJJGljVgHdOF3wEyjie',0,1,0,0,'2023-09-10'),(4,'instructor2','instructor2@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(5,'instructor3','instructor3@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(6,'instructor4','instructor4@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(7,'instructor5','instructor5@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(8,'instructor6','instructor6@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(9,'instructor7','instructor7@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(10,'instructor8','instructor8@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(11,'instructor9','instructor9@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(12,'instructor10','instructor10@swim.com','$2b$12$4zfnveSJ1R7W9lC8oxNN6eOPofK.SduImWEsTEkwTpYmFezu8RQou',0,1,0,0,'2023-09-10'),(13,'member1','mem1@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(14,'member2','member2@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(15,'member3','member3@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(16,'member4','member4@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(17,'member5','member5@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(18,'member6','member6@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(19,'member7','member7@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(20,'member8','member8@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(21,'member9','member9@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(22,'member10','member10@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(23,'member11','member11@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(24,'member12','member12@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(25,'member13','member13@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(26,'member14','member14@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(27,'member15','member15@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(28,'member16','member16@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(29,'member17','member17@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(30,'member18','member18@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(31,'member19','member19@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(32,'member20','member20@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(33,'member21','member21@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(34,'member22','member22@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(35,'member23','member23@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(36,'member24','member24@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(37,'member25','member25@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(38,'member26','member26@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(39,'member27','member27@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(40,'member28','member28@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(41,'member29','member29@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(42,'member30','member30@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(43,'member31','member31@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(44,'member32','member32@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(45,'member33','member33@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(46,'member34','member34@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(47,'member35','member35@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(48,'member36','member36@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(49,'member37','member37@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(50,'member38','member38@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(51,'member39','member39@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(52,'member40','member40@swim.com','$2b$12$CbuXG.AGoavQsyLdcus9Teslj3bufsPnpXnxOITkLLg0fBYXKhOwS',1,0,0,0,'2023-09-10'),(150,'member1000','ASOR9319@GMAIL.COM','$2b$12$fiWA7phJhLegJghKZooHw.fidvtFehC0sL3bmqBGRn5W/GB4982XC',1,0,0,0,'2023-09-13'),(151,'popcorn','jamieson@swim.come','$2b$12$uqCt1agNMAxeOkFwRN7GfOdgGqut3vcKB3aa3m0x9KWqyoFnfD/Je',0,1,0,0,'2023-09-13'),(152,'member47','nickyting222@gmail.com','$2b$12$rD3fqn0ml6eE/AABTCLfU.7.ZwvQ44u92XwxjBUB1KW7R8Ctr9gMi',1,0,0,0,'2023-09-13'),(153,'Peanut1','jamieson@gmail.com','$2b$12$1zSLk2ETdRL9LaFbM5MZJ.wo/6G9Hvu0/Lv250thefxtTor2.W6gu',1,0,0,0,'2023-09-13'),(154,'aquaCraze','ASOR9315@GMAIL.COM','$2b$12$YXETwCVjL5fG70tMs6IkJe71dE6yxpS.PG2zinmpbbT5m.QIMDVX6',1,0,0,0,'2023-09-13'),(155,'powt','powr@gmail.com','$2b$12$MGO/4aB6DnxoygpVTxYZQO04uOF/DNqVV2jm3jYEBLikrjF5cArra',0,1,0,0,'2023-09-13');
/*!40000 ALTER TABLE `user_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'new_swim'
--

--
-- Dumping routines for database 'new_swim'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-13 19:41:52
