-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ciftlikbank_db
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'Admin','User','admin@admin','pbkdf2_sha256$870000$9EAVPNXRE5bP2MwknnzEij$JNNm4Ib+B5XM4szAr0QIamefsoDDxVG4iRscNNalN20=',1,'customer'),(2,'Arhan','Yılmaz','arhan@test.com','pbkdf2_sha256$870000$6SY8Yrfzjo3VlCXdbA0VeV$E/ZosapGRaELJ4JP32hf0O6sCKZRCsdpkavdcDtRQEI=',0,'customer'),(3,'Arhan','Yılmaz','arhanantalya@gmail.com','pbkdf2_sha256$870000$AC3Avh2iRIURf30bnQTbgm$ymrRO97S9howekkfosNCAUj4ki4H3jAoiRoROZTvgHs=',0,'customer'),(4,'Arhan','Yılmaz','tsar@tsar.com','pbkdf2_sha256$870000$rZQ2TqwFYZfJSnSGoJHVSL$ocevX8DqMGHDWhox7yhyoT7SuEcRRiHa9FEtAVQMY7g=',0,'customer'),(5,'murat','turat','murmur@test.com','pbkdf2_sha256$870000$xtD1fifhEpRhIhEo4nqAJc$47nCMqowHeEl3tlsmkpg1bQV11ZfJZtGKknqfhDT+SA=',0,'customer'),(6,'Arhan','abay','retorik@reto.com','pbkdf2_sha256$870000$uwzAY284ptbpAIc6pLf7Db$fHauOQ9L76uqZABp4O4qg9dn7guDgEiuo3oftQZWUdk=',0,'customer'),(7,'murat','turat','murat@turat.com','pbkdf2_sha256$870000$YW4DErgiW6EupbkGvI3VfB$Gy+43UmNW9rtTnu+gLnp1LDzjTf8PZ5GDMm6kZps7tg=',0,'customer'),(8,'Arhan','Yılmaz','arhan@test1231.com','pbkdf2_sha256$870000$AjaZ4hTpAqTArvmmYX9wcg$fz6AtBi6LemzIRtK8j23K/E8xUjinkdFGT95yPtkn/0=',0,'customer'),(9,'Arhan','turat','turat@turat.com','pbkdf2_sha256$870000$oR1K1LFAAgceeJw5MuMN3u$WmMirXOB0GNt/sgJBgs0MGN6stwqgDxVfo4xgv/z5Tc=',0,'customer'),(10,'murat','abay','murat@abay.com','pbkdf2_sha256$870000$OMW0iT3K6SAvvXboaz9QII$1008t0DEz9/Z0Xe8aMCI4k7gKRiUBsew+pXMAs753vQ=',0,'customer'),(11,'mert','pekmez','pekmez@mert.com','pbkdf2_sha256$870000$5UyyIYTDxPgHUdycJA47z8$AyrRKHxy5z4pVoYba6fjonuJXRKH5pZW5CtbCtTw04U=',0,'customer'),(12,'ĞPolen','Murat','polen@polen.com','pbkdf2_sha256$870000$2ZsiQyfefJ2j1PDpsGlvsi$kQHJKgQWsJ3vxYwH0ATdk8HodIJ3Kn1WchRLXgFWviU=',0,'customer'),(13,'Sales','Manager','sales@example.com','pbkdf2_sha256$870000$bA76sHS8P78CIe7nbDRgmG$ejOrut9jY0t5dhKmpREkoFPABCABRuX/Opv4Wg0ya8g=',0,'sales_manager');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add user',7,'add_user'),(26,'Can change user',7,'change_user'),(27,'Can delete user',7,'delete_user'),(28,'Can view user',7,'view_user'),(29,'Can add product',8,'add_product'),(30,'Can change product',8,'change_product'),(31,'Can delete product',8,'delete_product'),(32,'Can view product',8,'view_product'),(33,'Can add cart',9,'add_cart'),(34,'Can change cart',9,'change_cart'),(35,'Can delete cart',9,'delete_cart'),(36,'Can view cart',9,'view_cart'),(37,'Can add cart item',10,'add_cartitem'),(38,'Can change cart item',10,'change_cartitem'),(39,'Can delete cart item',10,'delete_cartitem'),(40,'Can view cart item',10,'view_cartitem'),(41,'Can add order',11,'add_order'),(42,'Can change order',11,'change_order'),(43,'Can delete order',11,'delete_order'),(44,'Can view order',11,'view_order'),(45,'Can add order item',12,'add_orderitem'),(46,'Can change order item',12,'change_orderitem'),(47,'Can delete order item',12,'delete_orderitem'),(48,'Can view order item',12,'view_orderitem'),(49,'Can add review',13,'add_review'),(50,'Can change review',13,'change_review'),(51,'Can delete review',13,'delete_review'),(52,'Can view review',13,'view_review'),(53,'Can add address',14,'add_address'),(54,'Can change address',14,'change_address'),(55,'Can delete address',14,'delete_address'),(56,'Can view address',14,'view_address');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'accounts','user'),(14,'address','address'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(11,'orders','order'),(12,'orders','orderitem'),(9,'products','cart'),(10,'products','cartitem'),(8,'products','product'),(13,'reviews','review'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2025-04-26 23:46:28.088997'),(2,'accounts','0002_add_is_admin_field','2025-04-26 23:46:28.151757'),(3,'accounts','0003_create_admin_user','2025-04-26 23:46:28.629976'),(4,'contenttypes','0001_initial','2025-04-26 23:46:28.660929'),(5,'auth','0001_initial','2025-04-26 23:46:29.306852'),(6,'admin','0001_initial','2025-04-26 23:46:29.460023'),(7,'admin','0002_logentry_remove_auto_add','2025-04-26 23:46:29.466764'),(8,'admin','0003_logentry_add_action_flag_choices','2025-04-26 23:46:29.473616'),(9,'contenttypes','0002_remove_content_type_name','2025-04-26 23:46:29.571822'),(10,'auth','0002_alter_permission_name_max_length','2025-04-26 23:46:29.639562'),(11,'auth','0003_alter_user_email_max_length','2025-04-26 23:46:29.673839'),(12,'auth','0004_alter_user_username_opts','2025-04-26 23:46:29.679883'),(13,'auth','0005_alter_user_last_login_null','2025-04-26 23:46:29.730478'),(14,'auth','0006_require_contenttypes_0002','2025-04-26 23:46:29.730478'),(15,'auth','0007_alter_validators_add_error_messages','2025-04-26 23:46:29.730478'),(16,'auth','0008_alter_user_username_max_length','2025-04-26 23:46:29.806216'),(17,'auth','0009_alter_user_last_name_max_length','2025-04-26 23:46:29.882796'),(18,'auth','0010_alter_group_name_max_length','2025-04-26 23:46:29.887851'),(19,'auth','0011_update_proxy_permissions','2025-04-26 23:46:29.908925'),(20,'auth','0012_alter_user_first_name_max_length','2025-04-26 23:46:29.964593'),(21,'products','0001_initial','2025-04-26 23:46:30.008465'),(22,'products','0002_cart_cartitem','2025-04-26 23:46:30.340305'),(23,'orders','0001_initial','2025-04-26 23:46:30.575980'),(24,'orders','0002_alter_order_user','2025-04-26 23:46:30.714500'),(25,'reviews','0001_initial','2025-04-26 23:46:30.855960'),(26,'reviews','0002_alter_review_user','2025-04-26 23:46:31.001523'),(27,'sessions','0001_initial','2025-04-26 23:46:31.043562'),(28,'products','0003_alter_cart_user','2025-04-27 08:51:00.534648'),(29,'orders','0003_order_payment_reference','2025-04-27 23:36:14.109659'),(30,'products','0004_product_avg_rating_product_rating_count','2025-04-28 12:07:10.219986'),(31,'reviews','0003_alter_review_comment','2025-04-28 12:07:10.296301'),(32,'reviews','0004_alter_review_rating','2025-04-28 12:07:10.397653'),(33,'accounts','0004_user_role','2025-05-08 14:08:06.625193'),(34,'products','0005_product_cost_product_discount_rate_and_more','2025-05-08 14:08:06.789316');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('04pfs13ucfcbofkw8dfkik7vsnhiw110','eyJ1c2VyX2lkIjoxMn0:1u9NQL:q60nmA74xkJdTNXlQP9d_47EWsnQVbiD3nBWPxDsDdc','2025-05-12 12:17:25.962435'),('4fpbrus706l4nrlqgc8xl4llhvrfbb5k','e30:1u9NI3:_ete3dbDUVpz34Wmwtq8bLOSan8GI58DZuuHui69mWM','2025-05-12 12:08:51.954003'),('5udpxriowar2igq011i1b0qecirxg38j','e30:1u9NJZ:Wqsjs7HzW_mDTIYy48D-EZFu5EazSeEuZ88m3JbbANw','2025-05-12 12:10:25.123429'),('6g1xuaocp3xggw68wh73mzjjyn1yvah5','eyJ1c2VyX2lkIjoxMX0:1u9CWj:-xyGFjjkdemWTEnkHo2NboKvsHW70iSHcip1_7T_mIc','2025-05-12 00:39:17.447814'),('7g0plppptwpnuig8jnyf12ejk8pae1q9','eyJ1c2VyX2lkIjo5fQ:1u9629:wY2VkkHICdgQiIJJKTw-Du4PxvUDVj90ULR5Qio93vY','2025-05-11 17:43:17.948131'),('7mhfrnfaomi5qmvp9peoi8nbmu61l3bj','e30:1u9NHK:QFljGDZJjbR_NdHoJFcenVupyh_irjhgIvsZQt3SIPI','2025-05-12 12:08:06.338772'),('bydeskc1sffwi1a9y8ij16sk46u0l7iu','eyJ1c2VyX2lkIjo4fQ:1u95Sc:WhsRmLo3i95cGPIQzABYR1VWq20QpCz8pEvHirUOeng','2025-05-11 17:06:34.507280'),('c2tgm9c79emnlfxl9ipk1y6do608c39o','eyJ1c2VyX2lkIjoxMH0:1u9Bn0:tYLSMCKUNq1AELln6YJcBRnIfAvxRLg307gODrGfNuE','2025-05-11 23:52:02.282686'),('dp0z9y0tio3oibroqlz5xqx43d9mli6d','eyJ1c2VyX2lkIjoyfQ:1u99jA:xoI7ZMhJoABDjFDcRHKmHS1nkDoDRf0KEA3rbAWirLw','2025-05-11 21:39:56.803052'),('eo1tshtv5vkptqiw5y1u9n2npbn80mwp','eyJ1c2VyX2lkIjoyfQ:1u8pFH:LaYGDrxItqv8zJqSL6i1nVmfqMbMBKKB9F2jCboa-vs','2025-05-10 23:47:43.727343'),('f3b6tva44tetuvwhzm4z9qke77x2d3k7','e30:1u9NIc:bAkx_SRVzWuXDRmf2N7x4nxtIwZEeRQNtmuwJdVfXL8','2025-05-12 12:09:26.055935'),('ivkuyrwgylvsqwnz8ij1c6wvrs2cm30p','e30:1u9NNU:DguaDx-YGmOpj1lXEY54LrBgASfWpXzbBGWw1jp0eqg','2025-05-12 12:14:28.394284'),('jko5tb62t29fslyme4d9j399nx3i2nmt','e30:1u9NQg:EqM5PIXGoFZkuCNt1o3NONAtyWsMZ8bsTKOdOY0y1OM','2025-05-12 12:17:46.627549'),('jt8cp1clpwcemd5rzujbonj5n8balmso','e30:1u9NQg:EqM5PIXGoFZkuCNt1o3NONAtyWsMZ8bsTKOdOY0y1OM','2025-05-12 12:17:46.666923'),('llzy8br4iyvw8tvccm5odjwwp2borabp','eyJ1c2VyX2lkIjo2fQ:1u8zPr:VNoKsbd0eAHaah5tWvkaLOMQc0toyQ9cidi4J8nR2Qo','2025-05-11 10:39:19.565426'),('vwe9spbqws464fap3zs01xkof25s0stp','eyJ1c2VyX2lkIjoyfQ:1u9NSK:lN6f4KxN1VO0uJbf8O_cTeWI3oeY4iSOmc1yxQKzUyw','2025-05-12 12:19:28.108739'),('vzplf8qoeq4jca0sqybf8kxfc92wf2uj','eyJ1c2VyX2lkIjo1fQ:1u8yGd:VzuWuRT86fmZvzX_EOgrj7ApaR6oE94vESiE0SwTTGs','2025-05-11 09:25:43.303161'),('xribwgbezxeufbrb1miydzd5biuopoqi','e30:1u9NJs:nRUXWPbnG--3rTKFBZuscG5G3x5VoTApbBg7PGv84KY','2025-05-12 12:10:44.767821'),('z9b7ionzf4008p2jubzvmz6wk84u748l','eyJ1c2VyX2lkIjo0fQ:1u8pPK:q80p_3P0HyXIRfKyo0osstCs0CIo-ZsBFqMZrM9qYE8','2025-05-10 23:58:06.930933');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `delivery_address` varchar(255) NOT NULL,
  `status` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  `payment_reference` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_order_user_id_e9b59eb1_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `orders_order_user_id_e9b59eb1_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
INSERT INTO `orders_order` VALUES (1,'2025-04-27 23:59:48.162336',180.70,'','pending',2,NULL),(2,'2025-04-28 00:00:04.842114',180.70,'','pending',2,NULL),(3,'2025-04-28 00:00:35.665604',180.70,'','delivered',2,NULL),(4,'2025-04-28 00:03:07.181535',24.50,'','pending',10,NULL),(5,'2025-04-28 12:08:38.148515',24.50,'2121','processing',2,NULL),(6,'2025-04-28 12:08:40.464012',24.50,'2121','processing',2,NULL),(7,'2025-04-28 12:20:17.145123',147.00,'21deded','processing',2,NULL);
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `price_at_purchase` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`),
  KEY `orders_orderitem_product_id_afe4254a_fk_products_product_id` (`product_id`),
  CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_orderitem_product_id_afe4254a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `orders_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
INSERT INTO `orders_orderitem` VALUES (1,2,45.90,3,3),(2,2,24.50,3,2),(3,1,39.90,3,1),(4,1,24.50,4,2),(5,1,24.50,5,2),(6,1,24.50,6,2),(7,6,24.50,7,2);
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_cart`
--

DROP TABLE IF EXISTS `products_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_id` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_cart_user_id_d53bf7cf_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `products_cart_user_id_d53bf7cf_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_cart`
--

LOCK TABLES `products_cart` WRITE;
/*!40000 ALTER TABLE `products_cart` DISABLE KEYS */;
INSERT INTO `products_cart` VALUES (1,'z9b7ionzf4008p2jubzvmz6wk84u748l','2025-04-26 23:49:30.734369',NULL),(2,'rvzc1nbpyzenojku0jvtm42rolw5ju7x','2025-04-27 08:33:42.317107',NULL),(3,NULL,'2025-04-27 08:34:16.855461',2),(5,'66p55j8ywqejqk9ltt8sn4sjdvkosyy1','2025-04-27 08:51:59.906759',NULL),(6,'1hkfnsyhamyjywkkw0ceten540mpxetl','2025-04-27 09:21:43.028414',NULL),(8,'u2qsvw6dfsbaeczlnov49isgnhxkzn3g','2025-04-27 09:22:23.526788',NULL),(9,'7sibctym4fiiyzgy1vup0dmh0pwee4zi','2025-04-27 09:24:47.738875',NULL),(11,NULL,'2025-04-27 09:25:43.296141',5),(12,'l8y35k32k1lugb38w3h3op4lyvmestye','2025-04-27 10:49:32.076700',NULL),(13,'cyqllahwrewdcd5on173hjbsi3pymwj8','2025-04-27 17:07:37.084916',NULL),(14,NULL,'2025-04-27 17:26:23.927297',8),(15,NULL,'2025-04-27 17:32:52.862381',8),(18,'zld7157py6av2enjlyb76e7aohure6nt','2025-04-27 17:44:45.888095',NULL),(24,'k7qm3ccmi9vmcr8lm0utkn149bd9dyii','2025-04-27 19:00:34.428919',NULL),(25,NULL,'2025-04-27 19:03:15.080798',7),(26,'j4pixadbkarqcu335me0cx3k1fdud023','2025-04-27 19:03:38.090092',NULL),(29,'cq13qdz8f71avz2rcs44ykcax1mlbsgt','2025-04-27 19:08:58.779102',NULL),(30,'yaby7k3m31x7nlp4yx7ka1h9sw7ag9mh','2025-04-27 19:42:02.677547',NULL),(31,'aboueb2oz6czqh515gxa3zhbo6cid7hf','2025-04-27 19:46:27.517256',NULL),(32,'327cztiei3lx6tkl5rf69349k5lg6s2u','2025-04-27 19:50:36.499900',NULL),(33,NULL,'2025-04-27 22:41:22.504290',NULL),(34,NULL,'2025-04-27 23:52:06.949743',10),(35,NULL,'2025-04-28 12:14:57.036628',12);
/*!40000 ALTER TABLE `products_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_cartitem`
--

DROP TABLE IF EXISTS `products_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `cart_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_cartitem_cart_id_b75c2d92_fk_products_cart_id` (`cart_id`),
  KEY `products_cartitem_product_id_e735c06a_fk_products_product_id` (`product_id`),
  CONSTRAINT `products_cartitem_cart_id_b75c2d92_fk_products_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `products_cart` (`id`),
  CONSTRAINT `products_cartitem_product_id_e735c06a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `products_cartitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_cartitem`
--

LOCK TABLES `products_cartitem` WRITE;
/*!40000 ALTER TABLE `products_cartitem` DISABLE KEYS */;
INSERT INTO `products_cartitem` VALUES (1,3,1,2),(2,1,2,3),(5,1,5,2),(6,1,5,3),(7,1,6,2),(8,1,6,3),(10,1,8,2),(11,1,9,3),(14,1,12,2),(15,1,12,3),(16,1,13,3),(21,3,15,2),(22,3,15,3),(30,2,14,2),(31,2,14,3),(32,1,14,1),(35,1,14,6),(38,3,14,5),(39,2,14,4),(48,3,26,3),(52,2,29,2),(54,1,29,1),(55,1,30,2),(56,1,30,3),(57,1,31,2),(58,1,31,3),(59,5,32,1),(60,3,25,3),(62,1,33,2),(63,1,33,3),(66,1,35,6);
/*!40000 ALTER TABLE `products_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product`
--

DROP TABLE IF EXISTS `products_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `model` varchar(255) DEFAULT NULL,
  `serial_number` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_quantity` int unsigned NOT NULL,
  `category` varchar(100) NOT NULL,
  `warranty_status` tinyint(1) NOT NULL,
  `distributor_info` longtext NOT NULL,
  `image_url` varchar(200) NOT NULL,
  `avg_rating` double NOT NULL,
  `rating_count` int NOT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `discount_rate` decimal(5,2) NOT NULL,
  `discounted_price` decimal(10,2) DEFAULT NULL,
  `is_approved` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `serial_number` (`serial_number`),
  CONSTRAINT `products_product_chk_1` CHECK ((`stock_quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product`
--

LOCK TABLES `products_product` WRITE;
/*!40000 ALTER TABLE `products_product` DISABLE KEYS */;
INSERT INTO `products_product` VALUES (1,'10\'lu Organik Yumurta','ORG-MODEL-1','SN001ABC','Serbest dolaşan tavuklardan elde edilen taze organik yumurta.',39.90,12,'Süt Ürünleri',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/50524/uploads/urunresimleri/buyuk/10lu-gezen-tavuk-yumurtasi-fe5899.jpg',0,0,NULL,0.00,NULL,0),(2,'Organik Süt (1L)','ORG-MODEL-2','SN002ABC','Taze ve doğal organik süt.',24.50,0,'Süt Ürünleri',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/akmese-organik-sut-3lt-sadece-bursa-ve-dc0e09.png',5,1,NULL,0.00,NULL,0),(3,'Organik Peynir (500g)','ORG-MODEL-3','SN003ABC','El yapımı, lezzetli ve sağlıklı organik peynir.',45.90,14,'Süt Ürünleri',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/100-salamura-keci-peyniri-400-gr-8a5-c9.png',0,0,NULL,0.00,NULL,0),(4,'Domates (1 kg)','ORG-MODEL-4','SN004ABC','Taze ve organik domatesler, sağlıklı yemekler için ideal.',19.90,22,'Sebzeler',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/organik-sofralik-domates-1-kg-sadece-b-ef144f.jpeg',0,0,NULL,0.00,NULL,0),(5,'Kozalak Macunu 240 g','ORG-MODEL-5','SN005ABC','Doğal içeriğiyle kozalağın faydalarını sunan macun.',150.90,6,'Macunlar',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=360,quality=85/56277/uploads/urunresimleri/buyuk/og-kozalak-macunu-240-gr-cf2-9f.jpg',0,0,NULL,0.00,NULL,0),(6,'Jovia Organik %70 Bitter Çikolata-Yaban Mersini&Badem&Açai','ORG-MODEL-6','SN006ABC','Zengin kakao aroması ve organik içeriğiyle bitter çikolata keyfi.',220.90,5,'Atıştırmalıklar',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=360,quality=85/56277/uploads/urunresimleri/buyuk/jovia-organik-70-bitter-cikolata-yaban-d3ef-4.jpg',0,0,NULL,0.00,NULL,0),(7,'Taze Kuşkonmaz(1 kg)','ORG-MODEL-7','SN007ABC','Vitamin deposu taze kuşkonmaz, sağlıklı beslenme için.',27.90,9,'Sebzeler',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-kuskonmaz--b-4ec9.jpg',0,0,NULL,0.00,NULL,0),(8,'Taze Böğürtlen','ORG-MODEL-8','SN008ABC','Tatlı ve taze böğürtlen, doğal atıştırmalık olarak ideal.',240.90,4,'Meyveler',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-bogurtlen-213f64.jpg',0,0,NULL,0.00,NULL,0),(9,'Kara Mürver Püresi','ORG-MODEL-9','SN009ABC','Doğal ve besleyici kara mürver püresi.',225.00,3,'Macunlar',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/kara-murver-puresi-230g--46d1-.jpg',0,0,NULL,0.00,NULL,0),(10,'Taze Zerdeçal(80 gr)','ORG-MODEL-10','SN010ABC','Antioksidan özellikleriyle taze zerdeçal.',75.90,7,'Sebzeler',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-zerdecal-100gr-935-38.jpeg',0,0,NULL,0.00,NULL,0),(11,'Taze Zencefil (1 kg)','ORG-MODEL-11','SN011ABC','Baharat olarak veya sağlık amaçlı kullanabileceğiniz taze zencefil.',16.90,10,'Sebzeler',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-zencefil-250gpaket-7-e72f.jpg',0,0,NULL,0.00,NULL,0),(12,'Tatlı Patates (1 kg)','ORG-MODEL-12','SN012ABC','Lezzetli ve besleyici tatlı patates.',54.90,15,'Sebzeler',0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/tatli-patates-2-kg-da-734.jpg',0,0,NULL,0.00,NULL,0);
/*!40000 ALTER TABLE `products_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_review`
--

DROP TABLE IF EXISTS `reviews_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int DEFAULT NULL,
  `comment` longtext,
  `approved` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_review_product_id_ce2fa4c6_fk_products_product_id` (`product_id`),
  KEY `reviews_review_user_id_875caff2_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `reviews_review_product_id_ce2fa4c6_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `reviews_review_user_id_875caff2_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_review`
--

LOCK TABLES `reviews_review` WRITE;
/*!40000 ALTER TABLE `reviews_review` DISABLE KEYS */;
INSERT INTO `reviews_review` VALUES (1,5,'HARİKA ÜRÜN KESİNLİKLE ÖNERMEM',1,'2025-04-28 12:09:48.108736',2,2);
/*!40000 ALTER TABLE `reviews_review` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-14 19:14:13
