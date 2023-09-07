-- MySQL dump 10.13  Distrib 5.6.50, for Linux (x86_64)
--
-- Host: localhost    Database: swimming
-- ------------------------------------------------------
-- Server version	5.6.50-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;
/*!40103 SET TIME_ZONE = '+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;
/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin`
(
    `admin_id`     int(11) NOT NULL AUTO_INCREMENT,
    `user_id`      int(11)      DEFAULT NULL,
    `title_id`     int(11)      DEFAULT NULL,
    `first_name`   varchar(255) DEFAULT NULL,
    `last_name`    varchar(255) DEFAULT NULL,
    `phone_number` varchar(255) DEFAULT NULL,
    `state`        tinyint(1)   DEFAULT '0',
    PRIMARY KEY (`admin_id`),
    KEY `user_id` (`user_id`),
    KEY `title_id` (`title_id`),
    CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
    CONSTRAINT `admin_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 2
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `attendance_log`
--

DROP TABLE IF EXISTS `attendance_log`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attendance_log`
(
    `log_id`          int(11) NOT NULL AUTO_INCREMENT,
    `member_id`       int(11) DEFAULT NULL,
    `class_id`        int(11) DEFAULT NULL,
    `pool_id`         int(11) DEFAULT NULL,
    `attendance_date` date    DEFAULT NULL,
    PRIMARY KEY (`log_id`),
    KEY `member_id` (`member_id`),
    KEY `class_id` (`class_id`),
    KEY `attendance_log_ibfk_3_idx` (`pool_id`),
    CONSTRAINT `attendance_log_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`),
    CONSTRAINT `attendance_log_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `book_class_list` (`book_class_id`),
    CONSTRAINT `attendance_log_ibfk_3` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`pool_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  AUTO_INCREMENT = 72
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `available_time`
--

DROP TABLE IF EXISTS `available_time`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `available_time`
(
    `available_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id`      int(11) NOT NULL,
    `date`         date DEFAULT NULL,
    `start_time`   time DEFAULT NULL,
    `end_time`     time DEFAULT NULL,
    PRIMARY KEY (`available_id`),
    KEY `foreign1_idx` (`user_id`),
    CONSTRAINT `foreign1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  AUTO_INCREMENT = 61
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `book_class_list`
--

DROP TABLE IF EXISTS `book_class_list`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_class_list`
(
    `book_class_id`        int(11) NOT NULL AUTO_INCREMENT,
    `instructor_id`        int(11)    DEFAULT NULL,
    `pool_id`              int(11)    DEFAULT NULL,
    `class_id`             int(11)    DEFAULT NULL,
    `class_date`           date       DEFAULT NULL,
    `start_time`           time       DEFAULT NULL,
    `end_time`             time       DEFAULT NULL,
    `detailed_information` text,
    `is_individual`        tinyint(1) DEFAULT '0',
    PRIMARY KEY (`book_class_id`),
    KEY `instructor_id` (`instructor_id`),
    KEY `pool_id` (`pool_id`),
    KEY `book_class_list_class_list_class_id_fk` (`class_id`),
    CONSTRAINT `book_class_list_class_list_class_id_fk` FOREIGN KEY (`class_id`) REFERENCES `class_list` (`class_id`),
    CONSTRAINT `book_class_list_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `book_class_list_ibfk_2` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`pool_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  AUTO_INCREMENT = 59
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `book_list`
--

DROP TABLE IF EXISTS `book_list`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_list`
(
    `book_id`       int(11) NOT NULL AUTO_INCREMENT,
    `member_id`     int(11) DEFAULT NULL,
    `class_id`      int(11) DEFAULT NULL,
    `instructor_id` int(11) DEFAULT NULL,
    `pool_id`       int(11) DEFAULT NULL,
    `payment_id`    int(11) DEFAULT NULL,
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
) ENGINE = InnoDB
  AUTO_INCREMENT = 40
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city`
(
    `city_id`   int(11) NOT NULL AUTO_INCREMENT,
    `region_id` int(11)      DEFAULT NULL,
    `city`      varchar(255) DEFAULT NULL,
    PRIMARY KEY (`city_id`),
    KEY `city_id` (`region_id`),
    CONSTRAINT `city_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  AUTO_INCREMENT = 150
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `class_list`
--

DROP TABLE IF EXISTS `class_list`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_list`
(
    `class_id`   int(11) NOT NULL AUTO_INCREMENT,
    `class_name` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`class_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 6
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instructor`
(
    `instructor_id`        int(11) NOT NULL AUTO_INCREMENT,
    `user_id`              int(11)      DEFAULT NULL,
    `title_id`             int(11)      DEFAULT NULL,
    `first_name`           varchar(255) DEFAULT NULL,
    `last_name`            varchar(255) DEFAULT NULL,
    `phone_number`         varchar(255) DEFAULT NULL,
    `detailed_information` text,
    `state`                tinyint(1)   DEFAULT '0',
    PRIMARY KEY (`instructor_id`),
    KEY `user_id` (`user_id`),
    KEY `title_id` (`title_id`),
    CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
    CONSTRAINT `instructor_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 4
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member`
(
    `member_id`            int(11) NOT NULL AUTO_INCREMENT,
    `user_id`              int(11)      DEFAULT NULL,
    `title_id`             int(11)      DEFAULT NULL,
    `first_name`           varchar(255) DEFAULT NULL,
    `last_name`            varchar(255) DEFAULT NULL,
    `phone_number`         varchar(255) DEFAULT NULL,
    `detailed_information` text,
    `city_id`              int(11)      DEFAULT NULL,
    `region_id`            int(11)      DEFAULT NULL,
    `street_name`          varchar(255) DEFAULT NULL,
    `birth_date`           date         DEFAULT NULL,
    `health_information`   text,
    `state`                tinyint(1)   DEFAULT '0',
    PRIMARY KEY (`member_id`),
    KEY `user_id` (`user_id`),
    KEY `title_id` (`title_id`),
    KEY `city_id` (`city_id`),
    KEY `region_id` (`region_id`),
    CONSTRAINT `member_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`user_id`),
    CONSTRAINT `member_ibfk_2` FOREIGN KEY (`title_id`) REFERENCES `title` (`title_id`),
    CONSTRAINT `member_ibfk_3` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`),
    CONSTRAINT `member_region_region_id_fk` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 44
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news`
(
    `news_id` int(11) NOT NULL AUTO_INCREMENT,
    `news`    text,
    `time`    datetime DEFAULT NULL,
    PRIMARY KEY (`news_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 30
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment_due`
--

DROP TABLE IF EXISTS `payment_due`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_due`
(
    `due_id`     int(11) NOT NULL AUTO_INCREMENT,
    `payment_id` int(11) DEFAULT NULL,
    `member_id`  int(11) NOT NULL,
    `start_date` date    DEFAULT NULL,
    `end_date`   date    DEFAULT NULL,
    PRIMARY KEY (`due_id`),
    KEY `payment_due_member_member_id_fk` (`member_id`),
    KEY `payment_due_payment_list_payment_id_fk` (`payment_id`),
    CONSTRAINT `payment_due_member_member_id_fk` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`),
    CONSTRAINT `payment_due_payment_list_payment_id_fk` FOREIGN KEY (`payment_id`) REFERENCES `payment_list` (`payment_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 34
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment_list`
--

DROP TABLE IF EXISTS `payment_list`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_list`
(
    `payment_id`     int(11)     NOT NULL AUTO_INCREMENT,
    `member_id`      int(11) DEFAULT NULL,
    `price`          float   DEFAULT NULL,
    `payment_date`   date    DEFAULT NULL,
    `payment_type`   varchar(50) NOT NULL,
    `payment_method` varchar(50) NOT NULL,
    PRIMARY KEY (`payment_id`),
    KEY `member_id` (`member_id`),
    CONSTRAINT `payment_list_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  AUTO_INCREMENT = 91
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool`
--

DROP TABLE IF EXISTS `pool`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool`
(
    `pool_id`   int(11) NOT NULL AUTO_INCREMENT,
    `pool_name` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`pool_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 4
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region`
(
    `region_id` int(11) NOT NULL AUTO_INCREMENT,
    `region`    varchar(255) DEFAULT NULL,
    PRIMARY KEY (`region_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 18
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title`
--

DROP TABLE IF EXISTS `title`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `title`
(
    `title_id` int(11) NOT NULL AUTO_INCREMENT,
    `title`    varchar(255) DEFAULT NULL,
    PRIMARY KEY (`title_id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 4
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_account`
--

DROP TABLE IF EXISTS `user_account`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_account`
(
    `user_id`       int(11)      NOT NULL AUTO_INCREMENT,
    `username`      varchar(100) NOT NULL,
    `email`         varchar(100) NOT NULL,
    `password`      varchar(255) NOT NULL,
    `is_member`     tinyint(1) DEFAULT '0',
    `is_instructor` tinyint(1) DEFAULT '0',
    `is_admin`      tinyint(1) DEFAULT '0',
    `is_root`       tinyint(1) DEFAULT '0',
    `register_date` date       DEFAULT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 50
  DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE = @OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE = @OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES = @OLD_SQL_NOTES */;

-- Dump completed on 2023-09-07 23:38:28


INSERT INTO `title` (`title_id`, `title`)
VALUES (1, 'Mr.'),
       (2, 'Ms.'),
       (3, 'Miss.');
INSERT INTO `pool` (`pool_id`, `pool_name`)
VALUES (1, 'pool');
INSERT INTO `class_list` (`class_id`, `class_name`)
VALUES (1, 'Individual Lesson'),
       (2, 'Aqua Aerobics'),
       (3, 'Water Yoga');
INSERT INTO `region` (`region_id`, `region`)
VALUES (1, 'Northland'),
       (2, 'Auckland'),
       (3, 'Waikato'),
       (4, 'Bay Of Plenty'),
       (5, 'Gisborne'),
       (6, 'Hawke''s Bay'),
       (7, 'Taranaki'),
       (8, 'Manawatu - Whanganui'),
       (9, 'Wellington'),
       (10, 'Nelson Bays'),
       (11, 'Marlborough'),
       (12, 'West Coast'),
       (13, 'Canterbury'),
       (14, 'Timaru - Oamaru'),
       (15, 'Otago'),
       (16, 'Southland');
INSERT INTO `city` (`city_id`, `region_id`, `city`)
VALUES (1, 1, 'Dargaville'),
       (2, 1, 'Kaikohe'),
       (3, 1, 'Kaitaia'),
       (4, 1, 'Kawakawa'),
       (5, 1, 'Kerikeri'),
       (6, 1, 'Mangawhai'),
       (7, 1, 'Maungaturoto'),
       (8, 1, 'Paihia'),
       (9, 1, 'Whangarei'),
       (10, 2, 'Albany'),
       (11, 2, 'Auckland City'),
       (12, 2, 'Botany Downs'),
       (13, 2, 'Clevedon'),
       (14, 2, 'Franklin'),
       (15, 2, 'Great Barrier Island'),
       (16, 2, 'Helensville'),
       (17, 2, 'Henderson'),
       (18, 2, 'Hibiscus Coast'),
       (19, 2, 'Kumeu'),
       (20, 2, 'Mangere'),
       (21, 2, 'Manukau'),
       (22, 2, 'New Lynn'),
       (23, 2, 'North Shore'),
       (24, 2, 'Onehunga'),
       (25, 2, 'Papakura'),
       (26, 2, 'Pukekohe'),
       (27, 2, 'Remuera'),
       (28, 2, 'Waiheke Island'),
       (29, 2, 'Waitakere'),
       (30, 2, 'Waiuku'),
       (31, 2, 'Warkworth'),
       (32, 2, 'Wellsford'),
       (33, 3, 'Cambridge'),
       (34, 3, 'Coromandel'),
       (35, 3, 'Hamilton'),
       (36, 3, 'Huntly'),
       (37, 3, 'Matamata'),
       (38, 3, 'Morrinsville'),
       (39, 3, 'Ngaruawahia'),
       (40, 3, 'Ngatea'),
       (41, 3, 'Otorohanga'),
       (42, 3, 'Paeroa'),
       (43, 3, 'Raglan'),
       (44, 3, 'Taumarunui'),
       (45, 3, 'Taupo'),
       (46, 3, 'Te Awamutu'),
       (47, 3, 'Te Kuiti'),
       (48, 3, 'Thames'),
       (49, 3, 'Tokoroa/Putaruru'),
       (50, 3, 'Turangi '),
       (51, 3, 'Waihi'),
       (52, 3, 'Whangamata'),
       (53, 3, 'Whitianga'),
       (54, 4, 'Katikati'),
       (55, 4, 'Kawerau'),
       (56, 4, 'Mt. Maunganui'),
       (57, 4, 'Opotiki'),
       (58, 4, 'Papamoa'),
       (59, 4, 'Rotorua'),
       (60, 4, 'Tauranga'),
       (61, 4, 'Te Puke'),
       (62, 4, 'Waihi Beach'),
       (63, 4, 'Whakatane'),
       (64, 5, 'Gisborne'),
       (65, 5, 'Ruatoria'),
       (66, 6, 'Hastings'),
       (67, 6, 'Napier'),
       (68, 6, 'Waipukurau'),
       (69, 6, 'Wairoa'),
       (70, 7, 'Hawera'),
       (71, 7, 'Mokau'),
       (72, 7, 'New Plymouth'),
       (73, 7, 'Opunake'),
       (74, 7, 'Stratford'),
       (75, 8, 'Ohakune'),
       (76, 8, 'Taihape'),
       (77, 8, 'Waiouru'),
       (78, 8, 'Whanganui'),
       (79, 8, 'Bulls'),
       (80, 8, 'Dannevirke'),
       (81, 8, 'Feilding'),
       (82, 8, 'Levin'),
       (83, 8, 'Manawatu'),
       (84, 8, 'Marton'),
       (85, 8, 'Pahiatua'),
       (86, 8, 'Palmerston North'),
       (87, 8, 'Woodville'),
       (88, 9, 'Kapiti'),
       (89, 9, 'Lower Hutt City'),
       (90, 9, 'Porirua'),
       (91, 9, 'Upper Hutt City'),
       (92, 9, 'Wellington City'),
       (93, 10, 'Golden Bay'),
       (94, 10, 'Motueka'),
       (95, 10, 'Murchison'),
       (96, 10, 'Nelson'),
       (97, 11, 'Blenheim'),
       (98, 11, 'Marlborough Sounds'),
       (99, 11, 'Picton'),
       (100, 12, 'Greymouth'),
       (101, 12, 'Hokitika'),
       (102, 12, 'Westport'),
       (103, 13, 'Akaroa'),
       (104, 13, 'Amberley'),
       (105, 13, 'Ashburton'),
       (106, 13, 'Belfast'),
       (107, 13, 'Cheviot'),
       (108, 13, 'Christchurch City'),
       (109, 13, 'Darfield'),
       (110, 13, 'Fairlie'),
       (111, 13, 'Ferrymead'),
       (112, 13, 'Geraldine'),
       (113, 13, 'Halswell'),
       (114, 13, 'Hanmer Springs'),
       (115, 13, 'Kaiapoi'),
       (116, 13, 'Kaikoura'),
       (117, 13, 'Lyttelton'),
       (118, 13, 'Mt Cook'),
       (119, 13, 'Rangiora'),
       (120, 13, 'Rolleston'),
       (121, 13, 'Selwyn'),
       (122, 14, 'Kurow'),
       (123, 14, 'Oamaru'),
       (124, 14, 'Timaru'),
       (125, 14, 'Twizel'),
       (126, 14, 'Waimate'),
       (127, 15, 'Alexandra'),
       (128, 15, 'Balclutha'),
       (129, 15, 'Cromwell'),
       (130, 15, 'Dunedin'),
       (131, 15, 'Lawrence'),
       (132, 15, 'Milton'),
       (133, 15, 'Palmerston'),
       (134, 15, 'Queenstown'),
       (135, 15, 'Ranfurly'),
       (136, 15, 'Roxburgh'),
       (137, 15, 'Tapanui'),
       (138, 15, 'Wanaka'),
       (139, 16, 'Bluff'),
       (140, 16, 'Edendale'),
       (141, 16, 'Gore'),
       (142, 16, 'Invercargill'),
       (143, 16, 'Lumsden'),
       (144, 16, 'Otautau'),
       (145, 16, 'Riverton'),
       (146, 16, 'Stewart Island'),
       (147, 16, 'Te Anau'),
       (148, 16, 'Tokanui'),
       (149, 16, 'Winton');
-- Insert a root user into the user_account table
INSERT INTO user_account (username, email, password, is_root, register_date)
VALUES ('root', 'root@root.com', '$2b$12$rZ/oMfPkT9q16IWgGJ9n6.e5xynS7f9elfPmPiR.TbEBo2yTkc2Dq', 1, "2023-08-08");
-- root/adminpassword

INSERT INTO user_account (username, email, password, is_admin, register_date)
VALUES ('admin1', 'admin1@swim.com', '$2b$12$rZ/oMfPkT9q16IWgGJ9n6.e5xynS7f9elfPmPiR.TbEBo2yTkc2Dq', 1, "2023-08-08");
-- admin1/adminpassword
