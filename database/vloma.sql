-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: vloma
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address_line1` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address_line2` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pincode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'admin',
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (3,'Admin','admin@anistock.com','scrypt:32768:8:1$hYdJCR0lxZS1iiJn$a9159848438d7b35e4b0b7f89da34dc4863450ea49f26647c7ce888a7114695fdd5d0e9035906b5fb5e1776b3cfbfbb32324401e1a0186ffd440effae8f023e3','admin');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `discount` decimal(10,2) NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

LOCK TABLES `coupons` WRITE;
/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_categories`
--

DROP TABLE IF EXISTS `main_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_categories` (
  `main_category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`main_category_id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_categories`
--

LOCK TABLES `main_categories` WRITE;
/*!40000 ALTER TABLE `main_categories` DISABLE KEYS */;
INSERT INTO `main_categories` VALUES (1,'Cosmetics','cosmetics','2026-08-08 15:27:48'),(2,'Jewellery','jewellery','2026-08-08 15:29:43'),(3,'Footwear','footwear','2026-08-08 15:29:43'),(4,'Bags & Accessories','bags-accessories','2026-08-08 15:29:43'),(5,'Perfumes','perfumes','2026-08-08 15:29:43'),(6,'New Arrivals','new-arrivals','2026-08-08 15:29:43');
/*!40000 ALTER TABLE `main_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `material_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES (1,1,'Matte'),(2,1,'Cream'),(3,1,'Liquid'),(4,1,'Powder'),(5,1,'Gel'),(6,1,'Stick'),(7,1,'Balm'),(8,1,'Foam'),(9,1,'Oil'),(10,1,'Mist'),(11,2,'Gold'),(12,2,'Silver'),(13,2,'Rose Gold'),(14,2,'Platinum'),(15,2,'Diamond'),(16,2,'Pearl'),(17,2,'Kundan'),(18,2,'Polki'),(19,2,'Oxidised Silver'),(20,2,'Brass'),(21,2,'Copper'),(22,2,'Stainless Steel'),(23,2,'Sterling Silver'),(24,2,'Beads'),(25,2,'Crystal'),(26,3,'Leather'),(27,3,'PU Leather'),(28,3,'Suede'),(29,3,'Canvas'),(30,3,'Mesh'),(31,3,'Rubber'),(32,3,'Synthetic'),(33,3,'Velvet'),(34,3,'Denim'),(35,3,'PVC'),(36,4,'Leather'),(37,4,'PU Leather'),(38,4,'Canvas'),(39,4,'Nylon'),(40,4,'Polyester'),(41,4,'Denim'),(42,4,'Jute'),(43,4,'Cotton'),(44,4,'Velvet'),(45,4,'Straw'),(46,5,'Floral'),(47,5,'Woody'),(48,5,'Oriental'),(49,5,'Fresh'),(50,5,'Citrus'),(51,5,'Musk'),(52,5,'Vanilla'),(53,5,'Amber'),(54,5,'Aquatic'),(55,5,'Fruity'),(56,3,'Cork'),(59,3,'Jute');
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `seller_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `product_price` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `commission_percent` decimal(5,2) NOT NULL,
  `commission_amount` decimal(10,2) NOT NULL,
  `seller_earning` decimal(10,2) NOT NULL,
  `order_status` enum('Pending','Processing','Shipped','Delivered','Cancelled') COLLATE utf8mb4_unicode_ci DEFAULT 'Pending',
  `order_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  KEY `seller_id` (`seller_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `sellers` (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `image_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_primary` tinyint(1) DEFAULT '0',
  `display_order` int DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`image_id`),
  KEY `fk_product_images` (`product_id`),
  CONSTRAINT `fk_product_images` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_types`
--

DROP TABLE IF EXISTS `product_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_types` (
  `id` int NOT NULL,
  `category_id` int NOT NULL,
  `category_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subcategory_id` int NOT NULL,
  `subcategory_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `material_options` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_types`
--

LOCK TABLES `product_types` WRITE;
/*!40000 ALTER TABLE `product_types` DISABLE KEYS */;
INSERT INTO `product_types` VALUES (101,1,'Cosmetics',101,'Lipsticks, Glosses & Lip Liners','Liquid,Cream,Matte,Gloss'),(102,1,'Cosmetics',102,'Foundations, Concealers & Compacts','Liquid,Cream,Powder,Stick'),(103,1,'Cosmetics',103,'Eyeliners, Kajal & Mascara','Gel,Liquid,Pencil'),(104,1,'Cosmetics',104,'Highlighters, Blushes & Eyeshadows','Powder,Cream,Liquid'),(105,1,'Cosmetics',105,'Serums & Face Oils','Oil,Serum'),(106,1,'Cosmetics',106,'Moisturisers & Night Creams','Cream,Gel,Lotion'),(107,1,'Cosmetics',107,'Sunscreen & UV Protection','Cream,Gel,Spray,Lotion'),(108,1,'Cosmetics',108,'Face Washes & Cleansers','Foam,Gel,Cream'),(109,1,'Cosmetics',109,'Shampoos & Conditioners','Liquid,Cream'),(110,1,'Cosmetics',110,'Hair Serums & Masks','Serum,Cream,Oil'),(111,1,'Cosmetics',111,'Body Lotions, Washes & Scrubs','Lotion,Gel,Cream'),(201,2,'Jewellery',201,'Gold, Diamond & Silver Rings','Gold,Silver,Diamond,Platinum'),(202,2,'Jewellery',202,'Necklaces & Pendants','Gold,Silver,Pearl,Diamond'),(203,2,'Jewellery',203,'Bracelets & Bangles','Gold,Silver,Rose Gold'),(204,2,'Jewellery',204,'Statement Earrings & Hoops','Gold,Silver,Brass,Oxidised'),(205,2,'Jewellery',205,'Chokers & Layered Chains','Gold,Silver,Pearl'),(206,2,'Jewellery',206,'Trendy Rings & Cuffs','Gold,Silver,Stainless Steel'),(207,2,'Jewellery',207,'Temple & Kundan Jewellery Sets','Gold,Kundan,Pearl'),(208,2,'Jewellery',208,'Maang Tikkas & Matha Pattis','Gold,Kundan'),(209,2,'Jewellery',209,'Anklets (Payal) & Toe Rings','Silver,Oxidised'),(210,2,'Jewellery',210,'Nose Pins & Naths','Gold,Silver,Diamond'),(301,3,'Footwear',301,'Stilettos & Pumps','Leather,PU Leather,Suede'),(302,3,'Footwear',302,'Block Heels & Kitten Heels','Leather,PU Leather'),(303,3,'Footwear',303,'Platform Wedges','Leather,Canvas,Rubber'),(304,3,'Footwear',304,'Juttis & Mojris','Leather,Fabric'),(305,3,'Footwear',305,'Ballerinas & Loafers','Leather,Canvas,Suede'),(306,3,'Footwear',306,'Kolhapuri Sandals & Slides','Leather,Rubber'),(307,3,'Footwear',307,'Sneakers & Slip-ons','Canvas,Mesh,Rubber'),(308,3,'Footwear',308,'Running & Walking Shoes','Mesh,Rubber,Foam'),(309,3,'Footwear',309,'Flip-flops & Beach Slides','Rubber,EVA'),(401,4,'Bags',401,'Tote Bags & Shoulder Bags','Leather,PU Leather,Canvas'),(402,4,'Bags',402,'Satchels & Hobo Bags','Leather,PU Leather'),(403,4,'Bags',403,'Sling & Crossbody Bags','Leather,Canvas'),(404,4,'Bags',404,'Box Clutches & Envelope Bags','Leather,Velvet'),(405,4,'Bags',405,'Traditional Potli Bags','Silk,Velvet'),(406,4,'Bags',406,'Party Pouches','Velvet,Leather'),(407,4,'Bags',407,'Backpacks & Mini Backpacks','Canvas,Nylon,Polyester'),(408,4,'Bags',408,'Wallets & Card Holders','Leather,PU Leather'),(409,4,'Bags',409,'Laptop Sleeves & Travel Pouches','Canvas,Leather,Neoprene'),(501,5,'Perfumes',501,'Floral & Fruity','Floral,Fruity'),(502,5,'Perfumes',502,'Woody & Oriental','Woody,Oriental'),(503,5,'Perfumes',503,'Fresh & Citrus','Fresh,Citrus'),(504,5,'Perfumes',504,'Body Sprays & Deodorants','Fresh,Citrus'),(505,5,'Perfumes',505,'Scented Body Mists','Floral,Fruity'),(506,5,'Perfumes',506,'Luxury Discovery Sets','Mixed'),(507,5,'Perfumes',507,'Pocket Perfumes & Travel Sprays','Mixed');
/*!40000 ALTER TABLE `product_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `product_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `brand` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `material` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `material_id` int DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `rating` decimal(2,1) NOT NULL DEFAULT '0.0',
  `total_reviews` int NOT NULL DEFAULT '0',
  `badge` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `description` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`),
  KEY `fk_products_type` (`type_id`),
  KEY `fk_products_material` (`material_id`),
  CONSTRAINT `fk_products_material` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_products_type` FOREIGN KEY (`type_id`) REFERENCES `product_types` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,101,'Velvet Matte Lipstick - Crimson Rush','Glamora','Matte',1,499.00,4.3,1287,'Bestseller',150,'Long-lasting matte lipstick with a rich crimson finish.','2026-08-12 15:39:31'),(2,101,'Creamy Lip Tint - Rosewood','Glamora','Cream',2,429.00,4.1,587,NULL,170,'Buildable creamy lip tint with a natural flush.','2026-08-12 15:39:31'),(3,101,'Hydra Shine Liquid Lipstick - Coral Pop','Glamora','Liquid',3,379.00,4.2,642,'New',210,'Long-wear liquid lipstick with a glossy hydrating finish.','2026-08-12 15:39:31'),(4,102,'Second Skin Liquid Foundation','Lumière','Liquid',3,899.00,4.4,953,'New',120,'Lightweight buildable coverage foundation for all-day wear.','2026-08-12 15:39:31'),(5,102,'Full Coverage Cream Concealer','Lumière','Cream',2,549.00,4.2,412,NULL,160,'Creamy concealer that covers dark circles and blemishes.','2026-08-12 15:39:31'),(6,102,'Compact Powder Duo - Ivory Beige','Lumière','Powder',4,599.00,4.0,415,NULL,180,'Oil-control compact powder with mirror and puff.','2026-08-12 15:39:31'),(7,103,'Waterproof Gel Eyeliner','Lumière','Gel',5,349.00,4.2,731,NULL,175,'Precision-tip gel eyeliner for sharp winged looks.','2026-08-12 15:39:31'),(8,103,'Intense Liquid Eyeliner','Lumière','Liquid',3,299.00,4.3,528,'Bestseller',200,'Ultra-fine tip liquid eyeliner for a bold, precise line.','2026-08-12 15:39:31'),(9,103,'Volumising Stick Mascara','Lumière','Stick',6,399.00,4.1,245,'New',140,'Twist-up stick mascara for clump-free volume.','2026-08-12 15:39:31'),(10,104,'Golden Glow Powder Highlighter','Lumière','Powder',4,749.00,4.3,528,NULL,140,'Buildable powder highlighter for a radiant finish.','2026-08-12 15:39:31'),(11,104,'Blush Duo - Peach & Rose','Glamora','Cream',2,599.00,4.1,389,'New',160,'Creamy blendable blush duo for a natural flush.','2026-08-12 15:39:31'),(12,104,'Liquid Eyeshadow - Bronze Shimmer','Glamora','Liquid',3,499.00,4.2,267,'Bestseller',130,'Metallic liquid eyeshadow with a long-lasting shimmer finish.','2026-08-12 15:39:31'),(13,105,'Vitamin C Brightening Serum','DermaPure','Oil',9,999.00,4.6,1854,'Bestseller',220,'10% Vitamin C facial oil-serum for even-toned, glowing skin.','2026-08-12 15:39:31'),(14,105,'Niacinamide Gel Serum','DermaPure','Gel',5,749.00,4.3,690,NULL,190,'Lightweight gel-serum that minimizes pores and controls oil.','2026-08-12 15:39:31'),(15,105,'Rosehip Nourishing Face Oil','DermaPure','Oil',9,849.00,4.4,612,NULL,130,'Cold-pressed rosehip oil to restore skin elasticity.','2026-08-12 15:39:31'),(16,106,'Deep Repair Night Cream','DermaPure','Cream',2,749.00,4.5,940,NULL,175,'Rich overnight cream that repairs and hydrates skin.','2026-08-12 15:39:31'),(17,106,'Hyaluronic Gel Moisturiser','DermaPure','Gel',5,649.00,4.2,503,'New',190,'Lightweight gel moisturiser for oily and combination skin.','2026-08-12 15:39:31'),(18,106,'Shea Butter Balm Moisturiser','DermaPure','Balm',7,599.00,4.1,312,NULL,160,'Thick balm moisturiser for extra-dry skin overnight repair.','2026-08-12 15:39:31'),(19,107,'Matte SPF 50 Sunscreen Gel','DermaPure','Gel',5,599.00,4.6,1420,'Bestseller',260,'Broad spectrum SPF 50 sunscreen with a matte, non-greasy finish.','2026-08-12 15:39:31'),(20,107,'Sunscreen Cream SPF 40','DermaPure','Cream',2,499.00,4.2,356,NULL,200,'Nourishing SPF 40 sunscreen cream for daily protection.','2026-08-12 15:39:31'),(21,107,'Cooling Sunscreen Mist SPF 30','DermaPure','Mist',10,449.00,4.0,267,'New',210,'Easy-reapply SPF 30 mist for on-the-go sun protection.','2026-08-12 15:39:31'),(22,108,'Foaming Charcoal Face Wash','DermaPure','Foam',8,349.00,4.3,875,NULL,240,'Deep-cleansing charcoal foam for clear, fresh skin.','2026-08-12 15:39:31'),(23,108,'Gentle Gel Cleanser','DermaPure','Gel',5,299.00,4.0,421,'New',200,'Soap-free gel cleanser suitable for sensitive skin.','2026-08-12 15:39:31'),(24,108,'Cream Cleanser for Dry Skin','DermaPure','Cream',2,379.00,4.2,298,NULL,180,'Nourishing cream cleanser that removes makeup without stripping skin.','2026-08-12 15:39:31'),(25,109,'Argan Oil Nourishing Shampoo','HairLux','Liquid',3,449.00,4.3,1032,NULL,220,'Sulphate-free shampoo enriched with argan oil.','2026-08-12 15:39:31'),(26,109,'Deep Conditioning Cream Conditioner','HairLux','Cream',2,399.00,4.2,588,NULL,195,'Rich conditioner that smooths and detangles hair.','2026-08-12 15:39:31'),(27,109,'Anti-Dandruff Gel Shampoo','HairLux','Gel',5,349.00,4.1,276,'New',175,'Clarifying gel shampoo that controls dandruff and scalp itch.','2026-08-12 15:39:31'),(28,110,'Frizz-Free Gel Hair Serum','HairLux','Gel',5,399.00,4.4,764,'Bestseller',180,'Lightweight gel serum for instant shine and frizz control.','2026-08-12 15:39:31'),(29,110,'Keratin Repair Hair Mask','HairLux','Cream',2,599.00,4.3,412,NULL,150,'Deep repair cream mask for damaged and chemically treated hair.','2026-08-12 15:39:31'),(30,110,'Coconut Hair Oil Treatment','HairLux','Oil',9,349.00,4.2,298,NULL,190,'Pure coconut oil treatment for deep hair nourishment.','2026-08-12 15:39:31'),(31,111,'Aloe Vera Body Gel','HairLux','Gel',5,349.00,4.2,690,NULL,230,'Cooling aloe vera gel for soothing, hydrated skin.','2026-08-12 15:39:31'),(32,111,'Coffee Body Scrub Cream','HairLux','Cream',2,449.00,4.5,523,'New',170,'Exfoliating coffee cream scrub for smooth, radiant skin.','2026-08-12 15:39:31'),(33,111,'Almond Body Oil','HairLux','Oil',9,399.00,4.3,267,NULL,160,'Lightweight almond oil that deeply moisturises skin.','2026-08-12 15:39:31'),(34,201,'Solitaire Diamond Ring','Aurelia','Diamond',15,24999.00,4.7,210,'Bestseller',25,'Elegant solitaire ring with certified diamond in 18K gold.','2026-08-12 15:39:31'),(35,201,'Classic Gold Band Ring','Aurelia','Gold',11,15999.00,4.5,156,NULL,40,'22K gold band ring with a polished finish.','2026-08-12 15:39:31'),(36,201,'Platinum Promise Ring','Aurelia','Platinum',14,28999.00,4.6,98,'New',20,'Minimalist platinum band ring for everyday elegance.','2026-08-12 15:39:31'),(37,202,'Pearl Drop Pendant Necklace','Aurelia','Pearl',16,3499.00,4.4,320,NULL,60,'Freshwater pearl pendant on a delicate gold chain.','2026-08-12 15:39:31'),(38,202,'Diamond Solitaire Pendant','Aurelia','Diamond',15,18999.00,4.6,187,'New',30,'Sparkling diamond pendant set in 18K white gold.','2026-08-12 15:39:31'),(39,202,'Classic Gold Chain Necklace','Aurelia','Gold',11,8999.00,4.3,145,'Bestseller',45,'22K gold chain necklace with a timeless design.','2026-08-12 15:39:31'),(40,203,'Rose Gold Cuff Bracelet','Aurelia','Rose Gold',13,4299.00,4.3,245,NULL,55,'Sleek rose gold cuff bracelet for everyday elegance.','2026-08-12 15:39:31'),(41,203,'Silver Charm Bangle Set','Aurelia','Silver',12,2199.00,4.1,198,'Bestseller',80,'Set of 4 silver bangles with delicate charm detailing.','2026-08-12 15:39:31'),(42,203,'Gold Kada Bangle','Aurelia','Gold',11,12999.00,4.5,87,'New',30,'Traditional gold kada bangle with engraved detailing.','2026-08-12 15:39:31'),(43,204,'Oxidised Silver Jhumka Earrings','Aurelia','Oxidised Silver',19,899.00,4.5,410,'Bestseller',100,'Handcrafted oxidised jhumkas with traditional detailing.','2026-08-12 15:39:31'),(44,204,'Gold Plated Hoop Earrings','Aurelia','Gold',11,1299.00,4.2,276,NULL,90,'Statement gold-plated hoops with a glossy finish.','2026-08-12 15:39:31'),(45,204,'Brass Statement Earrings','Aurelia','Brass',20,799.00,4.0,154,'New',110,'Bold brass statement earrings with a hammered texture.','2026-08-12 15:39:31'),(46,205,'Layered Gold Chain Necklace','Aurelia','Gold',11,3999.00,4.3,165,'New',65,'Triple-layered gold-toned chain necklace.','2026-08-12 15:39:31'),(47,205,'Pearl Studded Choker','Aurelia','Pearl',16,2799.00,4.2,132,NULL,50,'Elegant pearl-studded choker for festive occasions.','2026-08-12 15:39:31'),(48,205,'Silver Layered Choker Set','Aurelia','Silver',12,1999.00,4.1,98,'Bestseller',70,'Trendy silver layered choker set for a modern look.','2026-08-12 15:39:31'),(49,206,'Stainless Steel Stackable Ring Set','UrbanEdge','Stainless Steel',22,799.00,4.0,289,NULL,120,'Set of 3 minimalist stackable rings.','2026-08-12 15:39:31'),(50,206,'Silver Statement Cuff','UrbanEdge','Silver',12,1599.00,4.3,174,'New',70,'Bold silver cuff with geometric design.','2026-08-12 15:39:31'),(51,206,'Gold Plated Trendy Ring','UrbanEdge','Gold',11,899.00,4.1,132,'Bestseller',100,'Adjustable gold-plated trendy ring for everyday wear.','2026-08-12 15:39:31'),(52,207,'Kundan Bridal Necklace Set','Aurelia','Kundan',17,8999.00,4.6,143,'Bestseller',35,'Traditional Kundan necklace set with matching earrings.','2026-08-12 15:39:31'),(53,207,'Temple Gold Jewellery Set','Aurelia','Gold',11,10999.00,4.5,98,NULL,28,'South Indian temple-style jewellery set with pearl drops.','2026-08-12 15:39:31'),(54,207,'Pearl Temple Jewellery Set','Aurelia','Pearl',16,7999.00,4.4,76,'New',32,'Elegant pearl-accented temple jewellery set for weddings.','2026-08-12 15:39:31'),(55,208,'Kundan Maang Tikka','Aurelia','Kundan',17,1299.00,4.4,112,NULL,60,'Delicate Kundan maang tikka for bridal wear.','2026-08-12 15:39:31'),(56,208,'Gold Plated Matha Patti','Aurelia','Gold',11,1899.00,4.3,76,'New',40,'Statement matha patti with intricate gold-plated design.','2026-08-12 15:39:31'),(57,208,'Polki Bridal Maang Tikka','Aurelia','Polki',18,2499.00,4.5,54,'Bestseller',25,'Regal Polki-studded maang tikka for bridal ensembles.','2026-08-12 15:39:31'),(58,209,'Oxidised Silver Payal Pair','Aurelia','Oxidised Silver',19,999.00,4.4,234,'Bestseller',90,'Traditional oxidised silver anklets with bell detailing.','2026-08-12 15:39:31'),(59,209,'Silver Toe Ring Pair','Aurelia','Silver',12,599.00,4.1,145,NULL,100,'Adjustable pure silver toe ring pair.','2026-08-12 15:39:31'),(60,209,'Sterling Silver Anklet','Aurelia','Sterling Silver',23,1199.00,4.3,87,'New',65,'Minimalist sterling silver anklet with a delicate chain.','2026-08-12 15:39:31'),(61,210,'Diamond Nose Pin','Aurelia','Diamond',15,3499.00,4.5,87,NULL,45,'Delicate diamond nose pin set in gold.','2026-08-12 15:39:31'),(62,210,'Traditional Gold Nath','Aurelia','Gold',11,5999.00,4.6,64,'New',25,'Elegant Maharashtrian-style gold nath with pearl detailing.','2026-08-12 15:39:31'),(63,210,'Silver Nose Pin - Minimal','Aurelia','Silver',12,599.00,4.0,112,'Bestseller',90,'Simple silver nose pin for everyday elegance.','2026-08-12 15:39:31'),(64,301,'Classic Leather Stiletto Heels','StepStyle','Leather',26,2999.00,4.3,342,'Bestseller',75,'Pointed-toe stiletto heels crafted from genuine leather.','2026-08-12 15:39:31'),(65,301,'PU Leather Pump Heels','StepStyle','PU Leather',27,1999.00,4.0,210,NULL,90,'Comfortable everyday pumps in vegan PU leather.','2026-08-12 15:39:31'),(66,301,'Suede Block Pumps','StepStyle','Suede',28,2499.00,4.1,198,NULL,85,'Comfortable suede pumps with a subtle block heel.','2026-08-12 15:39:31'),(67,302,'PU Leather Block Heels','StepStyle','PU Leather',27,1799.00,4.0,256,NULL,95,'Everyday block heels with cushioned insole.','2026-08-12 15:39:31'),(68,302,'Leather Kitten Heel Sandals','StepStyle','Leather',26,2199.00,4.2,167,'New',70,'Elegant kitten heels perfect for office wear.','2026-08-12 15:39:31'),(69,302,'Suede Kitten Heel Mules','StepStyle','Suede',28,1899.00,4.1,121,'Bestseller',80,'Chic suede mules with a comfortable kitten heel.','2026-08-12 15:39:31'),(70,303,'Canvas Platform Wedges','StepStyle','Canvas',29,1599.00,4.1,189,NULL,100,'Casual canvas wedges with a comfortable platform sole.','2026-08-12 15:39:31'),(71,303,'Rubber Sole Espadrille Wedges','StepStyle','Rubber',31,1899.00,4.3,145,'Bestseller',65,'Espadrille-style wedges with a sturdy rubber sole.','2026-08-12 15:39:31'),(72,303,'Leather Platform Wedge Sandals','StepStyle','Leather',26,2299.00,4.2,98,'New',55,'Premium leather platform sandals for all-day comfort.','2026-08-12 15:39:31'),(73,304,'Embroidered Leather Juttis','Rajwadi','Leather',26,1299.00,4.5,278,'Bestseller',110,'Handcrafted embroidered juttis with a leather sole.','2026-08-12 15:39:31'),(74,304,'Woven Jute Mojris','Rajwadi','Jute',59,899.00,4.1,132,NULL,90,'Rustic woven jute mojris with traditional embroidery.','2026-08-12 15:39:31'),(75,304,'Printed Canvas Juttis','Rajwadi','Canvas',29,799.00,4.0,145,'New',100,'Lightweight printed canvas juttis for casual ethnic wear.','2026-08-12 15:39:31'),(76,305,'Suede Ballerina Flats','StepStyle','Suede',28,1499.00,4.2,210,NULL,120,'Soft suede ballerina flats for all-day comfort.','2026-08-12 15:39:31'),(77,305,'Leather Penny Loafers','StepStyle','Leather',26,1999.00,4.4,176,'New',85,'Classic leather loafers with a stitched detail.','2026-08-12 15:39:31'),(78,305,'Canvas Slip-on Ballerinas','StepStyle','Canvas',29,999.00,4.0,132,'Bestseller',130,'Comfortable canvas ballerinas for everyday casual wear.','2026-08-12 15:39:31'),(79,306,'Handmade Leather Kolhapuris','Rajwadi','Leather',26,1099.00,4.5,302,'Bestseller',130,'Traditional handcrafted Kolhapuri sandals.','2026-08-12 15:39:31'),(80,306,'Rubber Sole Flat Slides','StepStyle','Rubber',31,799.00,4.0,189,NULL,150,'Comfortable everyday flat slides.','2026-08-12 15:39:31'),(81,306,'Cork Footbed Kolhapuri Sandals','Rajwadi','Cork',56,1199.00,4.2,98,'New',75,'Handcrafted Kolhapuri sandals with a cushioned cork footbed.','2026-08-12 15:39:31'),(82,307,'Mesh Casual Sneakers','UrbanEdge','Mesh',30,1999.00,4.3,456,'Bestseller',160,'Breathable mesh sneakers for everyday casual wear.','2026-08-12 15:39:31'),(83,307,'Canvas Slip-on Shoes','UrbanEdge','Canvas',29,1299.00,4.1,267,NULL,140,'Easy slip-on canvas shoes with a rubber sole.','2026-08-12 15:39:31'),(84,307,'Rubber Sole Street Sneakers','UrbanEdge','Rubber',31,2199.00,4.2,198,'New',120,'Durable rubber-soled sneakers built for everyday city wear.','2026-08-12 15:39:31'),(85,308,'Lightweight Mesh Running Shoes','UrbanEdge','Mesh',30,2799.00,4.4,512,'Bestseller',180,'Cushioned running shoes with breathable mesh upper.','2026-08-12 15:39:31'),(86,308,'Rubber Grip Walking Shoes','UrbanEdge','Rubber',31,2299.00,4.2,298,NULL,155,'Comfortable walking shoes with a durable rubber sole.','2026-08-12 15:39:31'),(87,308,'Synthetic Sport Running Shoes','UrbanEdge','Synthetic',32,2499.00,4.1,234,'New',145,'Lightweight synthetic upper running shoes with flexible sole.','2026-08-12 15:39:31'),(88,309,'PVC Comfort Flip-Flops','UrbanEdge','PVC',35,399.00,4.0,389,NULL,220,'Lightweight PVC flip-flops for everyday comfort.','2026-08-12 15:39:31'),(89,309,'Rubber Beach Slides','UrbanEdge','Rubber',31,449.00,4.1,234,'New',190,'Durable rubber slides perfect for the beach or pool.','2026-08-12 15:39:31'),(90,309,'Cork Footbed Beach Slides','UrbanEdge','Cork',56,599.00,4.2,145,'Bestseller',160,'Cushioned cork footbed slides for all-day beach comfort.','2026-08-12 15:39:31'),(91,401,'Leather Everyday Tote Bag','Carriza','Leather',36,3499.00,4.4,267,'Bestseller',70,'Spacious genuine leather tote for daily use.','2026-08-12 15:39:31'),(92,401,'PU Leather Shoulder Bag','Carriza','PU Leather',37,1999.00,4.1,187,NULL,90,'Chic vegan leather shoulder bag with gold hardware.','2026-08-12 15:39:31'),(93,401,'Canvas Tote Bag','Carriza','Canvas',38,1499.00,4.0,154,'New',95,'Durable canvas tote, perfect for daily errands.','2026-08-12 15:39:31'),(94,402,'PU Leather Hobo Bag','Carriza','PU Leather',37,1999.00,4.2,178,NULL,80,'Soft-structured hobo bag with gold-tone hardware.','2026-08-12 15:39:31'),(95,402,'Structured Leather Satchel','Carriza','Leather',36,2999.00,4.3,143,'New',60,'Classic structured satchel with a detachable strap.','2026-08-12 15:39:31'),(96,402,'Canvas Hobo Bag','Carriza','Canvas',38,1399.00,4.0,98,'Bestseller',85,'Relaxed slouchy canvas hobo bag for everyday use.','2026-08-12 15:39:31'),(97,403,'Leather Crossbody Sling Bag','Carriza','Leather',36,1699.00,4.3,289,'Bestseller',110,'Compact leather sling bag with adjustable strap.','2026-08-12 15:39:31'),(98,403,'Canvas Crossbody Bag','Carriza','Canvas',38,999.00,4.0,176,NULL,130,'Lightweight canvas crossbody for everyday errands.','2026-08-12 15:39:31'),(99,403,'Nylon Sling Bag','Carriza','Nylon',39,899.00,4.1,132,'New',140,'Water-resistant nylon sling bag for everyday use.','2026-08-12 15:39:31'),(100,404,'Velvet Box Clutch','Carriza','Velvet',44,1499.00,4.4,132,'New',65,'Elegant velvet box clutch for evening occasions.','2026-08-12 15:39:31'),(101,404,'Leather Envelope Clutch','Carriza','Leather',36,1299.00,4.2,98,NULL,75,'Sleek leather envelope clutch with a magnetic closure.','2026-08-12 15:39:31'),(102,404,'PU Leather Box Clutch','Carriza','PU Leather',37,999.00,4.0,76,'Bestseller',85,'Structured vegan leather box clutch with chain strap.','2026-08-12 15:39:31'),(103,405,'Velvet Potli Bag with Beadwork','Rajwadi','Velvet',44,799.00,4.3,156,NULL,90,'Richly beaded velvet potli bag for festive wear.','2026-08-12 15:39:31'),(104,405,'Embroidered Cotton Potli Bag','Rajwadi','Cotton',43,599.00,4.1,132,'New',100,'Handwoven cotton potli bag with traditional embroidery.','2026-08-12 15:39:31'),(105,405,'Jute Potli Bag with Tassels','Rajwadi','Jute',42,499.00,4.0,87,'Bestseller',110,'Eco-friendly jute potli bag with decorative tassels.','2026-08-12 15:39:31'),(106,406,'Velvet Evening Pouch','Carriza','Velvet',44,1099.00,4.2,121,NULL,80,'Compact velvet pouch with a sequin finish.','2026-08-12 15:39:31'),(107,406,'Leather Party Pouch','Carriza','Leather',36,1399.00,4.1,87,'New',60,'Sleek leather party pouch with a chain strap.','2026-08-12 15:39:31'),(108,406,'PU Leather Clutch Pouch','Carriza','PU Leather',37,899.00,4.0,65,'Bestseller',95,'Affordable vegan leather clutch pouch for evenings out.','2026-08-12 15:39:31'),(109,407,'Nylon Everyday Backpack','UrbanEdge','Nylon',39,1999.00,4.3,345,'Bestseller',140,'Durable water-resistant nylon backpack with laptop compartment.','2026-08-12 15:39:31'),(110,407,'Canvas Mini Backpack','UrbanEdge','Canvas',38,1299.00,4.1,198,NULL,120,'Compact canvas mini backpack for casual outings.','2026-08-12 15:39:31'),(111,407,'Polyester Travel Backpack','UrbanEdge','Polyester',40,1799.00,4.2,176,'New',110,'Lightweight polyester backpack with multiple compartments.','2026-08-12 15:39:31'),(112,408,'Leather Bifold Wallet','Carriza','Leather',36,899.00,4.4,267,'Bestseller',160,'Slim genuine leather bifold wallet with card slots.','2026-08-12 15:39:31'),(113,408,'PU Leather Card Holder','Carriza','PU Leather',37,399.00,4.0,145,NULL,200,'Compact card holder with multiple card slots.','2026-08-12 15:39:31'),(114,408,'Canvas Zip Wallet','Carriza','Canvas',38,449.00,4.1,98,'New',170,'Casual canvas zip-around wallet with coin pocket.','2026-08-12 15:39:31'),(115,409,'Canvas Laptop Sleeve','UrbanEdge','Canvas',38,699.00,4.1,178,NULL,160,'Padded canvas sleeve for 13-15 inch laptops.','2026-08-12 15:39:31'),(116,409,'Leather Laptop Sleeve','UrbanEdge','Leather',36,1299.00,4.3,132,'Bestseller',90,'Premium leather sleeve with a soft interior lining.','2026-08-12 15:39:31'),(117,409,'Nylon Travel Organiser Pouch','UrbanEdge','Nylon',39,599.00,4.0,154,'New',170,'Multi-compartment nylon pouch for travel essentials.','2026-08-12 15:39:31'),(118,501,'Blooming Rose Eau de Parfum','Essenza','Floral',46,1499.00,4.5,432,'Bestseller',120,'A romantic floral fragrance with notes of rose and jasmine.','2026-08-12 15:39:31'),(119,501,'Peach Blossom Fruity Perfume','Essenza','Fruity',55,1199.00,4.2,289,NULL,140,'A fresh fruity scent with juicy peach top notes.','2026-08-12 15:39:31'),(120,501,'Musk Blossom Eau de Toilette','Essenza','Musk',51,1399.00,4.3,198,'New',110,'A soft musky floral fragrance for everyday elegance.','2026-08-12 15:39:31'),(121,502,'Sandalwood Amber Perfume','Essenza','Woody',47,1799.00,4.6,356,'Bestseller',90,'A warm woody fragrance with sandalwood and amber base.','2026-08-12 15:39:31'),(122,502,'Oud Oriental Eau de Parfum','Essenza','Oriental',48,2199.00,4.4,198,'New',70,'An intense oriental fragrance layered with oud and spice.','2026-08-12 15:39:31'),(123,502,'Amber Musk Night Perfume','Essenza','Amber',53,1999.00,4.3,143,'Bestseller',80,'A rich amber fragrance perfect for evening wear.','2026-08-12 15:39:31'),(124,503,'Citrus Splash Eau de Cologne','Essenza','Citrus',50,999.00,4.1,267,NULL,160,'A zesty citrus cologne perfect for daily wear.','2026-08-12 15:39:31'),(125,503,'Ocean Breeze Fresh Perfume','Essenza','Fresh',49,1099.00,4.3,210,'Bestseller',150,'An invigorating fresh fragrance inspired by the sea breeze.','2026-08-12 15:39:31'),(126,503,'Aquatic Cool Eau de Toilette','Essenza','Aquatic',54,1249.00,4.2,176,'New',130,'A crisp aquatic fragrance with a cool, clean trail.','2026-08-12 15:39:31'),(127,504,'Citrus Burst Body Spray','Essenza','Citrus',50,349.00,4.0,512,NULL,250,'Long-lasting citrus-scented deodorant body spray.','2026-08-12 15:39:31'),(128,504,'Fresh Cool Deodorant Spray','Essenza','Fresh',49,299.00,4.1,398,'Bestseller',270,'24-hour protection deodorant with a fresh cooling scent.','2026-08-12 15:39:31'),(129,504,'Aquatic Splash Deodorant','Essenza','Aquatic',54,329.00,4.0,234,'New',230,'Refreshing aquatic deodorant spray for all-day freshness.','2026-08-12 15:39:31'),(130,505,'Floral Fantasy Body Mist','Essenza','Floral',46,449.00,4.2,345,NULL,200,'Light floral body mist for a delicate everyday scent.','2026-08-12 15:39:31'),(131,505,'Tropical Fruit Body Mist','Essenza','Fruity',55,399.00,4.0,276,'New',220,'Refreshing fruity body mist with tropical notes.','2026-08-12 15:39:31'),(132,505,'Vanilla Bloom Body Mist','Essenza','Vanilla',52,429.00,4.3,198,'Bestseller',210,'Sweet vanilla-floral body mist for a cozy everyday scent.','2026-08-12 15:39:31'),(133,506,'Floral Discovery Miniature Set','Essenza','Floral',46,1999.00,4.5,187,'Bestseller',60,'A curated set of 5 miniature floral signature fragrances.','2026-08-12 15:39:31'),(134,506,'Woody Luxury Sampler Box','Essenza','Woody',47,2299.00,4.4,132,'New',50,'Premium sampler box featuring 6 woody luxury fragrances.','2026-08-12 15:39:31'),(135,506,'Oriental Discovery Collection','Essenza','Oriental',48,2499.00,4.5,98,'Bestseller',45,'An exclusive discovery set of rich oriental fragrances.','2026-08-12 15:39:31'),(136,507,'Travel-Size Fresh Perfume Duo','Essenza','Fresh',49,699.00,4.1,165,NULL,130,'Compact travel-friendly perfume duo, perfect for on-the-go.','2026-08-12 15:39:31'),(137,507,'Pocket Citrus Atomiser Set','Essenza','Citrus',50,599.00,4.0,143,'New',150,'Refillable pocket citrus atomiser set for daily freshness.','2026-08-12 15:39:31'),(138,507,'Mini Floral Travel Spray','Essenza','Floral',46,649.00,4.2,121,'Bestseller',140,'Compact floral travel spray, perfect for handbags.','2026-08-12 15:39:31');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sellers`
--

DROP TABLE IF EXISTS `sellers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sellers` (
  `seller_id` int NOT NULL AUTO_INCREMENT,
  `shop_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gst_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pan_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pincode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('Pending','Approved','Rejected','Suspended') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `shop_logo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gst_certificate` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pan_document` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_image_1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_image_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_image_3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`seller_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sellers`
--

LOCK TABLES `sellers` WRITE;
/*!40000 ALTER TABLE `sellers` DISABLE KEYS */;
INSERT INTO `sellers` VALUES (1,'anistock','Kabir thapa','kabirthapa123@gmail.com','8167482381','scrypt:32768:8:1$ByXcw9k3xm3BcGwW$31346464400191b931dd4adab0df764b8eae4fecf2ca812a98f0022d24ad6af43ede79df9de4dc27899e11904d4d1e9694036ecba28ae4a169cf69e2a891518f','184515','HBAD95AL','nnan','sili','WB','734003','Jewellery','Approved','2026-08-13 07:18:15','uploads/shop_logos/8.png','uploads/gst/8.png','uploads/pan/8.png','uploads/products/footwear_2.jpg','uploads/products/footwear_2.jpg','uploads/products/footwear_3.jpg');
/*!40000 ALTER TABLE `sellers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_categories`
--

DROP TABLE IF EXISTS `sub_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_categories` (
  `sub_category_id` int NOT NULL AUTO_INCREMENT,
  `main_category_id` int NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sub_category_id`),
  UNIQUE KEY `uq_subcat_per_main` (`main_category_id`,`slug`),
  CONSTRAINT `fk_subcat_maincat` FOREIGN KEY (`main_category_id`) REFERENCES `main_categories` (`main_category_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_categories`
--

LOCK TABLES `sub_categories` WRITE;
/*!40000 ALTER TABLE `sub_categories` DISABLE KEYS */;
INSERT INTO `sub_categories` VALUES (1,1,'Makeup','makeup','2026-08-08 15:27:48'),(2,1,'Skincare','skincare','2026-08-08 15:27:48'),(3,1,'Haircare & Body Care','haircare-body-care','2026-08-08 15:27:48'),(4,2,'Fine & Precious Jewellery','fine-precious-jewellery','2026-08-08 15:29:43'),(5,2,'Fashion & Costume Jewellery','fashion-costume-jewellery','2026-08-08 15:29:43'),(6,2,'Traditional & Bridal','traditional-bridal','2026-08-08 15:29:43'),(7,3,'Heels & Wedges','heels-wedges','2026-08-08 15:29:43'),(8,3,'Flats & Ethnic','flats-ethnic','2026-08-08 15:29:43'),(9,3,'Casual & Sports','casual-sports','2026-08-08 15:29:43'),(10,4,'Handbags & Everyday','handbags-everyday','2026-08-08 15:29:43'),(11,4,'Evening & Occasion','evening-occasion','2026-08-08 15:29:43'),(12,4,'Travel & Utility','travel-utility','2026-08-08 15:29:43'),(13,5,'Perfumes','perfumes-sub','2026-08-08 15:29:43'),(14,5,'Daily Wear & Mists','daily-wear-mists','2026-08-08 15:29:43'),(15,5,'Gift Sets & Minis','gift-sets-minis','2026-08-08 15:29:43'),(16,6,'Latest Collections','latest-collections','2026-08-08 15:29:43');
/*!40000 ALTER TABLE `sub_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profile_image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT 'default.png',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-13 21:09:52
