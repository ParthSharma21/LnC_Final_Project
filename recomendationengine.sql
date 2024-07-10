-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: recomendationengine
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cusinetypeenum`
--

DROP TABLE IF EXISTS `cusinetypeenum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cusinetypeenum` (
  `CusineTypeID` int NOT NULL AUTO_INCREMENT,
  `CusineTypeName` varchar(45) NOT NULL,
  PRIMARY KEY (`CusineTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cusinetypeenum`
--

LOCK TABLES `cusinetypeenum` WRITE;
/*!40000 ALTER TABLE `cusinetypeenum` DISABLE KEYS */;
INSERT INTO `cusinetypeenum` VALUES (1,'North Indian'),(2,'South Indian'),(3,'Other');
/*!40000 ALTER TABLE `cusinetypeenum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dailymenu`
--

DROP TABLE IF EXISTS `dailymenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dailymenu` (
  `FoodItemID` int NOT NULL AUTO_INCREMENT,
  `FoodItemName` varchar(45) DEFAULT NULL,
  `FoodItemPrice` int DEFAULT NULL,
  PRIMARY KEY (`FoodItemID`),
  CONSTRAINT `dailymenu_ibfk_1` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dailymenu`
--

LOCK TABLES `dailymenu` WRITE;
/*!40000 ALTER TABLE `dailymenu` DISABLE KEYS */;
INSERT INTO `dailymenu` VALUES (1,'Pav Bhaji',70),(2,'Roti Curry (2pcs)',40),(3,'Aloo Paratha',25),(6,'Pasta',40),(7,'Idli/Vada (2 pcs)',30);
/*!40000 ALTER TABLE `dailymenu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detailedfeedback`
--

DROP TABLE IF EXISTS `detailedfeedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detailedfeedback` (
  `DetailedFeedbackID` int NOT NULL AUTO_INCREMENT,
  `NotificationID` int NOT NULL,
  `UserID` int NOT NULL,
  `FoodItemID` int NOT NULL,
  `AnswerToQueID` int NOT NULL,
  `DetailedFeedback` varchar(255) NOT NULL,
  PRIMARY KEY (`DetailedFeedbackID`),
  KEY `NotificationID` (`NotificationID`),
  KEY `UserID` (`UserID`),
  KEY `FoodItemID` (`FoodItemID`),
  CONSTRAINT `detailedfeedback_ibfk_1` FOREIGN KEY (`NotificationID`) REFERENCES `notifications` (`NotificationID`),
  CONSTRAINT `detailedfeedback_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`),
  CONSTRAINT `detailedfeedback_ibfk_3` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detailedfeedback`
--

LOCK TABLES `detailedfeedback` WRITE;
/*!40000 ALTER TABLE `detailedfeedback` DISABLE KEYS */;
INSERT INTO `detailedfeedback` VALUES (1,17,3,12,1,'qwe'),(2,17,3,12,2,'sad'),(3,17,3,12,3,'xzc'),(4,20,3,12,1,'not sweet at all'),(5,20,3,12,2,'add sweetness'),(6,20,3,12,3,'just add more sweetness');
/*!40000 ALTER TABLE `detailedfeedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detailedreviewrequireditem`
--

DROP TABLE IF EXISTS `detailedreviewrequireditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detailedreviewrequireditem` (
  `DetailedReviewRequiredItemID` int NOT NULL AUTO_INCREMENT,
  `FoodItemID` int NOT NULL,
  `FoodItemName` varchar(45) NOT NULL,
  `NotificationID` int DEFAULT NULL,
  PRIMARY KEY (`DetailedReviewRequiredItemID`),
  KEY `FoodItemID` (`FoodItemID`),
  KEY `NotificationID` (`NotificationID`),
  CONSTRAINT `detailedreviewrequireditem_ibfk_1` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`),
  CONSTRAINT `detailedreviewrequireditem_ibfk_2` FOREIGN KEY (`NotificationID`) REFERENCES `notifications` (`NotificationID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detailedreviewrequireditem`
--

LOCK TABLES `detailedreviewrequireditem` WRITE;
/*!40000 ALTER TABLE `detailedreviewrequireditem` DISABLE KEYS */;
INSERT INTO `detailedreviewrequireditem` VALUES (3,12,'ww',17),(4,12,'ww',20);
/*!40000 ALTER TABLE `detailedreviewrequireditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discardmenuitems`
--

DROP TABLE IF EXISTS `discardmenuitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discardmenuitems` (
  `DiscardItemID` int NOT NULL AUTO_INCREMENT,
  `FoodItemID` int NOT NULL,
  `FoodItemName` varchar(45) NOT NULL,
  `AvgRating` decimal(3,2) NOT NULL,
  `AvgSentiment` decimal(3,2) NOT NULL,
  `DiscardDate` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`DiscardItemID`),
  KEY `FoodItemID` (`FoodItemID`),
  CONSTRAINT `discardmenuitems_ibfk_1` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discardmenuitems`
--

LOCK TABLES `discardmenuitems` WRITE;
/*!40000 ALTER TABLE `discardmenuitems` DISABLE KEYS */;
INSERT INTO `discardmenuitems` VALUES (4,13,'qwert',1.00,-0.54,'2024-07-10 19:06:13'),(5,13,'qwert',1.00,-0.54,'2024-07-10 19:06:22'),(6,12,'ww',1.25,-0.39,'2024-07-10 20:22:37');
/*!40000 ALTER TABLE `discardmenuitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `FeedbackID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `FoodItemID` int DEFAULT NULL,
  `FoodReviewRating` int DEFAULT NULL,
  `FoodReviewComments` varchar(100) DEFAULT NULL,
  `FoodReviewDate` date DEFAULT NULL,
  `OrderID` int DEFAULT NULL,
  `Sentiment` float DEFAULT NULL,
  PRIMARY KEY (`FeedbackID`),
  KEY `UserID` (`UserID`),
  KEY `FoodItemID` (`FoodItemID`),
  KEY `OrderID` (`OrderID`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`),
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`),
  CONSTRAINT `feedback_ibfk_3` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`OrderID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,3,1,5,'Delicious!','2024-06-15',12,0.6114),(2,4,1,4,'Spicy and flavorful.','2024-06-16',1,0.3),(3,5,1,2,'Could be better.','2024-06-17',1,0.17),(4,3,2,4,'Good with extra curry.','2024-06-15',15,0.4404),(5,4,2,3,'Decent taste.','2024-06-16',10,0.1),(6,3,3,5,'Best in town!','2024-06-15',6,0.6696),(7,5,3,4,'Yummy filling.','2024-06-16',12,0.5267),(8,4,4,4,'Love the noodles!','2024-06-16',15,0.6696),(9,5,4,2,'Could be more flavorful.','2024-06-17',7,0),(10,3,5,3,'Quick and tasty.','2024-06-15',5,0.4215),(11,4,6,4,'Creamy and delicious.','2024-06-16',15,0.5719),(12,3,7,5,'Perfect for breakfast!','2024-06-15',3,0.6114),(13,5,7,3,'Needs more sambar.','2024-06-17',5,-0.1323),(14,4,8,5,'Spicy and crispy.','2024-06-16',9,0.12),(15,3,1,4,'Good.','2024-06-20',17,0.4404),(16,3,1,5,'Great','2024-06-20',18,0.6249),(17,3,8,4,'Nice','2024-06-20',18,0.4215),(18,3,1,4,'Nice','2024-06-21',19,0.4215),(19,3,3,3,'Could have better filling','2024-06-21',19,0.1264),(20,3,1,3,'Ok okish','2024-06-21',23,0.196),(21,3,8,1,'dosa was not very good and the sambhar was abysmal.','2024-06-21',23,-0.5865),(22,3,2,4,'It was good','2024-07-02',24,0.4404),(23,3,3,5,'The parathas were amazing','2024-07-02',24,0.5859),(24,3,3,4,'Good','2024-07-02',25,0.4404),(25,3,7,3,'Okish','2024-07-02',25,0),(26,3,3,3,'Average','2024-07-02',26,0),(27,3,6,5,'Best Pasta ever!!','2024-07-02',26,0.6988),(28,3,12,1,'Very Bad','2024-07-02',27,-0.5849),(29,4,12,2,'not good','2024-07-02',28,-0.3412),(30,5,12,1,'yuck!','2024-07-02',29,0),(31,5,12,1,'worst food ever','2024-07-02',30,-0.6249),(32,3,13,1,'bad','2024-07-11',31,-0.5423);
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fooddetails`
--

DROP TABLE IF EXISTS `fooddetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fooddetails` (
  `FoodDetailsID` int NOT NULL AUTO_INCREMENT,
  `FoodItemID` int DEFAULT NULL,
  `FoodType` int DEFAULT NULL,
  `SpiceLevel` int DEFAULT NULL,
  `IsSweet` int DEFAULT NULL,
  `CusineType` int DEFAULT NULL,
  PRIMARY KEY (`FoodDetailsID`),
  KEY `FoodItemID` (`FoodItemID`),
  KEY `FoodType` (`FoodType`),
  KEY `SpiceLevel` (`SpiceLevel`),
  KEY `IsSweet` (`IsSweet`),
  KEY `CusineType` (`CusineType`),
  CONSTRAINT `fooddetails_ibfk_1` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`),
  CONSTRAINT `fooddetails_ibfk_2` FOREIGN KEY (`FoodType`) REFERENCES `foodtypeenum` (`FoodTypeID`),
  CONSTRAINT `fooddetails_ibfk_3` FOREIGN KEY (`SpiceLevel`) REFERENCES `spicelevelenum` (`SpiceLevelID`),
  CONSTRAINT `fooddetails_ibfk_4` FOREIGN KEY (`IsSweet`) REFERENCES `sweetpreferenceenum` (`SweetPreferenceID`),
  CONSTRAINT `fooddetails_ibfk_5` FOREIGN KEY (`CusineType`) REFERENCES `cusinetypeenum` (`CusineTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fooddetails`
--

LOCK TABLES `fooddetails` WRITE;
/*!40000 ALTER TABLE `fooddetails` DISABLE KEYS */;
INSERT INTO `fooddetails` VALUES (3,1,1,2,2,1),(4,2,1,2,2,1),(5,3,1,2,2,1),(6,4,1,3,2,3),(7,5,1,2,2,3),(8,6,1,2,2,3),(9,7,1,2,2,2),(10,8,1,2,2,2);
/*!40000 ALTER TABLE `fooddetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foodtypeenum`
--

DROP TABLE IF EXISTS `foodtypeenum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foodtypeenum` (
  `FoodTypeID` int NOT NULL AUTO_INCREMENT,
  `FoodTypeName` varchar(45) NOT NULL,
  PRIMARY KEY (`FoodTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foodtypeenum`
--

LOCK TABLES `foodtypeenum` WRITE;
/*!40000 ALTER TABLE `foodtypeenum` DISABLE KEYS */;
INSERT INTO `foodtypeenum` VALUES (1,'Vegetarian'),(2,'Non Vegetarian'),(3,'Eggetarian');
/*!40000 ALTER TABLE `foodtypeenum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `FoodItemID` int NOT NULL AUTO_INCREMENT,
  `FoodItemName` varchar(45) DEFAULT NULL,
  `FoodItemPrice` int DEFAULT NULL,
  `FoodItemAvailability` tinyint(1) DEFAULT NULL,
  `IsDiscarded` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`FoodItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'Pav Bhaji',70,1,0),(2,'Roti Curry (2pcs)',40,1,0),(3,'Aloo Paratha',25,1,0),(4,'Hakka Noodles',40,1,0),(5,'Maggi',35,1,0),(6,'Pasta',40,1,0),(7,'Idli/Vada (2 pcs)',30,1,0),(8,'Masala Dose',40,1,0),(12,'ww',22,1,1),(13,'qwert',12,1,1);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `NotificationID` int NOT NULL AUTO_INCREMENT,
  `NotificationMessage` varchar(100) DEFAULT NULL,
  `NotificationGeneratedAtTimeStamp` datetime DEFAULT NULL,
  `GeneratedByUserID` int DEFAULT NULL,
  `NotificationType` int DEFAULT NULL,
  PRIMARY KEY (`NotificationID`),
  KEY `GeneratedByUserID` (`GeneratedByUserID`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`GeneratedByUserID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,'Chef has rolled out the menu for 2024-06-21 00:49:47.509672','2024-06-20 00:49:48',2,1),(2,'Chef has rolled out the menu for 2024-06-21 01:44:23.679181','2024-06-20 01:44:24',2,1),(3,'Chef has rolled out the menu for 2024-06-21','2024-06-20 01:46:24',2,1),(4,'Chef has rolled out the menu for 2024-06-21','2024-06-20 04:03:18',2,1),(5,'Chef has rolled out the menu for 2024-06-22','2024-06-21 04:14:17',2,1),(6,'Chef has rolled out the menu for 2024-06-22','2024-06-21 04:16:38',2,1),(7,'Chef has rolled out the menu for 2024-06-22','2024-06-21 12:42:23',2,1),(8,'Chef has rolled out the menu for 2024-07-03','2024-07-02 07:21:29',2,1),(9,'Chef has rolled out the menu for 2024-07-03','2024-07-02 15:20:10',2,1),(10,'Chef has rolled out the menu for 2024-07-03','2024-07-02 16:30:31',2,1),(11,'Chef has rolled out the menu for 2024-07-03','2024-07-02 16:52:07',2,1),(12,'Chef has rolled out the menu for 2024-07-03','2024-07-02 16:52:25',2,1),(13,'Chef has requested detailed review for ww.','2024-07-03 22:48:04',NULL,2),(14,'Chef has requested detailed review for ww.','2024-07-03 23:09:19',NULL,2),(15,'Chef has requested detailed review for ww.','2024-07-03 23:10:57',NULL,2),(16,'Chef has requested detailed review for ww.','2024-07-03 23:30:16',2,2),(17,'Chef has requested detailed review for ww.','2024-07-03 23:37:37',2,2),(18,'Chef has rolled out the menu for 2024-07-12','2024-07-11 00:19:47',2,NULL),(19,'Chef has rolled out the menu for 2024-07-12','2024-07-11 00:20:06',2,NULL),(20,'Chef has requested detailed review for ww.','2024-07-11 01:01:56',2,2),(21,'Chef has rolled out the menu for 2024-07-12','2024-07-11 02:26:19',2,NULL);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `OrderDate` date DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,3,'2024-06-18'),(2,3,'2024-06-17'),(3,3,'2024-06-16'),(4,3,'2024-06-15'),(5,3,'2024-06-14'),(6,4,'2024-06-18'),(7,4,'2024-06-17'),(8,4,'2024-06-16'),(9,4,'2024-06-15'),(10,4,'2024-06-14'),(11,5,'2024-06-18'),(12,5,'2024-06-17'),(13,5,'2024-06-16'),(14,5,'2024-06-15'),(15,5,'2024-06-14'),(16,3,'2024-06-20'),(17,3,'2024-06-20'),(18,3,'2024-06-20'),(19,3,'2024-06-21'),(20,3,'2024-06-21'),(21,3,'2024-06-21'),(22,3,'2024-06-21'),(23,3,'2024-06-21'),(24,3,'2024-07-02'),(25,3,'2024-07-02'),(26,3,'2024-07-02'),(27,3,'2024-07-02'),(28,4,'2024-07-02'),(29,5,'2024-07-02'),(30,5,'2024-07-02'),(31,3,'2024-07-11');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spicelevelenum`
--

DROP TABLE IF EXISTS `spicelevelenum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spicelevelenum` (
  `SpiceLevelID` int NOT NULL AUTO_INCREMENT,
  `SpiceLevelName` varchar(45) NOT NULL,
  PRIMARY KEY (`SpiceLevelID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spicelevelenum`
--

LOCK TABLES `spicelevelenum` WRITE;
/*!40000 ALTER TABLE `spicelevelenum` DISABLE KEYS */;
INSERT INTO `spicelevelenum` VALUES (1,'Low'),(2,'Medium'),(3,'High');
/*!40000 ALTER TABLE `spicelevelenum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sweetpreferenceenum`
--

DROP TABLE IF EXISTS `sweetpreferenceenum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sweetpreferenceenum` (
  `SweetPreferenceID` int NOT NULL AUTO_INCREMENT,
  `SweetPreferenceName` varchar(45) NOT NULL,
  PRIMARY KEY (`SweetPreferenceID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sweetpreferenceenum`
--

LOCK TABLES `sweetpreferenceenum` WRITE;
/*!40000 ALTER TABLE `sweetpreferenceenum` DISABLE KEYS */;
INSERT INTO `sweetpreferenceenum` VALUES (1,'Yes'),(2,'No');
/*!40000 ALTER TABLE `sweetpreferenceenum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) DEFAULT NULL,
  `UserRole` varchar(45) DEFAULT NULL,
  `UserPassword` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Parth','admin','1234'),(2,'ChefJi','chef','1234'),(3,'EmpParth','employee','1234'),(4,'Tushar','employee','1234'),(5,'Rohit','employee','1234');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userorderdetails`
--

DROP TABLE IF EXISTS `userorderdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userorderdetails` (
  `UserOrderDetailsID` int NOT NULL AUTO_INCREMENT,
  `OrderID` int DEFAULT NULL,
  `FoodItemID` int DEFAULT NULL,
  PRIMARY KEY (`UserOrderDetailsID`),
  KEY `OrderID` (`OrderID`),
  KEY `FoodItemID` (`FoodItemID`),
  CONSTRAINT `userorderdetails_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`OrderID`),
  CONSTRAINT `userorderdetails_ibfk_2` FOREIGN KEY (`FoodItemID`) REFERENCES `menu` (`FoodItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userorderdetails`
--

LOCK TABLES `userorderdetails` WRITE;
/*!40000 ALTER TABLE `userorderdetails` DISABLE KEYS */;
INSERT INTO `userorderdetails` VALUES (1,1,1),(2,1,3),(3,2,2),(4,2,4),(5,3,5),(6,3,7),(7,4,6),(8,4,8),(9,5,1),(10,5,4),(11,6,2),(12,6,3),(13,7,5),(14,7,6),(15,8,1),(16,8,8),(17,9,4),(18,9,7),(19,10,2),(20,10,5),(21,16,1),(22,16,3),(23,17,1),(24,18,1),(25,18,8),(26,19,1),(27,19,3),(28,20,3),(29,21,1),(30,21,3),(31,22,8),(32,23,1),(33,23,8),(34,24,2),(35,24,3),(36,25,3),(37,25,7),(38,26,3),(39,26,6),(40,27,12),(41,28,12),(42,29,12),(43,30,12),(44,31,13);
/*!40000 ALTER TABLE `userorderdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userpreference`
--

DROP TABLE IF EXISTS `userpreference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userpreference` (
  `UserPreferenceID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `FoodType` int DEFAULT NULL,
  `SpiceLevel` int DEFAULT NULL,
  `IsSweet` int DEFAULT NULL,
  `CusineType` int DEFAULT NULL,
  PRIMARY KEY (`UserPreferenceID`),
  KEY `UserID` (`UserID`),
  KEY `FoodType` (`FoodType`),
  KEY `SpiceLevel` (`SpiceLevel`),
  KEY `IsSweet` (`IsSweet`),
  KEY `CusineType` (`CusineType`),
  CONSTRAINT `userpreference_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`),
  CONSTRAINT `userpreference_ibfk_2` FOREIGN KEY (`FoodType`) REFERENCES `foodtypeenum` (`FoodTypeID`),
  CONSTRAINT `userpreference_ibfk_3` FOREIGN KEY (`SpiceLevel`) REFERENCES `spicelevelenum` (`SpiceLevelID`),
  CONSTRAINT `userpreference_ibfk_4` FOREIGN KEY (`IsSweet`) REFERENCES `sweetpreferenceenum` (`SweetPreferenceID`),
  CONSTRAINT `userpreference_ibfk_5` FOREIGN KEY (`CusineType`) REFERENCES `cusinetypeenum` (`CusineTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userpreference`
--

LOCK TABLES `userpreference` WRITE;
/*!40000 ALTER TABLE `userpreference` DISABLE KEYS */;
INSERT INTO `userpreference` VALUES (1,3,1,3,1,1),(2,5,1,1,2,3);
/*!40000 ALTER TABLE `userpreference` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-11  2:36:11
