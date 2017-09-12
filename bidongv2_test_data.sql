-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: 172.16.36.11    Database: bidongv2
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.22-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrators`
--

DROP TABLE IF EXISTS `administrators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrators` (
  `id` int(10) NOT NULL COMMENT 'administrator_id',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'name of the admin',
  `description` varchar(256) NOT NULL DEFAULT '' COMMENT 'brief of the admin',
  `mobile` bigint(20) NOT NULL COMMENT '手機號',
  `status` tinyint(5) NOT NULL DEFAULT '1' COMMENT '状态，2为删除，1为可用，0为不可用',
  `create_time` int(10) NOT NULL DEFAULT '0' COMMENT '创建时间，时间戳',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrators`
--

LOCK TABLES `administrators` WRITE;
/*!40000 ALTER TABLE `administrators` DISABLE KEYS */;
INSERT INTO `administrators` VALUES (1336353101,'奥德赛','13233334444',13233334444,1,1504681094),(1410683360,'18925152222','测试1111',18925152222,2,1504495218),(1525483113,'曾鼎','开发工程师',13333333333,1,1504238939),(1710237450,'18925151111','456',18925151111,1,1504494777),(1821039510,'SD','不要温柔地走进那个良夜',13422223333,1,1504252420),(1855102589,'974','123',13410238888,1,1504752145),(1874801325,'18925153758','',18925153758,1,1504250717);
/*!40000 ALTER TABLE `administrators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administrators_authorization`
--

DROP TABLE IF EXISTS `administrators_authorization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrators_authorization` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `authorization_holder` int(10) NOT NULL COMMENT '被授权主体的身份ID，可以是管理员id也可以是管理员组id',
  `holder_type` int(10) NOT NULL DEFAULT '0' COMMENT '被授权主体的类型,比如管理员,管理员组,默认为0代表一般的管理员个体, 将来扩展时详细定义',
  `resource_id` int(11) NOT NULL COMMENT '资源id, 对应于resource_registry表中的id字段',
  `resource_name` varchar(64) NOT NULL DEFAULT '' COMMENT '资源名称, public_name',
  `resource_locator` varchar(128) NOT NULL DEFAULT '' COMMENT '资源定位符, 一个具体资源在其所属类别中的标识符, 根据resource_id和resource_locator可以定位到一个资源, 类似uri的作用，留空时表示该类别中的所有资源',
  `allow_method` tinyint(4) NOT NULL DEFAULT '15' COMMENT '参考Linux文件权限,8为读,4为增,2为改,1为删,如有多个权限,累加.判断是否有某个权限时,比如最终结果为15,15 and 8 = 8,那么则为有读权限.',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否生效,1为是,0为否',
  PRIMARY KEY (`id`),
  UNIQUE KEY `authorization_holder` (`authorization_holder`,`resource_name`,`resource_locator`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrators_authorization`
--

LOCK TABLES `administrators_authorization` WRITE;
/*!40000 ALTER TABLE `administrators_authorization` DISABLE KEYS */;
INSERT INTO `administrators_authorization` VALUES (1,1525483113,0,4,'platform_executor_management','',15,1),(2,1525483113,0,1,'platform_project_management','',15,1),(3,1874801325,0,2,'platform_user_management','',15,1),(4,1874801325,0,6,'platform_operation_management','',15,2),(5,1874801325,0,4,'platform_executor_management','',15,1),(6,1874801325,0,1,'platform_project_management','',15,1),(7,1874801325,0,5,'platform_finance_management','',15,2),(8,1821039510,0,5,'platform_finance_management','',15,1),(9,1821039510,0,1,'platform_project_management','',15,1),(10,1821039510,0,4,'platform_executor_management','',15,1),(11,1821039510,0,6,'platform_operation_management','',15,1),(12,1821039510,0,2,'platform_user_management','',15,1),(13,1525483113,0,6,'platform_operation_management','',15,1),(14,1525483113,0,2,'platform_user_management','',15,1),(15,1525483113,0,5,'platform_finance_management','',15,1),(18,1710237450,0,1,'platform_project_management','',15,1),(19,1710237450,0,6,'platform_operation_management','',15,1),(20,1710237450,0,5,'platform_finance_management','',15,1),(21,1710237450,0,2,'platform_user_management','',15,1),(22,1710237450,0,4,'platform_executor_management','',15,1),(23,1410683360,0,6,'platform_operation_management','',15,1),(24,1410683360,0,1,'platform_project_management','',15,1),(25,1410683360,0,2,'platform_user_management','',15,1),(26,1410683360,0,5,'platform_finance_management','',15,1),(27,1410683360,0,4,'platform_executor_management','',15,1),(28,1336353101,0,1,'platform_project_management','',15,1),(29,1336353101,0,2,'platform_user_management','',15,1),(30,1336353101,0,4,'platform_executor_management','',15,1),(31,1336353101,0,5,'platform_finance_management','',15,1),(32,1336353101,0,6,'platform_operation_management','',15,1),(33,1855102589,0,4,'platform_executor_management','',15,1),(34,1855102589,0,1,'platform_project_management','',15,1),(35,1855102589,0,2,'platform_user_management','',15,1),(36,1855102589,0,5,'platform_finance_management','',15,2),(37,1855102589,0,6,'platform_operation_management','',15,2);
/*!40000 ALTER TABLE `administrators_authorization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administrators_password`
--

DROP TABLE IF EXISTS `administrators_password`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administrators_password` (
  `id` int(10) NOT NULL COMMENT 'administrator_id',
  `user_name` varchar(64) NOT NULL DEFAULT '' COMMENT '登錄的用戶名',
  `email` varchar(128) NOT NULL DEFAULT '' COMMENT '登錄用郵箱',
  `mobile` bigint(20) NOT NULL DEFAULT '0' COMMENT '登錄用手機號',
  `password` varchar(512) NOT NULL COMMENT '當前加鹽的密碼',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否已經重置 1為是 0為否',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrators_password`
--

LOCK TABLES `administrators_password` WRITE;
/*!40000 ALTER TABLE `administrators_password` DISABLE KEYS */;
INSERT INTO `administrators_password` VALUES (1336353101,'','',13233334444,'pbkdf2:sha256:50000$izYtAFxC$c74dccf64b6e65a895201654a34b7f0dc03d96a723ec96bb57ad2dbca6365066',0),(1410683360,'','',18925152222,'pbkdf2:sha256:50000$S32HGa4l$fe710ccc7c1adb4295f8dcc62074d73ca0a443c488e3f5b0b7fece4188b1ed15',0),(1525483113,'','',13333333333,'pbkdf2:sha256:50000$V27iDgKm$355e6d23d2af3d5f366ff707a2fd32cf3e0f3f665c58fc4ccf8e529c1615321f',1),(1710237450,'','',18925151111,'pbkdf2:sha256:50000$VH2HaImV$3b5b5bd9ce93bb1f4bf6f45e82893f34fe30537194cb7a9062fc4c6e2b0b8ce8',0),(1821039510,'','',13422223333,'pbkdf2:sha256:50000$eUyco6MB$7a1ad661a338e9809d438b32bed4fa087a55a05ebc2158d216a305bc9d90d34c',0),(1855102589,'','',13410238888,'pbkdf2:sha256:50000$RI8mPL74$e63f8337868c2293442a0a9330560ebab57c76ce89d263a408811b94d03f5205',0),(1874801325,'','',18925153758,'pbkdf2:sha256:50000$Lw23DIxU$f035f0f9e29a11a5c5cfbe90285b68d2d9b2dd7fd7f2464c49fbd8a41be07122',0);
/*!40000 ALTER TABLE `administrators_password` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_ac`
--

DROP TABLE IF EXISTS `bd_ac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_ac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '设备名称',
  `vendor` varchar(32) NOT NULL COMMENT '设备厂商',
  `ip` varchar(32) NOT NULL COMMENT 'ac的工作ip地址（内网或者外网)',
  `secret` varchar(64) NOT NULL COMMENT '设备安全字段，Radius报文使用',
  `coa_port` smallint(6) NOT NULL DEFAULT '3799' COMMENT '管理后台不对改字段做配置',
  `pip` varchar(15) NOT NULL DEFAULT '' COMMENT '映射公网地址',
  `port` smallint(6) unsigned NOT NULL DEFAULT '0' COMMENT '映射公网端口',
  `created_at` datetime NOT NULL null COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ac_ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_ac`
--

LOCK TABLES `bd_ac` WRITE;
/*!40000 ALTER TABLE `bd_ac` DISABLE KEYS */;
INSERT INTO `bd_ac` VALUES (2,'232','xinrui','255.0.12.34','7h45h4',3799,'',0,'2017-08-29 14:19:35'),(4,'string','xinrui','255.0.12.35','string',3799,'',0,'2017-08-29 16:43:22'),(7,'2017-8-9','huawei','255.0.12.12','1234',3799,'',0,'2017-09-01 16:13:50'),(8,'信锐AC','xinrui','10.20.0.110','这个测试也不知道',3799,'',0,'2017-09-04 10:44:34'),(10,'130456','huawei','10.20.0.130','123456',3799,'',0,'2017-09-05 14:42:47');
/*!40000 ALTER TABLE `bd_ac` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_account`
--

DROP TABLE IF EXISTS `bd_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_account` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '上网账号',
  `password` varchar(128) NOT NULL COMMENT '上网密码',
  `name` varchar(64) DEFAULT NULL COMMENT '用户姓名',
  `mask` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '账号标识,mask & (1 << 30) > 0账号被停用, mask & 1 > 0 已激活',
  `coin` int(11) unsigned DEFAULT '0' COMMENT '壁咚币, 1壁咚币=10分钟',
  `ends` smallint(5) unsigned DEFAULT '1' COMMENT '同时上网终端上限',
  `mobile` varchar(17) NOT NULL DEFAULT '' COMMENT '用户手机号码',
  `created_at` datetime  COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  `nickname` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_account_user` (`user`),
  UNIQUE KEY `uk_account_mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=12153 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_account`
--

LOCK TABLES `bd_account` WRITE;
/*!40000 ALTER TABLE `bd_account` DISABLE KEYS */;
INSERT INTO `bd_account` VALUES (12000,'12000','pbkdf2:sha256:50000$cKsEUStU$33699497d8e9c318879087db965a6b159048f8a969b5a4abe475a89816e6760b','阿斯蒂芬',1,0,3,'13322223333','2017-07-28 15:18:20','2017-09-07 10:55:41',''),(12001,'12001','pbkdf2:sha256:50000$10I93XUT$469ebc8c3346e3a55dc5ebf252e8b6eddd8fd1830689fde5d0fd632cf015bf00','老大哥',1,0,3,'13399998888','2017-07-28 17:48:38','2017-09-07 10:55:41',''),(12002,'12002','pbkdf2:sha256:50000$pyzmsPZN$2e99b8d28190fd9dc43ba70bef58a069a8282273c52c3616a6d4e63a0c422345','吖吖',1,0,3,'18198982323','2017-07-31 10:14:22','2017-09-07 10:55:41',''),(12003,'12003','pbkdf2:sha256:50000$kC4rRoW6$7e1b3854871a2157578425f26da6e7b7701ad9c0d2f8b029329bb5f424a5aa75','万维网',1,0,3,'13298985858','2017-07-31 10:15:25','2017-09-07 10:55:41',''),(12004,'12004','pbkdf2:sha256:50000$NmpPSSna$379473aad9b3b79a1c0dd3c4b732f5cedff6a8a8d979bf383a961a238351a7c3','奥德赛',1,0,3,'13233334444','2017-07-31 10:19:18','2017-09-07 10:55:41',''),(12005,'12005','pbkdf2:sha256:50000$0hgxR2e2$4a6e35b047490b3bc712b4402da17b5fe2f890681ed1a37b30d36eba397440a9','张里',1,0,3,'13333333333','2017-07-31 10:20:18','2017-09-07 10:55:41',''),(12006,'12006','pbkdf2:sha256:50000$yNffUJ8r$13df4c6050b51ec4a471dca36206625b392a1a9bd6da24c025ef05ddba2b44a8','张是',1,0,3,'13222224444','2017-07-31 10:20:52','2017-09-07 10:55:41',''),(12007,'12007','pbkdf2:sha256:50000$pvsiYbMt$0147886ba6c2da8b3b00c89263da11a8a12012db38a0fe58846b461972690ce4','张思',1,0,3,'13244443333','2017-07-31 10:21:10','2017-09-07 10:55:41',''),(12008,'12008','pbkdf2:sha256:50000$e1WDMGHr$8eeb40b4e65bb690fcc347b6b40bf553fceafaacd49a0b0ef029df1f9444f9a0','张螺',1,0,3,'13321212323','2017-07-31 10:21:51','2017-09-07 10:55:41',''),(12009,'12009','pbkdf2:sha256:50000$v1pZsJhJ$ae30d8c2ae93210c2583981fdc23bb6ac923f32c7cbad79e21fd498670f8a171','张斯蒂芬',1,0,3,'13822232223','2017-07-31 13:59:28','2017-09-07 10:55:41',''),(12010,'12010','pbkdf2:sha256:50000$qsCkqUDc$62f6053664be099905e6042c8e73b71c7521acfc76ec3a808144a5c0993a99c0','张斯蒂芬',1,0,3,'13911121112','2017-07-31 14:00:02','2017-09-07 10:55:41',''),(12011,'12011','pbkdf2:sha256:50000$sOkBPSAJ$55f853557f581517ea9e943f7b2b93214a3bb138bfb60ecd3211613b89171291','张坡',1,0,3,'13711121112','2017-07-31 14:00:43','2017-09-07 10:55:41',''),(12012,'12012','pbkdf2:sha256:50000$YgLxjfrF$c484b059ea7770b675b6a29eabb0961900ca9b4e7de3b0bd371c4919011a9c93','1',1,0,3,'13311112222','2017-07-31 14:53:10','2017-09-07 10:55:41',''),(12013,'12013','pbkdf2:sha256:50000$LaKduuKS$5517274b04625eeb75d1e47c5cecadeebf5b25f24d29d29efce0f609c4c1f10c','Wong',1,0,3,'13612444229','2017-08-01 10:05:45','2017-09-07 10:55:41',NULL),(12014,'12014','pbkdf2:sha256:50000$6vRixLRS$ae8a626ea78ac5589df981428f36e398c1ffad92737fbd1cb2c6a9dc17ba1ade','鹏',1,0,3,'13211112222','2017-08-01 10:12:04','2017-09-07 10:55:41',NULL),(12015,'12015','pbkdf2:sha256:50000$xlutaais$d58629d8e89a3429f7d0ede8f72cfd1132f9d605c9decd7131b5dd39cf1ae565','东方',1,0,3,'13456665565','2017-08-01 10:33:00','2017-09-07 10:55:41',NULL),(12016,'12016','pbkdf2:sha256:50000$YBc8LN8p$cdabf72dfd038853b1b90979504f0d8168a69bb6011b1eedb86d52fc5408cc77','老吴',1,0,3,'13222323322','2017-08-01 10:48:13','2017-09-07 10:55:41',NULL),(12017,'12017','pbkdf2:sha256:50000$bnfYDnWd$7f728a8e272ed6e5e3a913be0d4d2b80e8dadbad7cd473afe02abe3a8e80848e','SD',1,0,3,'13422223333','2017-08-01 11:25:20','2017-09-07 10:55:41',NULL),(12018,'12018','pbkdf2:sha256:50000$hw173ueK$252a14081e189c4064e4341b3113a2b449c046b24c2fa1dbf570bb777e1cbb7f','达菲',1,0,3,'13577776666','2017-08-01 11:25:43','2017-09-07 10:55:41',NULL),(12019,'12019','pbkdf2:sha256:50000$Gv1rqS8F$12bf280d7864f988a1d2922540a1f6db61720927aed5829ac7584a95249ec945','奥地利',1,0,3,'13233332222','2017-08-01 11:26:59','2017-09-07 10:55:41',NULL),(12020,'12020','pbkdf2:sha256:50000$hv4w5Bka$bdc9b22daf4e1234c993f5488c6824dff8098388db05e21d693f3b95eaba9b72','Chou',1,0,3,'13612444336','2017-08-01 12:19:13','2017-09-07 10:55:41',NULL),(12021,'12021','pbkdf2:sha256:50000$48FCuq3j$5db7ef30f97739ecb3a2c592219cc1a7cdb8af7bb76472c2fc6847b20c06bc50','Tom',1,0,3,'13198643087','2017-08-01 13:13:21','2017-09-07 10:55:41',NULL),(12022,'12022','pbkdf2:sha256:50000$OAtit4rb$29aadcd4a2a3e0a13461f0190b1a6997eb4be4db82c22b03f1768b96e4240b13','ABC',1,0,3,'13722223333','2017-08-01 13:17:01','2017-09-07 10:55:41',NULL),(12023,'12023','pbkdf2:sha256:50000$hIPoFIlm$6ca6888b8f60ba836faedf8eaefc363796a4250718e5c9ed2288d88b10852f2f','Perel',1,0,3,'13899990000','2017-08-01 13:24:19','2017-09-07 10:55:41',NULL),(12024,'12024','pbkdf2:sha256:50000$VwA2TiZZ$f32fe202aaafd7e612db71a7d7afb2807ca8190d46c72610d25809210af42966','Lsadu',1,0,3,'13900003333','2017-08-01 13:27:25','2017-09-07 10:55:41',NULL),(12025,'12025','pbkdf2:sha256:50000$gMIABG9z$1a0572608b7c7808b3ec793e2830d89d090587bea30f7c1444a3456a46b696d9','Uasdf',1,0,3,'13299993333','2017-08-01 13:28:21','2017-09-07 10:55:41',NULL),(12026,'12026','pbkdf2:sha256:50000$QGkByPlz$0dec4fdf0fafc5e7763e0876f07a3cdfffba1f96fec6ce454b9983fb1f11f049','Yjsd',1,0,3,'18399992222','2017-08-01 13:56:06','2017-09-07 10:55:41',NULL),(12027,'12027','pbkdf2:sha256:50000$JNcq6KQW$62c9addf2b16187f2ff5328591653ddf2cfd37424ed9a8ff1d63077fe2d4f509','Duel',1,0,3,'13722232223','2017-08-01 14:43:56','2017-09-07 10:55:41',NULL),(12028,'12028','pbkdf2:sha256:50000$2iz95zER$af7034016b3aa6c6518c38b62d8fe3ef61381cabdf8e877ec5adf7ed1ced1a75','Wrgr',1,0,3,'13855556666','2017-08-04 09:24:59','2017-09-07 10:55:41',NULL),(12029,'12029','pbkdf2:sha256:50000$yUNqnxyz$731758d155619803740e224ce56e1ae640ee22860b2746b4c00646ca53398cf7','Rsas',1,0,3,'13009983333','2017-08-04 09:25:49','2017-09-07 10:55:41',NULL),(12030,'12030','pbkdf2:sha256:50000$jUKE3ybN$4dc3598c9010724ea1d820cd8591bd0d53cfbd98a469451c8c5dab4934d82b6c','Sssss',1,0,3,'13788889999','2017-08-04 09:29:35','2017-09-07 10:55:41',NULL),(12031,'12031','pbkdf2:sha256:50000$xdpzpj5Q$d5ca9bae29f0b1af6b5822afec232b22047334c51218c31248ca83ec0f94e933','Peif',1,0,3,'13888888888','2017-08-04 10:13:26','2017-09-07 10:55:41',NULL),(12032,'12032','pbkdf2:sha256:50000$zdO1OHix$29c252066e3220faeaaa6bb881379d72b8cb29c420e3255e6d26a21f2b69aae5','Ysfe',1,0,3,'13688875468','2017-08-04 10:13:47','2017-09-07 10:55:41',NULL),(12033,'12033','pbkdf2:sha256:50000$jQVmwGOD$991f634fecaf9aa8989410fa9c5532762bb70a5866e0e14f6aa17e6b71565e09','Ysfe',1,0,3,'13688875123','2017-08-04 10:13:53','2017-09-07 10:55:41',NULL),(12034,'12034','pbkdf2:sha256:50000$5iWmB6fz$9182f91ab19d5d70f7e38ba9d969bc7eccfdd073aeefb07bac790f6c759955a0','Vrad',1,0,3,'13688871234','2017-08-04 10:14:20','2017-09-07 10:55:41',NULL),(12035,'12035','pbkdf2:sha256:50000$EFUJfHwj$e7842ba4ad30ce49ce1fc40de25834fa39e2c1614c2d34e7689adc670b9a2d28','Vab',1,0,3,'13688871233','2017-08-04 10:14:29','2017-09-07 10:55:41',NULL),(12036,'12036','pbkdf2:sha256:50000$RhqaYO4r$8395150500d9982e538f91c8f4ae848107e64ba26d907b467750f17513cb584b','Vab',1,0,3,'13683871233','2017-08-04 10:14:36','2017-09-07 10:55:41',NULL),(12037,'12037','pbkdf2:sha256:50000$xhp4nYJL$3a0065e6127017ff205be9cfd863879fe9d5899d4bb83fccb49d911cb36818b8','Vaba',1,0,3,'13383871233','2017-08-04 10:14:44','2017-09-07 10:55:41',NULL),(12038,'12038','pbkdf2:sha256:50000$XeqKkQgO$41e5f919e50ef2244a84645ef03e7d5ec28ea5d96be70f3e60b90748e3842ba3','Vaba',1,0,3,'13383871238','2017-08-04 10:14:48','2017-09-07 10:55:41',NULL),(12039,'12039','pbkdf2:sha256:50000$k6FKcJmu$7c2d9f0c0c3d332ca265e3a66527d055cacddb8b87a9382b94d987a609519001','Vaba',1,0,3,'13383871638','2017-08-04 10:14:51','2017-09-07 10:55:41',NULL),(12040,'12040','pbkdf2:sha256:50000$JzEQZu9d$9e3908e94299107c6759691d08beec8ed7ba4529943c3f7983e935d49bb9bcb9','Vaba',1,0,3,'13383871678','2017-08-04 10:14:53','2017-09-07 10:55:41',NULL),(12041,'12041','pbkdf2:sha256:50000$cpCUzJrY$da1df3bccb6b65f9babb8f4bea5c89e8bc463c6c68b0f6759dfc9e7718b79092','Vaba',1,0,3,'13385871678','2017-08-04 10:14:55','2017-09-07 10:55:41',NULL),(12042,'12042','pbkdf2:sha256:50000$xeZ9BaiS$530f02f89e718d6129c517ceedbb36f53425802d4ea084b914074ab86d9c8f5f','Vaba',1,0,3,'13385771678','2017-08-04 10:14:58','2017-09-07 10:55:41',NULL),(12043,'12043','pbkdf2:sha256:50000$O02qVlQb$9dcf618116f9032bcbe6b3649f19a1bc1c3c425d7607bc04ea242471322b9b8f','Vaba',1,0,3,'13385771878','2017-08-04 10:15:01','2017-09-07 10:55:41',NULL),(12044,'12044','pbkdf2:sha256:50000$yxVt2Qyj$b8f7b17cfbbfb02e4be5a26b3c3a6058ac65eca76d6b06a9347ec325b3c6a0f3','Vaba',1,0,3,'13389771878','2017-08-04 10:15:04','2017-09-07 10:55:41',NULL),(12045,'12045','pbkdf2:sha256:50000$o1u2k1aN$4eaa377ba002a68c27276b1c8e7f078e768c851a3e747551f68b7d96700997f6','Vaba',1,0,3,'13389771578','2017-08-04 10:15:06','2017-09-07 10:55:41',NULL),(12046,'12046','pbkdf2:sha256:50000$unaYbbOJ$9f87432c19b13877edfcb78d06b39ef4bcbd76833966415f0499a6ab813c0b24','Vaba',1,0,3,'13389771570','2017-08-04 10:15:13','2017-09-07 10:55:41',NULL),(12047,'12047','pbkdf2:sha256:50000$hE3Q9XMc$d1fd35e4260dbed5c5e48aa2430fe2e61407f8299dc3da5173bb19a64653f6bc','Vaba',1,0,3,'13380771570','2017-08-04 10:15:16','2017-09-07 10:55:41',NULL),(12048,'12048','pbkdf2:sha256:50000$kdTafxcD$ef39a1fd61967d1f0ac0e1d4bc17c83fbc2ca360e5fcfd95ba5069301b8a0e6d','Vaba',1,0,3,'13380071570','2017-08-04 10:15:19','2017-09-07 10:55:41',NULL),(12049,'12049','pbkdf2:sha256:50000$L84hqO6l$7fbb4e63571b1dc9fb21cdc6565e3be7decbe82a83a2f56f846ef78bc5400f1f','Vaba',1,0,3,'13380001570','2017-08-04 10:15:21','2017-09-07 10:55:41',NULL),(12050,'12050','pbkdf2:sha256:50000$bGrTjKSl$61464ac674d4a5c9e01b927453f30b01f785148e934fa04c651eda01dde3eb0c','Vaba',1,0,3,'13380000570','2017-08-04 10:15:23','2017-09-07 10:55:41',NULL),(12051,'12051','pbkdf2:sha256:50000$qWlOflYj$dd471d66f329f8a4e0ac94c28fbc004eef8e17adb58a657fe751ae3edfa0c7b7','Vaba',1,0,3,'13380000070','2017-08-04 10:15:26','2017-09-07 10:55:41',NULL),(12052,'12052','pbkdf2:sha256:50000$E3H2xJhF$52050dfca6b653811fc29bbab7627852069810bef160da0d33016be72aa8af33','Vaba',1,0,3,'13380000000','2017-08-04 10:15:28','2017-09-07 10:55:41',NULL),(12053,'12053','pbkdf2:sha256:50000$BXqPzN1c$c00f5b21a0b886cf15a46c05b05a31ef5d8ce01410da9bde1bf8365930211645','Vaba',1,0,3,'13380000001','2017-08-04 10:15:33','2017-09-07 10:55:41',NULL),(12054,'12054','pbkdf2:sha256:50000$uQwjBtuB$fdb743d568bd03f124d9e0363d742da1f28fb8bae358247efd0c03548fe3924c','Vaba',1,0,3,'13380002001','2017-08-04 10:15:40','2017-09-07 10:55:41',NULL),(12055,'12055','pbkdf2:sha256:50000$gJsdHNYh$778b1cef232e003f3dab9e3e0cf44de83905c177cd60d6aaf533369f986594eb','Vaba',1,0,3,'13380002201','2017-08-04 10:15:46','2017-09-07 10:55:41',NULL),(12056,'12056','pbkdf2:sha256:50000$73i1fODm$eef04b1fd29bffc7e616c2460de33dce24ac6cde528f807a96946a67675cd9ce','Vaba',1,0,3,'13381002201','2017-08-04 10:15:50','2017-09-07 10:55:41',NULL),(12057,'12057','pbkdf2:sha256:50000$NK42bCBF$8a4b00c13f2bf9c3b906338c6b611525e58c78d5b977b26f24d38b1dd28b3e3f','Vaba',1,0,3,'13381102201','2017-08-04 10:15:54','2017-09-07 10:55:41',NULL),(12058,'12058','pbkdf2:sha256:50000$xkchiA80$963354f11cb2a882735201e9a8703d94f60c336af2da07757b3494a404dadd1e','Vaba',1,0,3,'13381112201','2017-08-04 10:15:56','2017-09-07 10:55:41',NULL),(12059,'12059','pbkdf2:sha256:50000$Az2Y4D51$5f204a7f9fffe34493943b59b384bcc405bb9453270dbd151539ceadfbf622a6','Vaba',1,0,3,'13381111201','2017-08-04 10:15:59','2017-09-07 10:55:41',NULL),(12060,'12060','pbkdf2:sha256:50000$Wn4hfncg$7f5d59120e6c987d2515713a8c7c385ac710a20c0f7c0ddf590152c1b7592404','Vaba',1,0,3,'13381111101','2017-08-04 10:16:01','2017-09-07 10:55:41',NULL),(12061,'12061','pbkdf2:sha256:50000$GgywnEi5$62ec8d8a5a5dbdf3aac45f3de6e5d468e9e2d5add8cf035509aee37b9a5fe9a4','Vaba',1,0,3,'13381111111','2017-08-04 10:16:04','2017-09-07 10:55:41',NULL),(12062,'12062','pbkdf2:sha256:50000$f3yfDtrg$387dd2369e69cb24ed80b07c6ccb381902467c45a67ae33dc6d52b2622cd2120','Vaba',1,0,3,'13382111111','2017-08-04 10:16:07','2017-09-07 10:55:41',NULL),(12063,'12063','pbkdf2:sha256:50000$cToxdPLd$7330c1e5d6b370b8d8d477250c6588ae024c4cbcf76e8af9ae88b099ac5a5095','Vaba',1,0,3,'13382211111','2017-08-04 10:16:09','2017-09-07 10:55:41',NULL),(12064,'12064','pbkdf2:sha256:50000$Zb5MkDd5$afdca953f4b7ad3ee0a5840703a318ccdca1e11674576ac11d9d40e85f1cf0da','Vaba',1,0,3,'13382221111','2017-08-04 10:16:13','2017-09-07 10:55:41',NULL),(12065,'12065','pbkdf2:sha256:50000$dXkxClB5$84ff05a2646a0571c40d1c475fe2d54bb61866dcf5f122cbd4f093bcdf680824','黄丽的',1,0,3,'18825111149','2017-08-09 16:03:33','2017-09-07 10:55:41',NULL),(12066,'12066','pbkdf2:sha256:50000$D4iVRGSX$9e8ec231c29601efa0a4bcf446a3595eaf3ead06990ff26b9b8c1a275f022017','Psa',1,0,3,'18898986565','2017-08-10 16:03:28','2017-09-07 10:55:41',NULL),(12067,'12067','pbkdf2:sha256:50000$CZS5mIA0$c8e9683bbf193d7c1b88821b14b5fdea93adaf697293f48cb7fe7d9b4d0ed494','Piso',1,0,3,'13900908888','2017-08-10 16:04:12','2017-09-07 10:55:41',NULL),(12068,'12068','password-10','用户-10',0,0,3,'13612444210','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12069,'12069','password-11','用户-11',0,0,3,'13612444211','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12070,'12070','password-12','用户-12',0,0,3,'13612444212','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12071,'12071','password-13','用户-13',0,0,3,'13612444213','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12072,'12072','password-14','用户-14',0,0,3,'13612444214','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12073,'12073','password-15','用户-15',0,0,3,'13612444215','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12074,'12074','password-16','用户-16',0,0,3,'13612444216','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12075,'12075','password-17','用户-17',0,0,3,'13612444217','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12076,'12076','password-18','用户-18',0,0,3,'13612444218','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12077,'12077','password-19','用户-19',0,0,3,'13612444219','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12078,'12078','password-20','用户-20',0,0,3,'13612444220','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12079,'12079','password-21','用户-21',0,0,3,'13612444221','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12080,'12080','password-22','用户-22',0,0,3,'13612444222','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12081,'12081','password-23','用户-23',0,0,3,'13612444223','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12082,'12082','password-24','用户-24',0,0,3,'13612444224','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12083,'12083','password-25','用户-25',0,0,3,'13612444225','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12084,'12084','password-26','用户-26',0,0,3,'13612444226','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12085,'12085','password-27','用户-27',0,0,3,'13612444227','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12086,'12086','password-28','用户-28',0,0,3,'13612444228','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12088,'12088','password-30','用户-30',0,0,3,'13612444230','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12089,'12089','password-31','用户-31',0,0,3,'13612444231','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12090,'12090','password-32','用户-32',0,0,3,'13612444232','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12091,'12091','password-33','用户-33',0,0,3,'13612444233','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12092,'12092','password-34','用户-34',0,0,3,'13612444234','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12093,'12093','password-35','用户-35',0,0,3,'13612444235','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12094,'12094','password-36','用户-36',0,0,3,'13612444236','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12095,'12095','password-37','用户-37',0,0,3,'13612444237','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12096,'12096','password-38','用户-38',0,0,3,'13612444238','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12097,'12097','password-39','用户-39',0,0,3,'13612444239','2017-08-11 10:37:32','2017-09-07 10:55:41',NULL),(12098,'12098','pbkdf2:sha256:50000$wO3nOSQF$a7f10ac0a4795d50100c4914046eef64a84cddd889ffc14e0f23ad85c351b738','Imp1',1,0,3,'13800138656','2017-08-15 16:22:43','2017-09-07 10:55:41',NULL),(12099,'12099','pbkdf2:sha256:50000$TNbLWCNf$fe4014c51d20036bd577d336b761bafa00f0935d6f0c8e86d8da887663c7f18e','Imp2',1,0,3,'13200138656','2017-08-15 16:41:15','2017-09-07 10:55:41',NULL),(12100,'12100','pbkdf2:sha256:50000$iOzRTH5V$bcbf436454f320397dc5818a48c1f8d56cbbfca282cb47eae555c6cb92394574','Aaaa1',1,0,3,'13899892312','2017-08-15 16:49:39','2017-09-07 10:55:41',NULL),(12101,'12101','pbkdf2:sha256:50000$vUqDsQOi$545cebd15c2eecf7e68e9a5a7a91fd86160262d62ed72b5dd842de7549e4bd14','Aaab2',1,0,3,'13899892313','2017-08-15 16:49:39','2017-09-07 10:55:41',NULL),(12102,'12102','pbkdf2:sha256:50000$g3opHUqo$9ddc44408804408517ffd981c965d07cbc61525de1b8f9d236fab522dbb14427','Aaaa3',1,0,3,'13899892314','2017-08-15 16:49:39','2017-09-07 10:55:41',NULL),(12103,'12103','pbkdf2:sha256:50000$tIiBTYi1$103d6767299ae6873d15448e649fc110daa03f08d647aab243374fc6bb039d05','Aaab4',1,0,3,'13899892315','2017-08-15 16:49:40','2017-09-07 10:55:41',NULL),(12104,'12104','pbkdf2:sha256:50000$6AxszWmT$67318bfa492b782fb3296d100084b07bd3d7ec0608666c19b10dae5fa3a35666','Aaaa5',1,0,3,'13899892316','2017-08-15 16:49:40','2017-09-07 10:55:41',NULL),(12105,'12105','pbkdf2:sha256:50000$BBSFX2p7$39903c230298dc5f51c9706de78ddadd9cd1ccbeae781d90e2f6beabefa1e250','Aaaa2',1,0,3,'13899892317','2017-08-15 17:01:07','2017-09-07 10:55:41',NULL),(12106,'12106','pbkdf2:sha256:50000$DAhLv7Y5$4064a3ae9f324dabd61b4c7bb77ce45d7b84eb8fa0875ccc0876f411a90e296c','Aaab3',1,0,3,'13899892318','2017-08-15 17:01:07','2017-09-07 10:55:41',NULL),(12107,'12107','pbkdf2:sha256:50000$WENpORoJ$b12b4de715a92ec2c7eee0535e99c0b15d1589daea92d2b6eb753f81af58908e','Aaaa4',1,0,3,'13899892319','2017-08-15 17:01:08','2017-09-07 10:55:41',NULL),(12108,'12108','pbkdf2:sha256:50000$SD4JJQLL$80f6b462a41463d67da9f98454a00ecb7e22c2f240635129d739023f966139c2','Aaab5',1,0,3,'13899892320','2017-08-15 17:01:08','2017-09-07 10:55:41',NULL),(12109,'12109','pbkdf2:sha256:50000$gCDoqsUi$d0a6196b0025af617c40400e67302f63782783dc81e4e853138e0bda6eb25984','Aaaa6',1,0,3,'13899892321','2017-08-15 17:01:08','2017-09-07 10:55:41',NULL),(12110,'12110','pbkdf2:sha256:50000$4OaWiyNo$1bc8b145761875d053b3d787b4ed50d18c5b9918daae57c05cf8839f8eabcf21','Sala',1,0,3,'13788839992','2017-08-21 13:45:53','2017-09-07 10:55:41',NULL),(12111,'12111','pbkdf2:sha256:50000$zLoGbf0Y$15d6e358bb8f1b14bc3bf1e5f9a39dde5d29acf78b1bff03dba03df7343e1e78','Siel',1,0,3,'13822223333','2017-08-21 13:51:29','2017-09-07 10:55:41',NULL),(12112,'12112','pbkdf2:sha256:50000$rjbqEuDn$5d06be621e9fe39d8bae3831d42574eab5a593b4f862fc47218b2f21ffcd60d6','Sprlk',1,0,3,'13099988882','2017-08-21 13:52:30','2017-09-07 10:55:41',NULL),(12113,'12113','pbkdf2:sha256:50000$MwqzrmRl$8354b83cf5de4e8f33456b6e698c6d16fdd90ea49d99c0be151cfc6a3bcd1462','Uod',1,0,3,'13922232223','2017-08-21 14:58:01','2017-09-07 10:55:41',NULL),(12114,'12114','pbkdf2:sha256:50000$2VlM8muT$761918b69f73f89aac82bcba62af4487c70927fa25c90542aa5dc90f316ed2c6','阿拉善',0,0,3,'18824333321','2017-08-24 15:48:23','2017-09-07 10:55:41',NULL),(12115,'12115','pbkdf2:sha256:50000$I5NRibus$456a093dd6513ac95186e45a6769ab3a4c4c26a53e2f73d5c6fbf51c37537d7f','345',0,0,3,'13410238488','2017-08-25 10:02:31','2017-09-07 10:55:41',NULL),(12116,'12116','pbkdf2:sha256:50000$xb4WUCKK$aedf79901dfdf8ce44e1158bd3a53f800bd2949b4a840aeac7002a041d405071','828',0,0,3,'13410235555','2017-08-28 14:52:10','2017-09-07 10:55:41',NULL),(12117,'12117','pbkdf2:sha256:50000$Bk7qL0Kc$87513669595fa5fa0d2839111ba6edd6f59036d02889ba969877d4dc1607bacc','DJMC',0,0,3,'13410239969','2017-08-28 14:54:24','2017-09-07 10:55:41',NULL),(12118,'12118','pbkdf2:sha256:50000$l4IBIjla$36d999fb0649229558b9b99e8c3e020e6717a42bbef21c52e5a346f001b59514','456789',0,0,3,'13410236667','2017-08-28 14:58:21','2017-09-07 10:55:41',NULL),(12120,'12120','pbkdf2:sha256:50000$smQCfMRZ$aad1dfa8ccc0a19d6ed3cb904f7a7c3829eb152c6cf38cb335f108ec8f701680','李小姐',0,0,3,'18925153756','2017-09-01 10:32:40','2017-09-07 10:55:41',NULL),(12121,'12121','pbkdf2:sha256:50000$Tdri97qH$b6d44d6816d27f83186f313808eaa9c5bf9e26973b0fe0accde8d0af5cf2eea7','18925153757',0,0,3,'18925153757','2017-09-01 10:40:13','2017-09-07 10:55:41',NULL),(12122,'12122','pbkdf2:sha256:50000$QtHmqHTh$de8bc88e65f4f4d66998c029600b30f4d02f303922e40fc675d8c87caa9b25a5','18925153758',0,0,3,'18925153758','2017-09-01 15:24:38','2017-09-07 10:55:41',NULL),(12123,'12123','pbkdf2:sha256:50000$0YvMAoJw$85338d0127da7ce8736603af56f17fc45cc59e7fed1090496422451ce5dd812d','213',0,0,3,'13344443333','2017-09-01 15:33:38','2017-09-07 10:55:41',NULL),(12124,'12124','pbkdf2:sha256:50000$o046AMdi$924953d6fc8d5936d8850b44fbec656d8f58526fc3e8510a79f8bdb45be85776','18925151111',0,0,3,'18925151111','2017-09-04 11:10:59','2017-09-07 10:55:41',NULL),(12125,'12125','pbkdf2:sha256:50000$a9ikG6Uf$e144db825163dfc3c8ea857c47f64e33e60e1ee1950c10daf2642e9cfda12e22','18925152222',0,0,3,'18925152222','2017-09-04 11:19:40','2017-09-07 10:55:41',NULL),(12126,'12126','pbkdf2:sha256:50000$mTr4vRke$3443677d23fb4976508e4aefdf176460b9fafcadbe2aecf05d05383d17d1fb37','18925153333',0,0,3,'18925153333','2017-09-04 11:32:40','2017-09-07 10:55:41',NULL),(12127,'12127','pbkdf2:sha256:50000$In08MJZK$5c9589418a85f2ae29ad0870a954cbcebed07fb46e7c600af4dcb861f8b339ad','1',0,0,3,'13410239999','2017-09-04 15:45:19','2017-09-07 10:55:41',NULL),(12128,'12128','pbkdf2:sha256:50000$w3opKZ3o$26b01393ee8976bdc6a40b0fe0c608d20d4fd9a34162fa8c92199bf7ff2b0650','2',0,0,3,'13410239988','2017-09-04 15:46:56','2017-09-07 10:55:41',NULL),(12129,'12129','pbkdf2:sha256:50000$LfVJZoIx$877e2d9d12f8fbfdec8da9503d3426116deb1595d83f916495ef8ca9865b330b','8',0,0,3,'13410235566','2017-09-04 15:48:55','2017-09-07 10:55:41',NULL),(12130,'12130','pbkdf2:sha256:50000$EvJmTjUn$ed44c56e03dad60383dba00a6c5d5cf467efbc26a549bb4b9f8f180b89d68a0c','麻瓜',0,0,3,'13212444229','2017-09-04 16:19:03','2017-09-07 10:55:41',NULL),(12131,'12131','pbkdf2:sha256:50000$YoA8Sne8$8114a877e3bc7d8ae2294634c8a5df86992e5ee25e0c3a1e476e986acea7d02f','18925152233',0,0,3,'18925152233','2017-09-05 09:05:09','2017-09-07 10:55:41',NULL),(12132,'12132','pbkdf2:sha256:50000$X4NYfiwc$d604f27faa2812aeca47ebedeb944e0ecefbd3cf8c5bf06be727d9997074fbb1','95测试',0,0,3,'18925154444','2017-09-05 13:36:44','2017-09-07 10:55:41',NULL),(12133,'12133','pbkdf2:sha256:50000$X0bbBQmy$52fb1fb4e555ebbc029a396984ab29ed74909d50cd065fe6958f27e96ac5ef6f','95下午测试',0,0,3,'18925154466','2017-09-05 13:45:33','2017-09-07 10:55:41',NULL),(12134,'12134','pbkdf2:sha256:50000$9gB5Cs8r$9fe87d8556719021b8f4766eb06d4d44c1d5ee8440a1be8ec67834a4f1cb8df8','2200',0,0,3,'13510236666','2017-09-05 14:14:30','2017-09-07 10:55:41',NULL),(12135,'12135','pbkdf2:sha256:50000$ClDlZk6Y$6ab102590d7af1e4721ad6e85b0d4d2c80bfaabb27c9343159efad3395509fea','2201',0,0,3,'18725151111','2017-09-05 14:15:18','2017-09-07 10:55:41',NULL),(12136,'12136','pbkdf2:sha256:50000$wfVh18MH$11181e505994b591c32080ec21ce75d1e7a2221350cf57abf71d9d05cb9d2648','2202',0,0,3,'18725152222','2017-09-05 14:15:18','2017-09-07 10:55:41',NULL),(12137,'12137','pbkdf2:sha256:50000$u6WR32My$692471ee898fb76f108158cee964ee7e96b1f09590b86bbc95b58d88c0c07db5','96用户',0,0,3,'18925153755','2017-09-06 16:09:27','2017-09-07 10:55:41',NULL),(12141,'12141','pbkdf2:sha256:50000$zjfsn9QI$83c22a710c8af2b1cfd857d2ef1e8683efaa33714cc3abc49f01878657b652c9','大家阿里风景',0,0,3,'13212444228','2017-09-07 10:28:25','2017-09-07 10:28:25',NULL),(12146,'12146','pbkdf2:sha256:50000$quYlqDZU$54688207087a63557f9e6b4b1b1784283f1867025a0d62ad24e8ab9b6c06ca78','974',0,0,3,'13410238888','2017-09-07 10:36:32','2017-09-07 10:36:32',NULL),(12148,'12148','pbkdf2:sha256:50000$FdIi3j9Q$6a8fe0b61b5911a081369dcf2e67afda7505b8ee84a91756649cc0151b094a2a','怎么来的',0,0,3,'13410236666','2017-09-07 10:56:59','2017-09-07 10:56:59',NULL),(12149,'12149','pbkdf2:sha256:50000$muMS8rCx$7f7d86752c1bbd4e1111f8fdd5b1a1a01430e21ed90168353ff7e4bc849facf2','97973',0,0,3,'13410297973','2017-09-07 15:37:39','2017-09-07 15:38:21',NULL),(12150,'12150','pbkdf2:sha256:50000$4rDqa7V8$a012edce6ab8d5b8c20993dfda8eb86e5821e9a6085a46ba2832627fa25c6ffe','97972',0,0,3,'13410297972','2017-09-07 15:37:50','2017-09-07 15:37:50',NULL),(12151,'12151','pbkdf2:sha256:50000$NudbtEc3$80ba125747f80ff2c6e3c5b18ee00447150b1cb9f93e50bfa7bd37382e1e64b2','大名鼎鼎',0,0,3,'13899996666','2017-09-07 17:01:18','2017-09-07 17:01:18',NULL),(12152,'12152','pbkdf2:sha256:50000$uazJLMjF$6cea146bb9af2d6836296038d5edcecfcd9161f7f1f9db8d152f7eaca699b837','大法',0,0,3,'13888882222','2017-09-07 17:25:21','2017-09-07 17:25:21',NULL);
/*!40000 ALTER TABLE `bd_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_account_policy`
--

DROP TABLE IF EXISTS `bd_account_policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_account_policy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int(11) unsigned NOT NULL COMMENT '项目账号关联的平台用户',
  `mask` int(11) NOT NULL DEFAULT '0' COMMENT '项目账号标识,mask & (1 << 30) > 0账号被停用',
  `expired` datetime COMMENT '用户上网到期时间, NULL为无限期',
  `ends` int(11) unsigned DEFAULT '1' COMMENT '同时上网终端上限',
  `uplink` int(11) unsigned DEFAULT '0' COMMENT '账号上行带宽, 默认为0',
  `downlink` int(11) unsigned DEFAULT '0' COMMENT '账号下行带宽',
  `pn` varchar(32) NOT NULL COMMENT '所属项目id',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime  COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_account_user_pn` (`account_id`,`pn`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_account_policy`
--

LOCK TABLES `bd_account_policy` WRITE;
/*!40000 ALTER TABLE `bd_account_policy` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_account_policy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_account_profile`
--

DROP TABLE IF EXISTS `bd_account_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_account_profile` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL COMMENT '归属项目id',
  `account_id` int(11) NOT NULL COMMENT '关联的账号id',
  `name` varchar(64) DEFAULT NULL COMMENT '项目内用户姓名',
  `mobile` varchar(17) DEFAULT NULL COMMENT '用户手机',
  `dyncol` mediumblob COMMENT '动态列',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_profile_pn_mobile` (`pn`,`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12116 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_account_profile`
--

LOCK TABLES `bd_account_profile` WRITE;
/*!40000 ALTER TABLE `bd_account_profile` DISABLE KEYS */;
INSERT INTO `bd_account_profile` VALUES (12000,1,12000,'阿斯蒂芬','13322223333','\0C\0\0\0\0\0?\0	\0?\0\0#\0?\0?(\035\0noteemailtitlecompanyid_numberdepartmentid_back_imageid_front_image!教导处!!经理!siov1!!人事部!http://or7x902xd.bkt.clouddn.com/FmmoRJooQn6b4FM36zXps6_dpAvi!http://or7x902xd.bkt.clouddn.com/FmmoRJooQn6b4FM36zXps6_dpAvi','2017-07-28 15:18:20','2017-08-23 09:11:16'),(12001,1,12001,'老大哥','13399998888','\0\0\0\0\0\03\0\0\?\0notecompanydepartment!12!点对点!单独','2017-07-28 17:48:38','2017-08-01 11:10:59'),(12002,1,12004,'奥德赛','13233334444','\0\0\0\0\0\0#\0\0C\0notecompanydepartment!2!2!2','2017-07-31 10:19:18','2017-08-01 11:24:09'),(12003,1,12005,'张里','13333333333','\0\0\0\0\0\0#\0\0C\0notecompanydepartment!3!1!2dd','2017-07-31 10:20:18','2017-08-01 14:00:28'),(12005,12,12013,'Wong','13612444229',NULL,'2017-08-01 10:05:45','2017-08-01 10:05:45'),(12021,1,12027,'Duel','13722232223','\0#\0\0\0\0\0\0\0#\0\03\0notecompanydepartmentid_front_image!!!!1','2017-08-01 14:43:56','2017-08-01 14:43:56'),(12025,1,12031,'Peif','13888888888','\0C\0\0\0\0\0C\0	\0?\0\0\?\0\03\0s(\0?5\0noteemailtitlecompanyid_numberdepartmentid_back_imageid_front_image!ddd!wwww!engi!SIOV!ddd!develop!!','2017-08-04 10:13:26','2017-08-10 10:31:43'),(12026,1,12032,'Ysfe','13688875468','\0C\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0(\0c\05\0s\0noteemailtitlecompanyid_numberdepartmentid_back_imageid_front_image!!!!!!!!','2017-08-04 10:13:47','2017-08-31 15:04:54'),(12027,1,12033,'Ysfe','13688875123','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:13:53','2017-08-04 10:13:53'),(12028,1,12034,'Vrad','13688871234','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:20','2017-08-04 10:14:20'),(12029,1,12035,'Vab','13688871233','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:29','2017-08-04 10:14:29'),(12030,1,12036,'Vab','13683871233','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:36','2017-08-04 10:14:36'),(12031,1,12037,'Vaba','13383871233','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:44','2017-08-04 10:14:44'),(12032,1,12038,'Vaba','13383871238','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:48','2017-08-04 10:14:48'),(12033,1,12039,'Vaba','13383871638','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:51','2017-08-04 10:14:51'),(12035,1,12041,'Vaba','13385871678','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:55','2017-08-04 10:14:55'),(12036,1,12042,'Vaba','13385771678','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:14:58','2017-08-04 10:14:58'),(12037,1,12043,'Vaba','13385771878','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:01','2017-08-04 10:15:01'),(12038,1,12044,'Vaba','13389771878','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:04','2017-08-04 10:15:04'),(12039,1,12045,'Vaba','13389771578','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:06','2017-08-04 10:15:06'),(12042,1,12048,'Vaba','13380071570','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:19','2017-08-04 10:15:19'),(12043,1,12049,'Vaba','13380001570','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:21','2017-08-04 10:15:21'),(12044,1,12050,'Vaba','13380000570','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:23','2017-08-04 10:15:23'),(12045,1,12051,'Vaba','13380000070','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:26','2017-08-04 10:15:26'),(12046,1,12052,'Vaba','13380000000','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:28','2017-08-04 10:15:28'),(12047,1,12053,'Vaba','13380000001','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:33','2017-08-04 10:15:33'),(12048,1,12054,'Vaba','13380002001','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:40','2017-08-04 10:15:40'),(12049,1,12055,'Vaba','13380002201','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:46','2017-08-04 10:15:46'),(12050,1,12056,'Vaba','13381002201','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:50','2017-08-04 10:15:50'),(12051,1,12057,'Vaba','13381102201','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:54','2017-08-04 10:15:54'),(12052,1,12058,'Vaba','13381112201','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:56','2017-08-04 10:15:56'),(12053,1,12059,'Vaba','13381111201','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:15:59','2017-08-04 10:15:59'),(12054,1,12060,'Vaba','13381111101','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:16:02','2017-08-04 10:16:02'),(12055,1,12061,'Vaba','13381111111','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:16:04','2017-08-04 10:16:04'),(12056,1,12062,'Vaba','13382111111','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:16:07','2017-08-04 10:16:07'),(12057,1,12063,'Vaba','13382211111','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:16:09','2017-08-04 10:16:09'),(12058,1,12064,'Vaba','13382221111','\05\0\0\0\0\0\0\0#\0\Z\03\0\'\0C\0companyid_numberdepartmentid_back_imageid_front_image!!!!!','2017-08-04 10:16:13','2017-08-04 10:16:13'),(12059,1,12065,'黄丽的','18825111149','\0(\0\0\0\0\0c\0	\0\?\0\0S\0?\0?noteemailtitlecompanyid_numberdepartment!22222!xxx.xxx!扫地!SIOV!2222!研发','2017-08-09 16:03:33','2017-08-09 16:03:33'),(12060,1,12066,'Psa','18898986565','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-10 16:03:28','2017-08-10 16:03:28'),(12061,1,12067,'Piso','13900908888','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-10 16:04:12','2017-08-10 16:04:12'),(12062,1,12098,'Imp1','13800138656','\0(\0\0\0\0\0\0	\0?\0\0\?\0\0\0#noteemailtitlecompanyid_numberdepartment!!sa@sa.com!sa!sa!!sa','2017-08-15 16:22:43','2017-08-15 16:22:43'),(12063,1,12099,'Imp2','13200138656','\0(\0\0\0\0\0\0	\0?\0\0\?\0\0\0#noteemailtitlecompanyid_numberdepartment!!sa@sa.com!sa!sa!!sa','2017-08-15 16:41:15','2017-08-15 16:41:15'),(12064,1,12100,'Aaaa1','13899892312','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-15 16:49:39','2017-08-15 16:49:39'),(12065,1,12101,'Aaab2','13899892313','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-15 16:49:39','2017-08-15 16:49:39'),(12066,1,12102,'Aaaa3','13899892314','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-15 16:49:39','2017-08-15 16:49:39'),(12067,1,12103,'Aaab4','13899892315','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-15 16:49:40','2017-08-15 16:49:40'),(12068,1,12104,'Aaaa5','13899892316','\0(\0\0\0\0\03\0	\0c\0\0?\0\0\?\0\0?\0noteemailtitlecompanyid_numberdepartment!dd!dd!ddd!jjj!!ddd','2017-08-15 16:49:40','2017-08-25 15:06:45'),(12069,1,12105,'Aaaa2','13899892317','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-15 17:01:07','2017-08-15 17:01:07'),(12070,1,12106,'Aaab3','13899892318','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-08-15 17:01:07','2017-08-15 17:01:07'),(12074,1,12110,'Sala','13788839992','\0>\0\0\0\0\03\0	\0s\0\0?\0\0?\0#\030\0Cnotetitlecompanyid_numberdepartmentid_back_imageid_front_image!rr!333!111!444!222!!','2017-08-21 13:45:53','2017-08-21 13:45:53'),(12075,1,12111,'Siel','13822223333','\0>\0\0\0\0\03\0	\0s\0\0?\0\0?\0#\030\0Cnotetitlecompanyid_numberdepartmentid_back_imageid_front_image!66!444!222!555!333!!','2017-08-21 13:51:29','2017-08-21 13:51:29'),(12076,1,12112,'Sprlk','13099988882','\0>\0\0\0\0\03\0	\0c\0\0?\0\0\?\0#\0?\00\0\?notetitlecompanyid_numberdepartmentid_back_imageid_front_image!53!33!11!44!22!http://or7x902xd.bkt.clouddn.com/FtOT_4YU81AiawNmI9if1REf6wZY!http://or7x902xd.bkt.clouddn.com/Fh39AY11XIssnd1dURW_Uy5siKK5','2017-08-21 13:52:30','2017-08-21 14:39:56'),(12077,1,12113,'Uod','13922232223','\0>\0\0\0\0\0\0	\0#\0\03\0\0C\0#\0S\00\03notetitlecompanyid_numberdepartmentid_back_imageid_front_image!!!!!!http://or7x902xd.bkt.clouddn.com/Fh39AY11XIssnd1dURW_Uy5siKK5!http://or7x902xd.bkt.clouddn.com/FtOT_4YU81AiawNmI9if1REf6wZY','2017-08-21 14:58:01','2017-08-21 14:58:15'),(12078,1,12114,'阿拉善','18824333321','\0>\0\0\0\0\0s\0	\0\?\0\0S\0?#\030\0Cnoteemailcompanyid_numberdepartmentid_back_imageid_front_image!备注!d d d !么不!对对对!的!!','2017-08-24 15:48:23','2017-08-24 15:48:23'),(12080,1,12115,'123','13410238488',NULL,'2017-08-25 10:36:39','2017-08-25 10:36:39'),(12081,1,12116,'828','13410235555','\0\0\0\0\0\0\0	\0#\0\03\0\0C\0noteemailtitlecompanydepartment!!!!!','2017-08-28 14:52:10','2017-08-28 14:52:10'),(12084,1,12119,'李小姐','18925153756','\0\0\0\0\0\0\0	\0#\0\03\0\0C\0noteemailtitlecompanydepartment!!!!!','2017-09-01 10:26:16','2017-09-01 10:26:16'),(12085,1,12120,'李小姐','18925153756','\0\0\0\0\0\0\0	\0#\0\03\0\0C\0noteemailtitlecompanydepartment!!!!!','2017-09-01 10:32:40','2017-09-01 10:32:40'),(12086,1,12121,'18925153757','18925153757','\0\0\0\0\0\0\0	\0#\0\03\0\0C\0noteemailtitlecompanydepartment!!!!!','2017-09-01 10:40:13','2017-09-01 10:40:13'),(12087,1,12122,'18925153758','18925153758','\0\0\0\0\0\0\0companydepartment!!','2017-09-01 15:24:38','2017-09-01 15:24:38'),(12088,1674191091,12123,'213','13344443333',NULL,'2017-09-01 15:33:38','2017-09-01 15:33:38'),(12089,1674191091,12120,'李测试','18925153756',NULL,'2017-09-04 10:59:01','2017-09-04 10:59:01'),(12093,1132897105,12117,'DJMC','13410239969','\0(\0\0\0\0\0\?\0	\0C\0?\0\?\0?noteemailtitlecompanyid_numberdepartment!测试ddddd!163.com!only!siov!123dadjfajfk!DEV','2017-09-04 15:44:47','2017-09-06 17:41:24'),(12095,1132897105,12128,'2','13410239988','\0(\0\0\0\0\0#\0	\0C\0\0c\0\0?\0\0?\0noteemailtitlecompanyid_numberdepartment!3!3!2!1!3!1','2017-09-04 15:46:56','2017-09-04 15:46:56'),(12096,1132897105,12129,'8','13410235566','\0C\0\0\0\0\0#\0	\0C\0\0c\0\0?\0\0?\0(\0\?\05\0?noteemailtitlecompanyid_numberdepartmentid_back_imageid_front_image!8!8!8!8!88!8!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','2017-09-04 15:48:55','2017-09-04 15:48:55'),(12097,1146852709,12130,'麻瓜','13212444229','\0(\0\0\0\0\0s\0	\0#\0c\0?\0#noteemailtitlecompanyid_numberdepartment!么啊!xxx@xx.com!Eng!SIOV!123455!DEV','2017-09-04 16:19:03','2017-09-04 16:19:03'),(12098,1132897105,12131,'18925152233','18925152233','\0-\0\0\0\0\0\0	\03\0\0S\0\0c\0noteemailid_numberid_back_imageid_front_image!!1!1!!','2017-09-05 09:05:09','2017-09-05 09:05:09'),(12099,1535741440,12132,'95测试123','18925154444','\0C\0\0\0\0\0C\0	\0\?\0\0s\0\0S(\0?5\0\?noteemailtitlecompanyid_numberdepartmentid_back_imageid_front_image!123!邮箱123!12356666!公司123!123!部门123!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','2017-09-05 13:36:44','2017-09-05 16:43:16'),(12104,1535741440,12134,'2200','13510236666','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-09-05 14:23:04','2017-09-05 14:23:04'),(12105,1535741440,12135,'2201','18725151111','\0(\0\0\0\0\0\0	\0#\0\03\0\0C\0\0S\0noteemailtitlecompanyid_numberdepartment!!!!!!','2017-09-05 14:23:04','2017-09-05 14:23:04'),(12106,1535741440,12136,'李后果','18725156789','\0(\0\0\0\0\03\0	\0c\0\0?\0\0\03noteemailtitlecompanyid_numberdepartment!dd!dd!Test!SIOV!dd!DEV','2017-09-05 14:23:04','2017-09-05 16:46:37'),(12107,1410277206,12137,'96用户11','18925153744','\0C\0\0\0\0\03\0	\0c\0\0?\0\0\?\0\0?\0(\0#5\0noteemailtitlecompanyid_numberdepartmentid_back_imageid_front_image!55!33!66!11!44!22!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','2017-09-06 16:09:27','2017-09-06 16:13:32'),(12108,1146852709,12141,'大家阿里风景','13212444228',NULL,'2017-09-07 10:28:25','2017-09-07 10:28:25'),(12109,1410277206,12127,'97','13410239999','\01\0\0\0\0\0#\0\0C\0\0c\0#\0s\0titlecompanydepartmentid_back_imageid_front_image!3!1!2!!','2017-09-07 10:35:54','2017-09-07 10:35:54'),(12110,1410277206,12146,'974','13410238888','\01\0\0\0\0\0#\0\0C\0\0c\0#\0Ctitlecompanydepartmentid_back_imageid_front_image!3!1!2!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI!http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','2017-09-07 10:36:32','2017-09-07 10:36:32'),(12111,1146852709,12148,'怎么来的','13410236666',NULL,'2017-09-07 10:56:59','2017-09-07 10:56:59'),(12112,1101310510,12149,'97973','13410297973','\0\0\0\0\0company!1','2017-09-07 15:37:39','2017-09-07 15:38:21'),(12113,1101310510,12150,'97972','13410297972','\0\0\0\0\0company!','2017-09-07 15:37:50','2017-09-07 15:37:50'),(12114,1122327156,12151,'大名鼎鼎','13899996666',NULL,'2017-09-07 17:01:18','2017-09-07 17:01:18'),(12115,1122327156,12152,'大法','13888882222',NULL,'2017-09-07 17:25:21','2017-09-07 17:25:21');
/*!40000 ALTER TABLE `bd_account_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_account_tag`
--

DROP TABLE IF EXISTS `bd_account_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_account_tag` (
  `account_id` int(11) NOT NULL COMMENT '账号id',
  `tag_id` int(11) NOT NULL COMMENT '标签id',
  PRIMARY KEY (`account_id`,`tag_id`),
  KEY `fk_actag_tag_id` (`tag_id`),
  CONSTRAINT `fk_actag_account_id` FOREIGN KEY (`account_id`) REFERENCES `bd_account` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_actag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `bd_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_account_tag`
--

LOCK TABLES `bd_account_tag` WRITE;
/*!40000 ALTER TABLE `bd_account_tag` DISABLE KEYS */;
INSERT INTO `bd_account_tag` VALUES (12000,10),(12001,1),(12001,32),(12001,46),(12001,48),(12001,56),(12001,81),(12002,32),(12002,46),(12002,48),(12002,56),(12002,81),(12003,32),(12003,46),(12003,48),(12003,56),(12003,81),(12004,12),(12004,32),(12004,46),(12004,48),(12004,56),(12004,81),(12005,1),(12005,32),(12005,46),(12005,48),(12005,56),(12005,81),(12006,32),(12006,46),(12006,48),(12006,56),(12006,81),(12007,1),(12007,10),(12007,12),(12007,32),(12007,46),(12007,48),(12007,56),(12007,81),(12008,10),(12008,15),(12008,32),(12008,46),(12008,48),(12008,56),(12008,81),(12009,32),(12009,46),(12009,48),(12009,56),(12009,81),(12010,32),(12010,46),(12010,48),(12010,56),(12010,81),(12011,32),(12011,46),(12011,48),(12011,56),(12011,81),(12012,32),(12012,46),(12012,48),(12012,56),(12012,81),(12013,1),(12013,10),(12013,32),(12013,46),(12013,48),(12013,56),(12013,81),(12014,1),(12014,32),(12014,46),(12014,48),(12014,56),(12014,81),(12015,1),(12015,10),(12015,32),(12015,46),(12015,48),(12015,56),(12015,81),(12016,10),(12016,32),(12016,46),(12016,48),(12016,56),(12016,81),(12017,12),(12017,32),(12017,46),(12017,48),(12017,56),(12017,81),(12018,1),(12018,32),(12018,46),(12018,48),(12018,56),(12018,81),(12019,12),(12019,32),(12019,46),(12019,48),(12019,56),(12019,81),(12020,1),(12020,10),(12020,32),(12020,46),(12020,48),(12020,56),(12020,81),(12021,1),(12021,32),(12021,46),(12021,48),(12021,56),(12021,81),(12022,32),(12022,46),(12022,48),(12022,56),(12022,81),(12023,32),(12023,46),(12023,48),(12023,56),(12023,81),(12024,32),(12024,46),(12024,48),(12024,56),(12024,81),(12025,12),(12025,32),(12025,46),(12025,48),(12025,56),(12025,81),(12026,1),(12026,32),(12026,46),(12026,48),(12026,56),(12026,81),(12027,1),(12027,32),(12027,46),(12027,48),(12027,56),(12027,81),(12028,1),(12028,10),(12028,12),(12028,15),(12028,17),(12028,32),(12028,46),(12028,48),(12028,56),(12028,81),(12029,32),(12029,46),(12029,48),(12029,56),(12029,81),(12030,32),(12030,46),(12030,48),(12030,56),(12030,81),(12031,15),(12031,32),(12031,46),(12031,48),(12031,56),(12031,81),(12032,1),(12032,10),(12032,17),(12032,32),(12032,46),(12032,48),(12032,56),(12032,81),(12033,17),(12033,32),(12033,46),(12033,48),(12033,56),(12033,81),(12034,12),(12034,15),(12034,32),(12034,46),(12034,48),(12034,56),(12034,81),(12035,12),(12035,15),(12035,32),(12035,46),(12035,48),(12035,56),(12035,81),(12036,12),(12036,15),(12036,32),(12036,46),(12036,48),(12036,56),(12036,81),(12037,12),(12037,15),(12037,32),(12037,46),(12037,48),(12037,56),(12037,81),(12038,12),(12038,15),(12038,32),(12038,46),(12038,48),(12038,56),(12038,81),(12039,12),(12039,15),(12039,32),(12039,46),(12039,48),(12039,56),(12039,81),(12040,12),(12040,15),(12040,32),(12040,46),(12040,48),(12040,56),(12040,81),(12041,12),(12041,15),(12041,32),(12041,46),(12041,48),(12041,56),(12041,81),(12042,12),(12042,15),(12042,32),(12042,46),(12042,48),(12042,56),(12042,81),(12043,12),(12043,15),(12043,32),(12043,46),(12043,48),(12043,56),(12043,81),(12044,12),(12044,15),(12044,32),(12044,46),(12044,48),(12044,56),(12044,81),(12045,12),(12045,15),(12045,32),(12045,46),(12045,48),(12045,56),(12045,81),(12046,12),(12046,15),(12046,32),(12046,46),(12046,48),(12046,56),(12046,81),(12047,12),(12047,15),(12047,32),(12047,46),(12047,48),(12047,56),(12047,81),(12048,12),(12048,15),(12048,32),(12048,46),(12048,48),(12048,56),(12048,81),(12049,12),(12049,15),(12049,32),(12049,46),(12049,48),(12049,56),(12049,81),(12050,12),(12050,15),(12050,32),(12050,46),(12050,48),(12050,56),(12050,81),(12051,12),(12051,15),(12051,32),(12051,46),(12051,48),(12051,56),(12051,81),(12052,12),(12052,15),(12052,32),(12052,46),(12052,48),(12052,56),(12052,81),(12053,12),(12053,15),(12053,32),(12053,46),(12053,48),(12053,56),(12053,81),(12054,10),(12054,12),(12054,32),(12054,46),(12054,48),(12054,56),(12054,81),(12055,1),(12055,10),(12055,32),(12055,46),(12055,48),(12055,56),(12055,81),(12056,1),(12056,10),(12056,32),(12056,46),(12056,48),(12056,56),(12056,81),(12057,1),(12057,10),(12057,32),(12057,46),(12057,48),(12057,56),(12057,81),(12058,1),(12058,10),(12058,32),(12058,46),(12058,48),(12058,56),(12058,81),(12059,1),(12059,10),(12059,32),(12059,46),(12059,48),(12059,56),(12059,81),(12060,1),(12060,10),(12060,32),(12060,46),(12060,48),(12060,56),(12060,81),(12061,1),(12061,10),(12061,32),(12061,46),(12061,48),(12061,56),(12061,81),(12062,1),(12062,10),(12062,32),(12062,46),(12062,48),(12062,56),(12062,81),(12063,1),(12063,10),(12063,32),(12063,46),(12063,48),(12063,56),(12063,81),(12064,1),(12064,10),(12064,32),(12064,46),(12064,48),(12064,56),(12064,81),(12065,32),(12065,46),(12065,48),(12065,56),(12065,81),(12066,32),(12066,46),(12066,48),(12066,56),(12066,81),(12067,32),(12067,46),(12067,48),(12067,56),(12067,81),(12068,32),(12068,46),(12068,48),(12068,56),(12068,81),(12069,32),(12069,46),(12069,48),(12069,56),(12069,81),(12070,32),(12070,46),(12070,48),(12070,56),(12070,81),(12071,32),(12071,46),(12071,48),(12071,56),(12071,81),(12072,32),(12072,46),(12072,48),(12072,56),(12072,81),(12073,32),(12073,46),(12073,48),(12073,56),(12073,81),(12074,32),(12074,46),(12074,48),(12074,56),(12074,81),(12075,32),(12075,46),(12075,48),(12075,56),(12075,81),(12076,32),(12076,46),(12076,48),(12076,56),(12076,81),(12077,32),(12077,46),(12077,48),(12077,56),(12077,81),(12078,32),(12078,46),(12078,48),(12078,56),(12078,81),(12079,32),(12079,46),(12079,48),(12079,56),(12079,81),(12080,32),(12080,46),(12080,48),(12080,56),(12080,81),(12081,32),(12081,46),(12081,48),(12081,56),(12081,81),(12082,32),(12082,46),(12082,48),(12082,56),(12082,81),(12083,32),(12083,46),(12083,48),(12083,56),(12083,81),(12084,32),(12084,46),(12084,48),(12084,56),(12084,81),(12085,32),(12085,46),(12085,48),(12085,56),(12085,81),(12086,32),(12086,46),(12086,48),(12086,56),(12086,81),(12088,32),(12088,46),(12088,48),(12088,56),(12088,81),(12089,32),(12089,46),(12089,48),(12089,56),(12089,81),(12090,32),(12090,46),(12090,48),(12090,56),(12090,81),(12091,32),(12091,46),(12091,48),(12091,56),(12091,81),(12092,32),(12092,46),(12092,48),(12092,56),(12092,81),(12093,32),(12093,46),(12093,48),(12093,56),(12093,81),(12094,32),(12094,46),(12094,48),(12094,56),(12094,81),(12095,32),(12095,46),(12095,48),(12095,56),(12095,81),(12096,32),(12096,46),(12096,48),(12096,56),(12096,81),(12097,32),(12097,46),(12097,48),(12097,56),(12097,81),(12098,32),(12098,46),(12098,48),(12098,56),(12098,81),(12099,32),(12099,46),(12099,48),(12099,56),(12099,81),(12110,1),(12110,10),(12111,1),(12111,10),(12112,1),(12112,10),(12114,1),(12114,10),(12114,12),(12115,1),(12115,48),(12117,92),(12117,93),(12117,94),(12124,81),(12125,81),(12126,32),(12126,46),(12126,48),(12126,56),(12126,81),(12129,84),(12132,81),(12132,91),(12133,81),(12134,48);
/*!40000 ALTER TABLE `bd_account_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_ap`
--

DROP TABLE IF EXISTS `bd_ap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_ap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(32) NOT NULL COMMENT 'AP mac地址',
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT 'AP归属的项目ID',
  `vendor` varchar(16) DEFAULT NULL COMMENT '品牌',
  `name` varchar(128) DEFAULT NULL COMMENT 'AP名',
  `ip` varchar(16) DEFAULT NULL COMMENT 'AP ip地址',
  `address` varchar(64) DEFAULT NULL COMMENT 'AP地址',
  `ac_ip` varchar(16) DEFAULT NULL COMMENT 'AC ip地址',
  `is_online` tinyint(3) unsigned DEFAULT '0' COMMENT '是否在线，0 - 否，1 - 是',
  `mpoi_id` int(11) DEFAULT NULL COMMENT '地址位置信息字段',
  `connections` int(11) DEFAULT '0' COMMENT '在线人数',
  `model` varchar(32) DEFAULT NULL COMMENT 'ap型号',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime  COMMENT '修改时间',
  `is_sens` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0-关闭感知/1-开启感知',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ap_mac` (`mac`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_ap`
--

LOCK TABLES `bd_ap` WRITE;
/*!40000 ALTER TABLE `bd_ap` DISABLE KEYS */;
INSERT INTO `bd_ap` VALUES (5,'0A:1B:2C:3D:4E:5F',1,'ruijie','55',NULL,'21',NULL,0,NULL,0,NULL,'2017-08-23 16:14:14','2017-08-23 16:14:14',0),(6,'1A:1B:2C:3D:4E:5F',1,'ruijie','e',NULL,'21',NULL,0,NULL,0,NULL,'2017-08-23 16:25:44','2017-08-23 16:25:44',0),(7,'2A:1B:2C:3D:4E:5F',1,'ruijie','22',NULL,'21',NULL,0,NULL,0,NULL,'2017-08-23 16:25:51','2017-08-23 16:25:51',0),(8,'3A:1B:2C:3D:4E:5F',1,'ruijie','333',NULL,'21',NULL,0,NULL,0,NULL,'2017-08-23 16:25:55','2017-08-23 16:25:55',0),(9,'4A:1B:2C:3D:4E:5F',1,'ruijie','4444',NULL,'21',NULL,0,NULL,0,NULL,'2017-08-23 16:26:00','2017-08-23 16:26:00',0),(10,'5A:1B:2C:3D:4E:5F',1,'ruijie','4444',NULL,'2123',NULL,0,NULL,0,NULL,'2017-08-23 16:26:12','2017-08-23 16:26:12',0),(11,'AA:1B:2C:3D:4E:5F',1,'huawei','1',NULL,'2',NULL,0,NULL,0,NULL,'2017-08-23 16:28:08','2017-08-23 16:28:08',0),(12,'D4:68:BA:02:93:96',1,'xinrui','test824',NULL,'1232',NULL,0,NULL,0,NULL,'2017-08-24 17:48:00','2017-08-24 17:48:00',0),(13,'D4:68:BA:02:93:97',1,'ruijie','南沙',NULL,'123',NULL,0,NULL,0,NULL,'2017-08-28 14:37:03','2017-08-28 14:37:03',0),(14,'D4:68:BA:02:93:98',1,'ruijie','南沙1',NULL,'123',NULL,0,NULL,0,NULL,'2017-08-28 14:38:21','2017-08-28 14:38:21',0),(15,'0A:1B:2C:3D:4E:55',1146852709,'ruijie','1',NULL,'1',NULL,0,NULL,0,NULL,'2017-09-01 17:37:08','2017-09-01 17:37:08',0),(16,'D4:68:BA:02:93:81',1132897105,'xinrui','123',NULL,'123',NULL,0,NULL,0,NULL,'2017-09-04 15:19:30','2017-09-04 15:19:30',0),(17,'0A:1B:2C:3D:4E:3F',1674191091,'hanming','2',NULL,'2',NULL,0,NULL,0,NULL,'2017-09-04 16:07:28','2017-09-04 16:07:28',0),(18,'0A:1B:2C:3D:4E:CC',1146852709,'h3c','啊发放',NULL,'提阿虎恶气',NULL,0,NULL,0,NULL,'2017-09-04 16:57:30','2017-09-04 16:57:30',0),(19,'D4:68:BA:02:93:86',1535741440,'huawei','95ap',NULL,'南沙资讯园区',NULL,1,NULL,2,NULL,'2017-09-05 09:12:19','2017-09-06 13:39:08',0),(20,'BB:1B:2C:3D:4E:5F',1132897105,'ruijie','a',NULL,'a',NULL,0,NULL,0,NULL,'2017-09-05 10:28:19','2017-09-05 10:28:19',0),(21,'5F:1B:2C:3D:4E:5F',1132897105,'xinrui','b',NULL,'3',NULL,0,NULL,0,NULL,'2017-09-05 10:28:38','2017-09-05 10:28:38',0),(22,'D4:68:BA:02:93:16',1535741440,'ruijie','1',NULL,'12',NULL,0,NULL,0,NULL,'2017-09-05 14:59:32','2017-09-05 14:59:32',0),(23,'D4:68:BA:02:93:11',1535741440,'huawei','11',NULL,'11',NULL,0,NULL,0,NULL,'2017-09-06 13:41:02','2017-09-06 13:41:02',0);
/*!40000 ALTER TABLE `bd_ap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_ap_tag`
--

DROP TABLE IF EXISTS `bd_ap_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_ap_tag` (
  `ap_id` int(11) NOT NULL COMMENT 'AP id',
  `tag_id` int(11) NOT NULL COMMENT '标签id',
  PRIMARY KEY (`ap_id`,`tag_id`),
  KEY `fk_aptag_tag_id` (`tag_id`),
  CONSTRAINT `fk_aptag_ap_id` FOREIGN KEY (`ap_id`) REFERENCES `bd_ap` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_aptag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `bd_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_ap_tag`
--

LOCK TABLES `bd_ap_tag` WRITE;
/*!40000 ALTER TABLE `bd_ap_tag` DISABLE KEYS */;
INSERT INTO `bd_ap_tag` VALUES (5,49),(6,49),(7,49),(8,49),(9,49),(10,49),(11,49),(12,49),(12,50),(13,50),(14,49),(14,50),(15,79),(16,82),(18,87),(18,88),(19,90),(23,90);
/*!40000 ALTER TABLE `bd_ap_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_api_token`
--

DROP TABLE IF EXISTS `bd_api_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_api_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `secret_key` varchar(64) NOT NULL COMMENT 'secret_key',
  `access_token` varchar(128) NOT NULL COMMENT 'access_token',
  `note` varchar(128) NOT NULL COMMENT '备注',
  `mask` int(11) unsigned NOT NULL DEFAULT '0' COMMENT 'token标志位, mask & 1 > 0禁用',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_portal_pn_name` (`secret_key`,`access_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_api_token`
--

LOCK TABLES `bd_api_token` WRITE;
/*!40000 ALTER TABLE `bd_api_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_api_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_coupon_code`
--

DROP TABLE IF EXISTS `bd_coupon_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_coupon_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL COMMENT '兑换码',
  `hours` smallint(6) NOT NULL COMMENT '兑换码时长',
  `expired` datetime NOT NULL COMMENT '兑换码过期时间',
  `is_used` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否已被使用',
  `serial_id` int(11) NOT NULL COMMENT '序列号id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_code_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_coupon_code`
--

LOCK TABLES `bd_coupon_code` WRITE;
/*!40000 ALTER TABLE `bd_coupon_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_coupon_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_coupon_serial`
--

DROP TABLE IF EXISTS `bd_coupon_serial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_coupon_serial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_by` int(11) NOT NULL COMMENT '生成兑换码管理员ID',
  `serial` int(11) NOT NULL COMMENT '兑换码序列号',
  `created_at` datetime  COMMENT '生成时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_coupon_serial`
--

LOCK TABLES `bd_coupon_serial` WRITE;
/*!40000 ALTER TABLE `bd_coupon_serial` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_coupon_serial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_coupon_used_record`
--

DROP TABLE IF EXISTS `bd_coupon_used_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_coupon_used_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL COMMENT '兑换码',
  `account_id` int(11) NOT NULL COMMENT '兑换用户id',
  `hours` smallint(6) NOT NULL COMMENT '兑换时长',
  `created_at` datetime COMMENT '兑换时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_record_user_code` (`account_id`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_coupon_used_record`
--

LOCK TABLES `bd_coupon_used_record` WRITE;
/*!40000 ALTER TABLE `bd_coupon_used_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_coupon_used_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_dyncol`
--

DROP TABLE IF EXISTS `bd_dyncol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_dyncol` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `col` varchar(32) NOT NULL COMMENT '字段名',
  `label` varchar(32) NOT NULL COMMENT '属性名',
  `created_at` datetime  COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dyncol_col_label` (`col`,`label`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_dyncol`
--

LOCK TABLES `bd_dyncol` WRITE;
/*!40000 ALTER TABLE `bd_dyncol` DISABLE KEYS */;
INSERT INTO `bd_dyncol` VALUES (1,'company','公司','2017-07-27 13:11:57'),(2,'department','部门','2017-07-27 13:11:57'),(3,'title','职位','2017-07-27 13:11:57'),(4,'email','邮箱','2017-07-27 13:11:57'),(5,'id_number','身份证号','2017-07-27 13:11:57'),(6,'id_front_image','身份证照片（正面）','2017-07-27 13:11:57'),(7,'id_back_image','身份证照片（反面）','2017-07-27 13:11:57'),(8,'note','备注','2017-07-27 13:11:57');
/*!40000 ALTER TABLE `bd_dyncol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_letter`
--

DROP TABLE IF EXISTS `bd_letter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_letter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '通知内容',
  `status` smallint(5) unsigned NOT NULL COMMENT '状态标示, 0 - 草稿, 1 - 发布, 2 - 删除',
  `created_by` int(11) NOT NULL COMMENT '创建平台管理员id',
  `created_at` datetime COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_letter`
--

LOCK TABLES `bd_letter` WRITE;
/*!40000 ALTER TABLE `bd_letter` DISABLE KEYS */;
INSERT INTO `bd_letter` VALUES (70,'string','string',0,1525483113,'2017-09-01 14:40:59'),(71,'string','string',0,1525483113,'2017-09-01 14:41:49'),(72,'string','string',0,1525483113,'2017-09-01 14:42:51'),(73,'string','string',2,1525483113,'2017-09-01 14:45:08'),(74,'94测试','94测试',1,1525483113,'2017-09-04 14:28:19'),(75,'94草稿','94草稿',1,1525483113,'2017-09-04 14:33:52'),(76,'95','95',1,1525483113,'2017-09-05 09:38:12'),(77,'9595','9595',1,1525483113,'2017-09-05 09:38:40'),(78,'5','5',0,1525483113,'2017-09-05 10:26:34'),(79,'55','55',0,1525483113,'2017-09-05 10:26:39'),(80,'5','5',1,1525483113,'2017-09-05 10:26:46'),(81,'5','5',1,1525483113,'2017-09-05 10:26:51'),(82,'站内信9598','站内信9598',2,1525483113,'2017-09-05 10:39:08'),(83,'958958','958958',1,1525483113,'2017-09-05 10:41:45');
/*!40000 ALTER TABLE `bd_letter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_mac_history`
--

DROP TABLE IF EXISTS `bd_mac_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_mac_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '关联的bd_account.user字段',
  `mac` char(17) NOT NULL DEFAULT '' COMMENT '用户设备mac地址',
  `tlogin` datetime COMMENT '上网终端绑定时间',
  `platform` varchar(256) NOT NULL DEFAULT '' COMMENT '上网设备，User-Agent判断',
  `expired` datetime  COMMENT '自动认证过期时间',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT 'AC ssid',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_mac_ssid` (`user`,`mac`,`ssid`),
  KEY `idx_mac_history_mac` (`mac`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_mac_history`
--

LOCK TABLES `bd_mac_history` WRITE;
/*!40000 ALTER TABLE `bd_mac_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_mac_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_mailbox`
--

DROP TABLE IF EXISTS `bd_mailbox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_mailbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receiver_id` int(11) DEFAULT NULL COMMENT '管理员id',
  `letter_id` int(11) DEFAULT NULL COMMENT '站内信id',
  `title` varchar(256) DEFAULT NULL COMMENT '标题',
  `content` text COMMENT '通知内容',
  `is_broadcast` smallint(5) unsigned NOT NULL DEFAULT '1' COMMENT '是否广播信息, 0 - 不是, 1 - 是',
  `status` smallint(5) unsigned NOT NULL COMMENT '状态标示, 0 - 未读, 1 - 已读, 2 - 删除',
  `created_at` datetime COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_mailbox`
--

LOCK TABLES `bd_mailbox` WRITE;
/*!40000 ALTER TABLE `bd_mailbox` DISABLE KEYS */;
INSERT INTO `bd_mailbox` VALUES (138,1087029815,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(139,1411410731,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(140,1450895554,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(141,1517121291,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(142,1545224857,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(143,1608581031,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(144,1609968344,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(145,1710487325,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(146,1954999235,74,NULL,NULL,1,0,'2017-09-04 14:28:19'),(147,2147483647,74,NULL,NULL,1,1,'2017-09-04 14:28:19'),(148,1087029815,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(149,1411410731,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(150,1450895554,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(151,1517121291,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(152,1545224857,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(153,1608581031,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(154,1609968344,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(155,1710487325,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(156,1954999235,75,NULL,NULL,1,0,'2017-09-04 14:33:58'),(157,2147483647,75,NULL,NULL,1,1,'2017-09-04 14:33:58'),(158,1087029815,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(159,1100350806,76,NULL,NULL,1,2,'2017-09-05 09:38:12'),(160,1411410731,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(161,1450895554,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(162,1517121291,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(163,1545224857,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(164,1608581031,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(165,1609968344,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(166,1710487325,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(167,1954999235,76,NULL,NULL,1,0,'2017-09-05 09:38:12'),(168,2147483647,76,NULL,NULL,1,1,'2017-09-05 09:38:12'),(169,1087029815,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(170,1100350806,77,NULL,NULL,1,2,'2017-09-05 09:38:40'),(171,1411410731,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(172,1450895554,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(173,1517121291,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(174,1545224857,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(175,1608581031,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(176,1609968344,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(177,1710487325,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(178,1954999235,77,NULL,NULL,1,0,'2017-09-05 09:38:40'),(179,2147483647,77,NULL,NULL,1,1,'2017-09-05 09:38:40'),(180,1087029815,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(181,1100350806,80,NULL,NULL,1,1,'2017-09-05 10:26:46'),(182,1411410731,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(183,1450895554,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(184,1517121291,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(185,1545224857,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(186,1608581031,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(187,1609968344,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(188,1710487325,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(189,1954999235,80,NULL,NULL,1,0,'2017-09-05 10:26:46'),(190,2147483647,80,NULL,NULL,1,1,'2017-09-05 10:26:46'),(191,1087029815,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(192,1100350806,81,NULL,NULL,1,1,'2017-09-05 10:26:51'),(193,1411410731,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(194,1450895554,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(195,1517121291,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(196,1545224857,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(197,1608581031,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(198,1609968344,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(199,1710487325,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(200,1954999235,81,NULL,NULL,1,0,'2017-09-05 10:26:51'),(201,2147483647,81,NULL,NULL,1,1,'2017-09-05 10:26:51'),(202,1087029815,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(203,1100350806,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(204,1411410731,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(205,1450895554,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(206,1517121291,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(207,1545224857,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(208,1608581031,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(209,1609968344,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(210,1710487325,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(211,1954999235,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(212,2147483647,82,NULL,NULL,1,2,'2017-09-05 10:39:48'),(213,1087029815,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(214,1100350806,83,NULL,NULL,1,1,'2017-09-05 10:41:56'),(215,1411410731,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(216,1450895554,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(217,1517121291,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(218,1545224857,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(219,1608581031,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(220,1609968344,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(221,1710487325,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(222,1954999235,83,NULL,NULL,1,0,'2017-09-05 10:41:56'),(223,2147483647,83,NULL,NULL,1,2,'2017-09-05 10:41:56');
/*!40000 ALTER TABLE `bd_mailbox` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_network_config`
--

DROP TABLE IF EXISTS `bd_network_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_network_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT '网络项目编号',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT '无线ssid',
  `portal_id` int(11) NOT NULL DEFAULT '0' COMMENT '认证portal配置ID, 0为默认模版',
  `is_public` smallint(6) NOT NULL DEFAULT '1' COMMENT '是否为私有网络, 0为公有',
  `is_free` smallint(6) NOT NULL DEFAULT '1' COMMENT '计费方式, 0 - 收费, 1 - 免费',
  `mask` int(11) NOT NULL COMMENT '认证方式, 前三位表示, 0 - 手机号, 1 - 微信, 2 - APP, 如 mask=7则全部支持',
  `wechat_account_id` int(11) DEFAULT NULL COMMENT '微信认证上网公众账号, 仅当 mask & 2 > 0时使用',
  `duration` int(11) NOT NULL DEFAULT '30' COMMENT '自动认证间隔时间，默认为30天',
  `session_timeout` int(11) NOT NULL DEFAULT '24' COMMENT '一次认证，授权时间（小时)',
  `created_at` datetime  COMMENT '兑换时间',
  `updated_at` datetime  COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pn_network_config_pn_ssid` (`pn`,`ssid`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_network_config`
--

LOCK TABLES `bd_network_config` WRITE;
/*!40000 ALTER TABLE `bd_network_config` DISABLE KEYS */;
INSERT INTO `bd_network_config` VALUES (2,1,'6547',1,0,0,5,NULL,4,5,'2017-08-22 13:41:30','2017-08-22 13:41:30'),(3,1,'45634',9,0,0,5,NULL,2,240,'2017-08-22 13:51:57','2017-09-05 10:03:15'),(4,1,'77777',8,1,1,6,4,2,3,'2017-08-22 14:23:48','2017-08-25 15:10:31'),(5,1,'6666665',1,0,1,6,5,6,720,'2017-08-22 14:25:21','2017-08-22 14:29:13'),(6,1,'11',1,1,1,7,7,240,6,'2017-08-23 10:03:03','2017-08-23 10:03:03'),(7,1,'123',1,1,1,1,NULL,24,6,'2017-08-24 17:41:39','2017-08-24 17:41:39'),(8,1,'1234',12,1,1,7,5,72,7,'2017-08-25 09:47:59','2017-08-25 10:17:10'),(9,1,'BD_TEST',1,0,0,7,7,720,7,'2017-08-25 09:54:44','2017-08-25 09:54:44'),(10,1,'123456',15,0,0,3,4,7,7,'2017-08-25 10:28:45','2017-08-28 14:05:52'),(13,1,'12345645',20,0,0,7,10,7,7,'2017-09-01 11:03:06','2017-09-01 11:03:06'),(14,1131221010,'22',9,0,0,7,12,2,96,'2017-09-01 17:20:11','2017-09-05 10:03:15'),(15,1253910457,'3',9,0,1,4,NULL,3,5,'2017-09-04 11:21:41','2017-09-05 10:03:15'),(16,1132897105,'123',9,0,0,1,NULL,7,7,'2017-09-04 14:52:54','2017-09-05 10:03:15'),(17,1132897105,'2',9,0,0,1,NULL,3,4,'2017-09-04 15:03:10','2017-09-05 10:03:15'),(18,1132897105,'1234567890',28,1,1,7,14,240,240,'2017-09-04 17:10:16','2017-09-04 17:16:32'),(19,1535741440,'123456',30,0,0,7,17,7,18,'2017-09-06 10:05:03','2017-09-06 10:05:03'),(20,1410277206,'789456',31,1,1,7,18,7,720,'2017-09-06 10:39:26','2017-09-06 10:39:26'),(22,1535741440,'2',30,0,1,7,17,3,5,'2017-09-06 13:32:05','2017-09-06 13:32:05'),(23,1535741440,'3',9,1,1,1,NULL,7,96,'2017-09-06 13:32:27','2017-09-06 13:32:27'),(24,1535741440,'4',30,0,1,4,NULL,7,18,'2017-09-06 13:32:49','2017-09-06 13:32:49'),(25,1122327156,'有毒勿连',9,0,0,1,NULL,720,3,'2017-09-07 14:08:48','2017-09-07 14:08:48');
/*!40000 ALTER TABLE `bd_network_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_online`
--

DROP TABLE IF EXISTS `bd_online`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL DEFAULT '' COMMENT '用户上网账号, 关联bd_account.user',
  `nas_addr` varchar(32) NOT NULL DEFAULT '' COMMENT 'AC或认证网关ip地址',
  `acct_session_id` varchar(64) NOT NULL DEFAULT '' COMMENT '会话id, radius查找在线设备依据',
  `acct_start_time` datetime COMMENT '上网起始时间',
  `framed_ipaddr` varchar(32) NOT NULL DEFAULT '' COMMENT '终端获得的ip地址',
  `mac_addr` varchar(24) NOT NULL DEFAULT '' COMMENT '终端的mac地址',
  `billing_times` int(11) NOT NULL DEFAULT '0' COMMENT '计费时长',
  `input_total` int(11) NOT NULL DEFAULT '0' COMMENT '下行数据量',
  `output_total` int(11) NOT NULL DEFAULT '0' COMMENT '上行数据量',
  `start_source` smallint(6) NOT NULL DEFAULT '0' COMMENT '状态',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT '联网AP ssid',
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT '在线设备所在项目, 0为平台',
  `ap_mac` varchar(24) NOT NULL DEFAULT '' COMMENT 'ap mac地址',
  `is_auto` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否通过无感知上线，1: 是，0: 否',
  `auth_type` smallint(6) NOT NULL DEFAULT '0' COMMENT '认证方式，默认为账号密码, 1 -手机号, 2 - 微信, 4 - APP',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_online_mac_addr` (`mac_addr`),
  UNIQUE KEY `uk_online_nas_session_id` (`nas_addr`,`acct_session_id`),
  KEY `idx_online_user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_online`
--

LOCK TABLES `bd_online` WRITE;
/*!40000 ALTER TABLE `bd_online` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_online` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_package`
--

DROP TABLE IF EXISTS `bd_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT '' COMMENT '套餐名称',
  `price` decimal(8,2) DEFAULT NULL COMMENT '套餐价格',
  `time` float DEFAULT NULL COMMENT '可用上网时长（小时）',
  `ends` smallint(6) DEFAULT NULL COMMENT '同时上网终端数',
  `expired` datetime DEFAULT NULL COMMENT '上网过期时间',
  `available_until` datetime DEFAULT NULL COMMENT '套餐过期时间',
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT '套餐所属项目，0为平台套餐',
  `mask` int(11) NOT NULL COMMENT 'mask & 1 == 1 按小时收费;mask & 1 = 0 按天收费',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否删除, 0 - 否, 1 - 是',
  `apply_projects` varchar(256) NOT NULL DEFAULT '[]' COMMENT '投放项目id列表，空为全部项目',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_package_pn` (`name`,`pn`,`is_deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_package`
--

LOCK TABLES `bd_package` WRITE;
/*!40000 ALTER TABLE `bd_package` DISABLE KEYS */;
INSERT INTO `bd_package` VALUES (1,'单身套餐',3.00,NULL,3,'2017-08-09 00:00:00','2017-08-20 00:00:00',1,0,1,'[]','2017-08-08 14:34:13','2017-08-08 16:25:57'),(2,'情侣套餐',8.00,192,8,NULL,'2017-08-26 00:00:00',1,0,1,'[]','2017-08-08 16:13:13','2017-08-08 16:26:01'),(3,'快餐',1.00,NULL,1,'2017-08-09 00:00:00','2018-08-04 00:00:00',1,0,1,'[]','2017-08-08 16:26:29','2017-08-10 13:45:34'),(4,'特餐',1.00,NULL,1,'2017-08-09 00:00:00','2017-08-02 00:00:00',1,0,1,'[]','2017-08-08 16:26:42','2017-08-10 13:45:37'),(5,'常餐',1.00,NULL,1,'2017-08-09 00:00:00','2017-08-02 00:00:00',1,0,1,'[]','2017-08-08 16:26:50','2017-08-10 13:45:45'),(6,'晚餐',1.00,NULL,1,'2017-08-09 00:00:00','2017-08-02 00:00:00',1,0,1,'[]','2017-08-08 16:27:03','2017-08-10 13:45:49'),(7,'午餐',1.00,216,1,NULL,'2017-08-02 00:00:00',1,0,1,'[]','2017-08-08 16:27:25','2017-08-10 13:45:52'),(8,'萨达',1.00,2133330000,1,NULL,'2017-08-02 00:00:00',1,0,1,'[]','2017-08-08 16:28:05','2017-08-08 16:33:55'),(9,'萨达u',1.00,2133330000000,1,NULL,'2017-08-02 00:00:00',1,0,1,'[]','2017-08-08 16:28:19','2017-08-08 16:28:28'),(10,'31',234435.35,1080,1,NULL,'2017-08-08 00:00:00',1,0,1,'[]','2017-08-08 16:34:15','2017-08-09 09:45:20'),(11,'3134',234435.35,1080,1,NULL,'2017-08-08 00:00:00',1,0,1,'[]','2017-08-08 16:34:30','2017-08-09 09:45:22'),(12,'adsf',11.00,11,2,NULL,'2017-08-18 00:00:00',0,1,1,'[1]','2017-08-08 17:19:00','2017-08-10 13:46:22'),(13,'fgwea',33.00,33,4,NULL,'2017-08-24 00:00:00',0,1,1,'[2]','2017-08-08 17:20:41','2017-08-08 17:37:44'),(14,'  ',30.00,552,2,NULL,'2017-08-31 00:00:00',1,0,1,'[]','2017-08-10 11:24:05','2017-08-10 11:24:18'),(17,'月套餐',30.00,720,3,NULL,'2017-08-26 00:00:00',1,0,0,'[]','2017-08-10 15:52:39','2017-08-10 15:52:39'),(18,'优惠套餐',40.00,1440,3,NULL,'2019-09-30 00:00:00',1,0,0,'[]','2017-08-10 15:55:38','2017-08-10 15:55:38'),(19,'套餐',30.00,720,4,NULL,'2017-08-31 00:00:00',0,0,0,'[]','2017-08-10 16:02:00','2017-08-28 15:17:36'),(20,'套餐1',30.00,30,NULL,NULL,'1970-01-01 00:00:00',1,0,0,'[]','2017-08-11 10:37:32','2017-08-11 10:53:08'),(21,'套餐2',45.00,40,NULL,NULL,NULL,2,0,0,'[]','2017-08-11 10:37:32','2017-08-11 10:37:32'),(22,'套餐3',60.00,70,NULL,NULL,NULL,3,0,0,'[]','2017-08-11 10:37:32','2017-08-11 10:37:32'),(23,'套餐4',30.00,30,NULL,NULL,NULL,1,0,0,'[]','2017-08-11 10:37:32','2017-08-11 10:37:32'),(24,'套餐5',45.00,40,NULL,NULL,NULL,2,0,0,'[]','2017-08-11 10:37:32','2017-08-11 10:37:32'),(25,'套餐6',60.00,70,NULL,NULL,NULL,3,0,0,'[]','2017-08-11 10:37:32','2017-08-11 10:37:32'),(26,'123',123.00,24,1,NULL,'2017-08-16 00:00:00',0,0,0,'[1]','2017-08-16 11:27:20','2017-08-16 11:27:20'),(27,'2',3.00,72,1,NULL,'2017-08-16 00:00:00',1,0,0,'[]','2017-08-16 13:07:26','2017-08-16 13:07:26'),(28,'1',1.00,24,1,NULL,'2017-08-16 00:00:00',1,0,0,'[]','2017-08-16 13:12:42','2017-08-16 13:12:42'),(29,'大优惠',15.00,720,3,NULL,'2017-09-30 00:00:00',0,0,0,'[1, 2]','2017-08-24 15:56:02','2017-08-24 15:56:02'),(30,'456',1.00,288,1,NULL,'2017-08-24 00:00:00',0,0,0,'[]','2017-08-24 17:27:09','2017-08-24 17:27:09'),(31,'1234',4.00,96,1,NULL,'2017-08-24 00:00:00',0,0,0,'[]','2017-08-24 17:39:36','2017-08-24 17:39:36'),(32,'825测试',1.00,1,6,NULL,'2017-08-25 00:00:00',0,1,0,'[]','2017-08-25 09:10:18','2017-08-25 09:10:18'),(33,'825测试1',1.00,24,9,NULL,'2017-08-31 00:00:00',0,0,0,'[]','2017-08-25 09:12:56','2017-08-25 09:12:56'),(34,'825825',1000.00,NULL,1,'2017-09-08 00:00:00','2017-08-25 00:00:00',1,0,0,'[]','2017-08-25 10:08:01','2017-08-25 10:08:01'),(35,'828',1.00,1,4,NULL,'2017-08-31 00:00:00',0,1,1,'[]','2017-08-28 11:34:17','2017-08-28 13:23:51'),(38,'8281',1.00,1,4,NULL,'2017-08-30 00:00:00',0,1,1,'[]','2017-08-28 13:25:22','2017-08-29 15:31:17'),(39,'828828',1.00,24,1,NULL,'2017-09-09 00:00:00',0,0,1,'[]','2017-08-28 13:30:21','2017-08-30 11:10:59'),(40,'828',0.10,NULL,1,'2017-09-09 00:00:00','2017-08-28 00:00:00',1,0,0,'[]','2017-08-28 15:20:56','2017-08-28 15:20:56'),(41,'usr r ',1111.00,3216,1,NULL,'2017-08-31 00:00:00',0,0,1,'[]','2017-08-30 11:08:38','2017-08-30 11:10:56'),(42,'eeeeeeee',12.00,12,1,NULL,'2017-08-31 00:00:00',0,1,0,'[1253910457, 1316118103]','2017-08-31 17:38:43','2017-09-01 16:11:49'),(43,'201791套餐',100.00,48,1,NULL,'2017-09-01 00:00:00',0,0,1,'[]','2017-09-01 10:52:47','2017-09-01 10:53:36'),(44,'91',100.00,NULL,4,'2017-09-30 00:00:00','2017-09-30 00:00:00',1,0,0,'[]','2017-09-01 11:07:09','2017-09-01 11:07:09'),(45,'3',324.00,768,1,NULL,'2017-09-20 00:00:00',1253910457,0,0,'[]','2017-09-04 10:56:38','2017-09-04 10:56:38'),(46,'94测试',3.00,3,5,NULL,'2017-09-30 00:00:00',0,1,0,'[1132897105]','2017-09-04 13:58:13','2017-09-04 13:58:13'),(47,'94',1.00,1,1,NULL,'2017-09-04 00:00:00',0,1,0,'[1132897105]','2017-09-04 14:05:08','2017-09-04 14:05:08'),(48,'941',1.00,24,1,NULL,'2017-09-04 00:00:00',0,0,0,'[1132897105]','2017-09-04 14:05:25','2017-09-04 14:05:25'),(49,'9411',1.00,1,1,NULL,'2017-09-04 00:00:00',0,1,1,'[1132897105, 1253910457, 1146852709, 1316118103]','2017-09-04 14:05:34','2017-09-04 14:07:26'),(53,'89',1.00,24,1,NULL,'2017-09-04 00:00:00',0,0,1,'[1132897105]','2017-09-04 14:09:49','2017-09-04 14:20:41'),(56,'平台的套餐-0',37.00,45,3,NULL,'1970-01-01 00:00:00',0,0,0,'[1132897105]','2017-09-04 15:29:34','2017-09-05 09:26:07'),(57,'平台的套餐-1',47.00,45,3,NULL,'2017-09-05 00:00:00',0,0,0,'[]','2017-09-04 15:29:34','2017-09-05 09:25:54'),(58,'20170904测试的套餐-0',63.00,30,3,NULL,NULL,1132897105,0,0,'[]','2017-09-04 15:29:34','2017-09-04 15:29:34'),(59,'20170904测试的套餐-1',52.00,30,3,NULL,NULL,1132897105,0,0,'[]','2017-09-04 15:29:34','2017-09-04 15:29:34'),(60,'我想象我们的相遇的套餐-0',71.00,30,3,NULL,NULL,1131221010,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(61,'我想象我们的相遇的套餐-1',67.00,30,3,NULL,NULL,1131221010,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(62,'北京市云江科技有限公司的套餐-0',49.00,60,3,NULL,NULL,1674191091,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(63,'北京市云江科技有限公司的套餐-1',30.00,30,3,NULL,NULL,1674191091,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(64,'一九二七年，帕斯捷尔纳克致茨维塔耶娃的套餐-0',60.00,45,3,NULL,NULL,1146852709,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(65,'一九二七年，帕斯捷尔纳克致茨维塔耶娃的套餐-1',51.00,30,3,NULL,NULL,1146852709,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(66,'20170902测试的套餐-0',40.00,45,3,NULL,NULL,1316118103,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(67,'20170902测试的套餐-1',30.00,60,3,NULL,NULL,1316118103,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(68,'一九二七年的春夜的套餐-0',71.00,30,3,NULL,NULL,1253910457,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(69,'一九二七年的春夜的套餐-1',35.00,30,3,NULL,NULL,1253910457,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(70,'20170901下午的套餐-0',40.00,45,3,NULL,NULL,1342451022,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(71,'20170901下午的套餐-1',37.00,45,3,NULL,NULL,1342451022,0,0,'[]','2017-09-04 15:29:35','2017-09-04 15:29:35'),(72,'sad',1.00,24,1,NULL,'2017-09-04 00:00:00',1132897105,0,0,'[]','2017-09-04 16:18:41','2017-09-04 16:18:41'),(73,'213',2.00,NULL,2,'2017-09-15 00:00:00','2017-09-04 00:00:00',1132897105,0,0,'[]','2017-09-04 16:19:05','2017-09-04 16:19:05'),(74,'23',2.00,48,2,NULL,'2017-09-17 00:00:00',1132897105,0,0,'[]','2017-09-04 16:19:14','2017-09-04 16:19:14'),(75,'3',3.00,72,2,NULL,'2017-09-22 00:00:00',0,0,0,'[1253910457]','2017-09-05 09:25:12','2017-09-05 09:25:12'),(76,'a3',3.00,72,1,NULL,'2017-09-05 00:00:00',0,0,0,'[]','2017-09-05 09:30:53','2017-09-05 09:30:53'),(77,'9441',11.00,12,1,NULL,'2017-09-05 00:00:00',0,1,1,'[1132897105, 1253910457, 1316118103]','2017-09-05 10:40:55','2017-09-05 10:41:03'),(79,'201795小时',51.00,50,52,NULL,'2017-11-30 00:00:00',0,1,0,'[1535741440, 1132897105]','2017-09-05 10:56:54','2017-09-05 11:18:25'),(80,'20170905天数',4.00,72,5,NULL,'2017-09-30 00:00:00',0,0,0,'[1535741440]','2017-09-05 11:19:27','2017-09-05 11:19:27'),(81,'9411',11.00,11,2,NULL,'2017-09-30 00:00:00',0,1,1,'[1132897105, 1253910457]','2017-09-05 11:26:02','2017-09-06 16:23:34'),(82,'20170905项目套餐',4.00,72,5,NULL,'2017-09-30 00:00:00',1535741440,0,0,'[]','2017-09-05 11:28:58','2017-09-05 11:28:58'),(83,'指定日期',5.00,NULL,6,'2017-09-30 00:00:00','2019-09-30 00:00:00',1535741440,0,0,'[]','2017-09-05 11:29:28','2017-09-05 11:31:18'),(84,'201796',123.00,18936,1001,NULL,'2017-09-30 00:00:00',1410277206,0,1,'[]','2017-09-06 10:42:53','2017-09-06 16:23:11'),(85,'201796',1.00,24,2,NULL,'2017-09-06 00:00:00',1410277206,0,0,'[]','2017-09-06 16:23:20','2017-09-06 16:23:20'),(86,'9411',1.00,24,2,NULL,'2017-09-06 00:00:00',0,0,0,'[1535741440]','2017-09-06 16:23:45','2017-09-06 16:23:45'),(87,'全球通',800.00,2400,3,NULL,'2037-12-31 00:00:00',1122327156,0,0,'[]','2017-09-07 14:03:37','2017-09-07 14:03:37');
/*!40000 ALTER TABLE `bd_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_package_order`
--

DROP TABLE IF EXISTS `bd_package_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_package_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `package_id` int(11) NOT NULL COMMENT '套餐id',
  `account_id` int(11) NOT NULL COMMENT '用户账号id',
  `amount` decimal(8,2) NOT NULL COMMENT '金额',
  `pay_with` varchar(32) NOT NULL COMMENT '支付方式, alipay or wechat',
  `pay_from` varchar(32) NOT NULL COMMENT '支付入口, APP or wechat',
  `created_at` datetime COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `fk_pack_order_account_id` (`account_id`),
  KEY `fk_pack_order_package_id` (`package_id`),
  CONSTRAINT `fk_pack_order_account_id` FOREIGN KEY (`account_id`) REFERENCES `bd_account` (`id`),
  CONSTRAINT `fk_pack_order_package_id` FOREIGN KEY (`package_id`) REFERENCES `bd_package` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=489 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_package_order`
--

LOCK TABLES `bd_package_order` WRITE;
/*!40000 ALTER TABLE `bd_package_order` DISABLE KEYS */;
INSERT INTO `bd_package_order` VALUES (181,56,12029,37.00,'微信支付','微信','2017-09-05 15:29:33'),(182,57,12029,47.00,'微信支付','APP','2017-09-04 15:29:33'),(183,56,12112,37.00,'微信支付','APP','2017-09-04 15:29:33'),(184,57,12112,47.00,'微信支付','微信','2017-09-04 15:29:33'),(185,56,12021,37.00,'支付宝','微信','2017-09-04 15:29:33'),(186,57,12021,47.00,'微信支付','APP','2017-09-04 15:29:33'),(187,56,12099,37.00,'微信支付','微信','2017-09-04 15:29:33'),(188,57,12099,47.00,'微信支付','APP','2017-09-04 15:29:33'),(189,56,12014,37.00,'支付宝','微信','2017-09-04 15:29:33'),(190,57,12014,47.00,'支付宝','微信','2017-09-04 15:29:33'),(191,56,12006,37.00,'支付宝','微信','2017-09-04 15:29:33'),(192,57,12006,47.00,'支付宝','APP','2017-09-04 15:29:33'),(193,56,12016,37.00,'支付宝','微信','2017-09-04 15:29:33'),(194,57,12016,47.00,'微信支付','微信','2017-09-04 15:29:33'),(195,56,12019,37.00,'支付宝','APP','2017-09-04 15:29:33'),(196,57,12019,47.00,'支付宝','APP','2017-09-04 15:29:33'),(197,56,12004,37.00,'支付宝','微信','2017-09-04 15:29:33'),(198,57,12004,47.00,'支付宝','微信','2017-09-04 15:29:33'),(199,56,12007,37.00,'微信支付','APP','2017-09-04 15:29:33'),(200,57,12007,47.00,'微信支付','微信','2017-09-04 15:29:33'),(201,56,12003,37.00,'支付宝','微信','2017-09-04 15:29:33'),(202,57,12003,47.00,'支付宝','微信','2017-09-04 15:29:33'),(203,56,12025,37.00,'支付宝','APP','2017-09-04 15:29:33'),(204,57,12025,47.00,'微信支付','APP','2017-09-04 15:29:33'),(205,56,12012,37.00,'支付宝','微信','2017-09-04 15:29:33'),(206,57,12012,47.00,'微信支付','微信','2017-09-04 15:29:33'),(207,56,12008,37.00,'微信支付','微信','2017-09-04 15:29:33'),(208,57,12008,47.00,'微信支付','APP','2017-09-04 15:29:33'),(209,56,12000,37.00,'微信支付','微信','2017-09-04 15:29:33'),(210,57,12000,47.00,'支付宝','APP','2017-09-04 15:29:33'),(211,56,12005,37.00,'微信支付','微信','2017-09-04 15:29:33'),(212,57,12005,47.00,'微信支付','微信','2017-09-04 15:29:33'),(213,56,12123,37.00,'微信支付','微信','2017-09-04 15:29:33'),(214,57,12123,47.00,'微信支付','APP','2017-09-04 15:29:33'),(215,56,12052,37.00,'支付宝','微信','2017-09-04 15:29:33'),(216,57,12052,47.00,'支付宝','APP','2017-09-04 15:29:33'),(217,56,12053,37.00,'微信支付','APP','2017-09-04 15:29:33'),(218,57,12053,47.00,'微信支付','APP','2017-09-04 15:29:33'),(219,56,12051,37.00,'支付宝','微信','2017-09-04 15:29:33'),(220,57,12051,47.00,'支付宝','APP','2017-09-04 15:29:33'),(221,56,12029,37.00,'支付宝','微信','2017-09-03 15:29:33'),(222,57,12029,47.00,'微信支付','APP','2017-09-03 15:29:33'),(223,56,12112,37.00,'支付宝','微信','2017-09-03 15:29:33'),(224,57,12112,47.00,'微信支付','APP','2017-09-03 15:29:33'),(225,56,12021,37.00,'微信支付','微信','2017-09-03 15:29:33'),(226,57,12021,47.00,'支付宝','微信','2017-09-03 15:29:33'),(227,56,12099,37.00,'支付宝','APP','2017-09-03 15:29:33'),(228,57,12099,47.00,'支付宝','微信','2017-09-03 15:29:33'),(229,56,12014,37.00,'微信支付','APP','2017-09-03 15:29:33'),(230,57,12014,47.00,'支付宝','微信','2017-09-03 15:29:33'),(231,56,12006,37.00,'微信支付','APP','2017-09-03 15:29:33'),(232,57,12006,47.00,'支付宝','APP','2017-09-03 15:29:33'),(233,56,12016,37.00,'支付宝','APP','2017-09-03 15:29:33'),(234,57,12016,47.00,'支付宝','微信','2017-09-03 15:29:33'),(235,56,12019,37.00,'支付宝','APP','2017-09-03 15:29:33'),(236,57,12019,47.00,'支付宝','微信','2017-09-03 15:29:33'),(237,56,12004,37.00,'支付宝','APP','2017-09-03 15:29:33'),(238,57,12004,47.00,'支付宝','APP','2017-09-03 15:29:33'),(239,56,12007,37.00,'微信支付','微信','2017-09-03 15:29:33'),(240,57,12007,47.00,'微信支付','APP','2017-09-03 15:29:33'),(241,56,12003,37.00,'微信支付','APP','2017-09-03 15:29:33'),(242,57,12003,47.00,'支付宝','APP','2017-09-03 15:29:33'),(243,56,12025,37.00,'支付宝','APP','2017-09-03 15:29:33'),(244,57,12025,47.00,'微信支付','APP','2017-09-03 15:29:33'),(245,56,12012,37.00,'支付宝','APP','2017-09-03 15:29:33'),(246,57,12012,47.00,'微信支付','微信','2017-09-03 15:29:33'),(247,56,12008,37.00,'微信支付','微信','2017-09-03 15:29:33'),(248,57,12008,47.00,'微信支付','APP','2017-09-03 15:29:33'),(249,56,12000,37.00,'微信支付','微信','2017-09-03 15:29:33'),(250,57,12000,47.00,'支付宝','APP','2017-09-03 15:29:33'),(251,56,12005,37.00,'支付宝','APP','2017-09-03 15:29:33'),(252,57,12005,47.00,'支付宝','APP','2017-09-03 15:29:33'),(253,56,12123,37.00,'支付宝','APP','2017-09-03 15:29:33'),(254,57,12123,47.00,'支付宝','APP','2017-09-03 15:29:33'),(255,56,12052,37.00,'支付宝','微信','2017-09-03 15:29:33'),(256,57,12052,47.00,'支付宝','微信','2017-09-03 15:29:33'),(257,56,12053,37.00,'微信支付','微信','2017-09-03 15:29:33'),(258,57,12053,47.00,'微信支付','APP','2017-09-03 15:29:33'),(259,56,12029,37.00,'微信支付','APP','2017-09-02 15:29:33'),(260,57,12029,47.00,'支付宝','微信','2017-09-02 15:29:33'),(261,56,12112,37.00,'微信支付','APP','2017-09-02 15:29:33'),(262,57,12112,47.00,'微信支付','APP','2017-09-02 15:29:33'),(263,56,12021,37.00,'微信支付','APP','2017-09-02 15:29:33'),(264,57,12021,47.00,'微信支付','APP','2017-09-02 15:29:33'),(265,56,12099,37.00,'微信支付','微信','2017-09-02 15:29:33'),(266,57,12099,47.00,'微信支付','微信','2017-09-02 15:29:33'),(267,56,12014,37.00,'支付宝','微信','2017-09-02 15:29:33'),(268,57,12014,47.00,'微信支付','APP','2017-09-02 15:29:33'),(269,56,12006,37.00,'微信支付','APP','2017-09-02 15:29:33'),(270,57,12006,47.00,'支付宝','微信','2017-09-02 15:29:33'),(271,56,12016,37.00,'支付宝','微信','2017-09-02 15:29:33'),(272,57,12016,47.00,'支付宝','微信','2017-09-02 15:29:33'),(273,56,12019,37.00,'微信支付','APP','2017-09-02 15:29:33'),(274,57,12019,47.00,'支付宝','微信','2017-09-02 15:29:33'),(275,56,12004,37.00,'微信支付','APP','2017-09-02 15:29:33'),(276,57,12004,47.00,'支付宝','APP','2017-09-02 15:29:33'),(277,56,12007,37.00,'微信支付','微信','2017-09-02 15:29:33'),(278,57,12007,47.00,'微信支付','APP','2017-09-02 15:29:33'),(279,56,12003,37.00,'微信支付','APP','2017-09-02 15:29:33'),(280,57,12003,47.00,'支付宝','微信','2017-09-02 15:29:33'),(281,56,12025,37.00,'支付宝','微信','2017-09-02 15:29:33'),(282,57,12025,47.00,'支付宝','APP','2017-09-02 15:29:33'),(283,56,12012,37.00,'支付宝','微信','2017-09-02 15:29:33'),(284,57,12012,47.00,'支付宝','APP','2017-09-02 15:29:33'),(285,56,12008,37.00,'支付宝','微信','2017-09-02 15:29:33'),(286,57,12008,47.00,'微信支付','APP','2017-09-02 15:29:33'),(287,56,12000,37.00,'支付宝','APP','2017-09-02 15:29:33'),(288,57,12000,47.00,'微信支付','APP','2017-09-02 15:29:33'),(289,56,12005,37.00,'支付宝','APP','2017-09-02 15:29:33'),(290,57,12005,47.00,'支付宝','微信','2017-09-02 15:29:33'),(291,56,12123,37.00,'支付宝','微信','2017-09-02 15:29:33'),(292,57,12123,47.00,'微信支付','微信','2017-09-02 15:29:33'),(293,56,12052,37.00,'微信支付','微信','2017-09-02 15:29:33'),(294,57,12052,47.00,'微信支付','微信','2017-09-02 15:29:33'),(295,56,12029,37.00,'支付宝','APP','2017-09-01 15:29:33'),(296,57,12029,47.00,'支付宝','APP','2017-09-01 15:29:33'),(297,56,12112,37.00,'微信支付','微信','2017-09-01 15:29:33'),(298,57,12112,47.00,'微信支付','APP','2017-09-01 15:29:33'),(299,56,12021,37.00,'微信支付','APP','2017-09-01 15:29:33'),(300,57,12021,47.00,'支付宝','微信','2017-09-01 15:29:33'),(301,56,12099,37.00,'支付宝','APP','2017-09-01 15:29:33'),(302,57,12099,47.00,'支付宝','APP','2017-09-01 15:29:33'),(303,56,12014,37.00,'微信支付','APP','2017-09-01 15:29:33'),(304,57,12014,47.00,'微信支付','APP','2017-09-01 15:29:33'),(305,56,12006,37.00,'微信支付','微信','2017-09-01 15:29:33'),(306,57,12006,47.00,'支付宝','APP','2017-09-01 15:29:33'),(307,56,12016,37.00,'支付宝','微信','2017-09-01 15:29:33'),(308,57,12016,47.00,'支付宝','APP','2017-09-01 15:29:33'),(309,56,12019,37.00,'支付宝','APP','2017-09-01 15:29:33'),(310,57,12019,47.00,'微信支付','微信','2017-09-01 15:29:33'),(311,56,12004,37.00,'支付宝','微信','2017-09-01 15:29:33'),(312,57,12004,47.00,'微信支付','微信','2017-09-01 15:29:33'),(313,56,12007,37.00,'支付宝','APP','2017-09-01 15:29:33'),(314,57,12007,47.00,'支付宝','APP','2017-09-01 15:29:33'),(315,56,12003,37.00,'支付宝','APP','2017-09-01 15:29:33'),(316,57,12003,47.00,'支付宝','微信','2017-09-01 15:29:33'),(317,56,12025,37.00,'微信支付','APP','2017-09-01 15:29:33'),(318,57,12025,47.00,'微信支付','APP','2017-09-01 15:29:33'),(319,56,12012,37.00,'微信支付','微信','2017-09-01 15:29:33'),(320,57,12012,47.00,'微信支付','微信','2017-09-01 15:29:33'),(321,56,12008,37.00,'微信支付','微信','2017-09-01 15:29:33'),(322,57,12008,47.00,'支付宝','APP','2017-09-01 15:29:33'),(323,56,12000,37.00,'微信支付','微信','2017-09-01 15:29:33'),(324,57,12000,47.00,'支付宝','APP','2017-09-01 15:29:33'),(325,56,12005,37.00,'支付宝','APP','2017-09-01 15:29:33'),(326,57,12005,47.00,'支付宝','APP','2017-09-01 15:29:33'),(327,56,12123,37.00,'支付宝','微信','2017-09-01 15:29:33'),(328,57,12123,47.00,'微信支付','微信','2017-09-01 15:29:33'),(329,56,12029,37.00,'支付宝','微信','2017-08-31 15:29:33'),(330,57,12029,47.00,'支付宝','微信','2017-08-31 15:29:33'),(331,56,12112,37.00,'支付宝','微信','2017-08-31 15:29:33'),(332,57,12112,47.00,'支付宝','微信','2017-08-31 15:29:33'),(333,56,12021,37.00,'支付宝','APP','2017-08-31 15:29:33'),(334,57,12021,47.00,'微信支付','微信','2017-08-31 15:29:33'),(335,56,12099,37.00,'支付宝','APP','2017-08-31 15:29:33'),(336,57,12099,47.00,'微信支付','微信','2017-08-31 15:29:33'),(337,56,12014,37.00,'微信支付','APP','2017-08-31 15:29:33'),(338,57,12014,47.00,'支付宝','APP','2017-08-31 15:29:33'),(339,56,12006,37.00,'微信支付','APP','2017-08-31 15:29:33'),(340,57,12006,47.00,'支付宝','APP','2017-08-31 15:29:33'),(341,56,12016,37.00,'支付宝','微信','2017-08-31 15:29:33'),(342,57,12016,47.00,'微信支付','微信','2017-08-31 15:29:33'),(343,56,12019,37.00,'微信支付','APP','2017-08-31 15:29:33'),(344,57,12019,47.00,'微信支付','微信','2017-08-31 15:29:33'),(345,56,12004,37.00,'支付宝','微信','2017-08-31 15:29:33'),(346,57,12004,47.00,'微信支付','APP','2017-08-31 15:29:33'),(347,56,12007,37.00,'微信支付','微信','2017-08-31 15:29:33'),(348,57,12007,47.00,'微信支付','微信','2017-08-31 15:29:33'),(349,56,12003,37.00,'微信支付','APP','2017-08-31 15:29:33'),(350,57,12003,47.00,'支付宝','APP','2017-08-31 15:29:33'),(351,56,12025,37.00,'支付宝','微信','2017-08-31 15:29:33'),(352,57,12025,47.00,'微信支付','微信','2017-08-31 15:29:33'),(353,56,12012,37.00,'微信支付','微信','2017-08-31 15:29:33'),(354,57,12012,47.00,'支付宝','APP','2017-08-31 15:29:33'),(355,56,12008,37.00,'微信支付','APP','2017-08-31 15:29:33'),(356,57,12008,47.00,'支付宝','微信','2017-08-31 15:29:33'),(357,56,12000,37.00,'支付宝','微信','2017-08-31 15:29:33'),(358,57,12000,47.00,'微信支付','APP','2017-08-31 15:29:33'),(359,56,12005,37.00,'支付宝','微信','2017-08-31 15:29:33'),(360,57,12005,47.00,'支付宝','微信','2017-08-31 15:29:33'),(361,56,12029,37.00,'微信支付','APP','2017-08-30 15:29:33'),(362,57,12029,47.00,'微信支付','APP','2017-08-30 15:29:33'),(363,56,12112,37.00,'支付宝','APP','2017-08-30 15:29:33'),(364,57,12112,47.00,'微信支付','APP','2017-08-30 15:29:33'),(365,56,12021,37.00,'微信支付','APP','2017-08-30 15:29:33'),(366,57,12021,47.00,'支付宝','APP','2017-08-30 15:29:33'),(367,56,12099,37.00,'支付宝','APP','2017-08-30 15:29:33'),(368,57,12099,47.00,'微信支付','微信','2017-08-30 15:29:33'),(369,56,12014,37.00,'微信支付','APP','2017-08-30 15:29:33'),(370,57,12014,47.00,'支付宝','微信','2017-08-30 15:29:33'),(371,56,12006,37.00,'支付宝','微信','2017-08-30 15:29:33'),(372,57,12006,47.00,'微信支付','APP','2017-08-30 15:29:33'),(373,56,12016,37.00,'微信支付','微信','2017-08-30 15:29:33'),(374,57,12016,47.00,'微信支付','APP','2017-08-30 15:29:33'),(375,56,12019,37.00,'支付宝','APP','2017-08-30 15:29:33'),(376,57,12019,47.00,'微信支付','微信','2017-08-30 15:29:33'),(377,56,12004,37.00,'支付宝','微信','2017-08-30 15:29:33'),(378,57,12004,47.00,'微信支付','APP','2017-08-30 15:29:33'),(379,56,12007,37.00,'微信支付','微信','2017-08-30 15:29:33'),(380,57,12007,47.00,'支付宝','微信','2017-08-30 15:29:33'),(381,56,12003,37.00,'支付宝','APP','2017-08-30 15:29:33'),(382,57,12003,47.00,'微信支付','APP','2017-08-30 15:29:33'),(383,56,12025,37.00,'支付宝','微信','2017-08-30 15:29:33'),(384,57,12025,47.00,'支付宝','APP','2017-08-30 15:29:33'),(385,56,12012,37.00,'支付宝','微信','2017-08-30 15:29:33'),(386,57,12012,47.00,'微信支付','微信','2017-08-30 15:29:33'),(387,56,12008,37.00,'微信支付','APP','2017-08-30 15:29:33'),(388,57,12008,47.00,'支付宝','微信','2017-08-30 15:29:33'),(389,56,12000,37.00,'微信支付','APP','2017-08-30 15:29:33'),(390,57,12000,47.00,'支付宝','APP','2017-08-30 15:29:33'),(391,56,12029,37.00,'支付宝','微信','2017-08-29 15:29:33'),(392,57,12029,47.00,'微信支付','微信','2017-08-29 15:29:33'),(393,56,12112,37.00,'支付宝','微信','2017-08-29 15:29:33'),(394,57,12112,47.00,'支付宝','APP','2017-08-29 15:29:33'),(395,56,12021,37.00,'微信支付','APP','2017-08-29 15:29:33'),(396,57,12021,47.00,'微信支付','微信','2017-08-29 15:29:33'),(397,56,12099,37.00,'支付宝','APP','2017-08-29 15:29:33'),(398,57,12099,47.00,'支付宝','APP','2017-08-29 15:29:33'),(399,56,12014,37.00,'微信支付','微信','2017-08-29 15:29:33'),(400,57,12014,47.00,'支付宝','APP','2017-08-29 15:29:33'),(401,56,12006,37.00,'微信支付','APP','2017-08-29 15:29:33'),(402,57,12006,47.00,'微信支付','微信','2017-08-29 15:29:33'),(403,56,12016,37.00,'支付宝','微信','2017-08-29 15:29:33'),(404,57,12016,47.00,'微信支付','微信','2017-08-29 15:29:33'),(405,56,12019,37.00,'微信支付','微信','2017-08-29 15:29:33'),(406,57,12019,47.00,'支付宝','微信','2017-08-29 15:29:33'),(407,56,12004,37.00,'微信支付','APP','2017-08-29 15:29:33'),(408,57,12004,47.00,'微信支付','微信','2017-08-29 15:29:33'),(409,56,12007,37.00,'微信支付','微信','2017-08-29 15:29:33'),(410,57,12007,47.00,'微信支付','APP','2017-08-29 15:29:33'),(411,56,12003,37.00,'微信支付','微信','2017-08-29 15:29:33'),(412,57,12003,47.00,'微信支付','APP','2017-08-29 15:29:33'),(413,56,12025,37.00,'微信支付','微信','2017-08-29 15:29:33'),(414,57,12025,47.00,'微信支付','APP','2017-08-29 15:29:33'),(415,56,12012,37.00,'支付宝','微信','2017-08-29 15:29:33'),(416,57,12012,47.00,'支付宝','APP','2017-08-29 15:29:33'),(417,56,12008,37.00,'微信支付','APP','2017-08-29 15:29:33'),(418,57,12008,47.00,'微信支付','APP','2017-08-29 15:29:33'),(419,58,12124,63.00,'微信支付','APP','2017-09-04 15:29:33'),(420,59,12124,52.00,'微信支付','APP','2017-09-04 15:29:33'),(421,58,12125,63.00,'微信支付','APP','2017-09-04 15:29:33'),(422,59,12125,52.00,'微信支付','微信','2017-09-04 15:29:33'),(423,58,12126,63.00,'微信支付','微信','2017-09-04 15:29:33'),(424,59,12126,52.00,'支付宝','APP','2017-09-04 15:29:33'),(425,58,12124,63.00,'支付宝','APP','2017-09-03 15:29:33'),(426,59,12124,52.00,'微信支付','APP','2017-09-03 15:29:33'),(427,58,12125,63.00,'微信支付','微信','2017-09-03 15:29:33'),(428,59,12125,52.00,'微信支付','微信','2017-09-03 15:29:33'),(429,58,12126,63.00,'支付宝','APP','2017-09-03 15:29:33'),(430,59,12126,52.00,'微信支付','微信','2017-09-03 15:29:33'),(431,58,12124,63.00,'支付宝','APP','2017-09-02 15:29:33'),(432,59,12124,52.00,'支付宝','微信','2017-09-02 15:29:33'),(433,58,12125,63.00,'支付宝','APP','2017-09-02 15:29:33'),(434,59,12125,52.00,'支付宝','微信','2017-09-02 15:29:33'),(435,58,12126,63.00,'微信支付','APP','2017-09-02 15:29:33'),(436,59,12126,52.00,'支付宝','微信','2017-09-02 15:29:33'),(437,58,12124,63.00,'微信支付','微信','2017-09-01 15:29:33'),(438,59,12124,52.00,'支付宝','微信','2017-09-01 15:29:33'),(439,58,12125,63.00,'支付宝','微信','2017-09-01 15:29:33'),(440,59,12125,52.00,'支付宝','微信','2017-09-01 15:29:33'),(441,58,12126,63.00,'支付宝','微信','2017-09-01 15:29:33'),(442,59,12126,52.00,'微信支付','APP','2017-09-01 15:29:33'),(443,58,12124,63.00,'支付宝','APP','2017-08-31 15:29:33'),(444,59,12124,52.00,'微信支付','微信','2017-08-31 15:29:33'),(445,58,12125,63.00,'支付宝','微信','2017-08-31 15:29:33'),(446,59,12125,52.00,'微信支付','APP','2017-08-31 15:29:33'),(447,58,12126,63.00,'支付宝','APP','2017-08-31 15:29:33'),(448,59,12126,52.00,'支付宝','APP','2017-08-31 15:29:33'),(449,58,12124,63.00,'微信支付','APP','2017-08-30 15:29:33'),(450,59,12124,52.00,'微信支付','微信','2017-08-30 15:29:33'),(451,58,12125,63.00,'支付宝','APP','2017-08-30 15:29:33'),(452,59,12125,52.00,'微信支付','APP','2017-08-30 15:29:33'),(453,58,12126,63.00,'支付宝','APP','2017-08-30 15:29:33'),(454,59,12126,52.00,'支付宝','微信','2017-08-30 15:29:33'),(455,58,12124,63.00,'微信支付','微信','2017-08-29 15:29:33'),(456,59,12124,52.00,'支付宝','APP','2017-08-29 15:29:33'),(457,58,12125,63.00,'支付宝','APP','2017-08-29 15:29:33'),(458,59,12125,52.00,'支付宝','APP','2017-08-29 15:29:33'),(459,58,12126,63.00,'微信支付','APP','2017-08-29 15:29:33'),(460,59,12126,52.00,'支付宝','微信','2017-08-29 15:29:33'),(461,62,12120,49.00,'支付宝','微信','2017-09-04 15:29:33'),(462,63,12120,30.00,'支付宝','APP','2017-09-04 15:29:33'),(463,62,12123,49.00,'支付宝','APP','2017-09-04 15:29:33'),(464,63,12123,30.00,'微信支付','微信','2017-09-04 15:29:33'),(465,62,12120,49.00,'支付宝','APP','2017-09-03 15:29:33'),(466,63,12120,30.00,'微信支付','微信','2017-09-03 15:29:33'),(467,62,12123,49.00,'支付宝','APP','2017-09-03 15:29:33'),(468,63,12123,30.00,'支付宝','微信','2017-09-03 15:29:33'),(469,62,12120,49.00,'支付宝','APP','2017-09-02 15:29:33'),(470,63,12120,30.00,'支付宝','APP','2017-09-02 15:29:33'),(471,62,12123,49.00,'微信支付','微信','2017-09-02 15:29:33'),(472,63,12123,30.00,'微信支付','APP','2017-09-02 15:29:33'),(473,62,12120,49.00,'支付宝','APP','2017-09-01 15:29:33'),(474,63,12120,30.00,'支付宝','微信','2017-09-01 15:29:33'),(475,62,12123,49.00,'支付宝','微信','2017-09-01 15:29:33'),(476,63,12123,30.00,'支付宝','微信','2017-09-01 15:29:33'),(477,62,12120,49.00,'微信支付','微信','2017-08-31 15:29:33'),(478,63,12120,30.00,'支付宝','APP','2017-08-31 15:29:33'),(479,62,12123,49.00,'微信支付','微信','2017-08-31 15:29:33'),(480,63,12123,30.00,'微信支付','APP','2017-08-31 15:29:33'),(481,62,12120,49.00,'微信支付','APP','2017-08-30 15:29:33'),(482,63,12120,30.00,'微信支付','APP','2017-08-30 15:29:33'),(483,62,12123,49.00,'支付宝','微信','2017-08-30 15:29:33'),(484,63,12123,30.00,'支付宝','微信','2017-08-30 15:29:33'),(485,62,12120,49.00,'支付宝','APP','2017-08-29 15:29:33'),(486,63,12120,30.00,'微信支付','微信','2017-08-29 15:29:33'),(487,62,12123,49.00,'微信支付','APP','2017-08-29 15:29:33'),(488,63,12123,30.00,'支付宝','APP','2017-08-29 15:29:33');
/*!40000 ALTER TABLE `bd_package_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_package_tag`
--

DROP TABLE IF EXISTS `bd_package_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_package_tag` (
  `package_id` int(11) NOT NULL COMMENT '套餐id',
  `tag_id` int(11) NOT NULL COMMENT '标签id',
  PRIMARY KEY (`package_id`,`tag_id`),
  KEY `fk_packtag_tag_id` (`tag_id`),
  CONSTRAINT `fk_packtag_package_id` FOREIGN KEY (`package_id`) REFERENCES `bd_package` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_packtag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `bd_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_package_tag`
--

LOCK TABLES `bd_package_tag` WRITE;
/*!40000 ALTER TABLE `bd_package_tag` DISABLE KEYS */;
INSERT INTO `bd_package_tag` VALUES (17,12),(18,10),(18,12),(26,32),(27,1),(27,10),(28,10),(32,32),(33,32),(34,1),(34,10),(34,12),(34,15),(34,17),(35,32),(35,46),(35,48),(39,32),(39,46),(39,48),(41,32),(41,48),(42,48),(43,48),(44,15),(44,69),(46,32),(46,46),(46,48),(46,56),(46,81),(47,48),(48,48),(49,48),(53,56),(53,81),(56,81),(57,32),(57,46),(72,84),(73,84),(74,84),(75,32),(75,48),(77,56),(79,81),(81,32),(86,81);
/*!40000 ALTER TABLE `bd_package_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_pn_field`
--

DROP TABLE IF EXISTS `bd_pn_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_pn_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL COMMENT '项目编号',
  `dyncol_id` int(11) NOT NULL COMMENT '动态列id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_pnfield_col` (`pn`,`dyncol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_pn_field`
--

LOCK TABLES `bd_pn_field` WRITE;
/*!40000 ALTER TABLE `bd_pn_field` DISABLE KEYS */;
INSERT INTO `bd_pn_field` VALUES (83,1101310510,1),(81,1132897105,1),(82,1132897105,2),(73,1410277206,1),(74,1410277206,2),(75,1410277206,3),(78,1410277206,6),(79,1410277206,7),(65,1535741440,1),(66,1535741440,2),(67,1535741440,3),(63,1674191091,1),(64,1674191091,2);
/*!40000 ALTER TABLE `bd_pn_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_portal`
--

DROP TABLE IF EXISTS `bd_portal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_portal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT 'portal页面所属项目, 0为平台默认portal页',
  `name` varchar(32) NOT NULL COMMENT 'portal页名称',
  `note` varchar(128) DEFAULT NULL COMMENT '备注',
  `mobile_title` varchar(64) NOT NULL COMMENT '移动端头部文案内容',
  `mobile_banner_url` varchar(256) NOT NULL COMMENT '移动端顶部banner图片链接',
  `pc_title` varchar(64) NOT NULL COMMENT 'PC 文案内容',
  `pc_banner_url` varchar(256) NOT NULL COMMENT 'PC 顶部banner图片链接',
  `on_using` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否为默认模版, 仅对平台portal模版有意义',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_portal_pn_name` (`pn`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_portal`
--

LOCK TABLES `bd_portal` WRITE;
/*!40000 ALTER TABLE `bd_portal` DISABLE KEYS */;
INSERT INTO `bd_portal` VALUES (1,1,'测试Portal','dddd','PC壁咚WiFi','http://or7x902xd.bkt.clouddn.com/Fufh0GnqQDyzHxy-QrbwKX163Rpb','壁咚WiFi','http://or7x902xd.bkt.clouddn.com/Fufh0GnqQDyzHxy-QrbwKX163Rpb',0,'2017-08-22 11:39:37','2017-08-22 11:39:54'),(5,0,'壁咚','bidong','壁咚pc','http://or7x902xd.bkt.clouddn.com/Fufh0GnqQDyzHxy-QrbwKX163Rpb','壁咚移大拇指动','http://or7x902xd.bkt.clouddn.com/Fufh0GnqQDyzHxy-QrbwKX163Rpb',0,'2017-08-22 16:19:28','2017-09-05 10:03:15'),(9,0,'dd','1','1234','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',1,'2017-08-24 17:35:08','2017-09-05 10:03:15'),(10,0,'825test','825','测试PC','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','测试','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-08-25 09:22:13','2017-08-28 14:18:49'),(12,1,'825CES ','123456','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-08-25 09:43:40','2017-08-25 09:43:40'),(13,1,'82525','82525','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-08-25 09:50:19','2017-08-25 09:50:19'),(15,1,'项目不能删除','note','D','http://or7x902xd.bkt.clouddn.com/FsSLWUeTBUfYrE8YryY5PAQTRPst','d','http://or7x902xd.bkt.clouddn.com/FsSLWUeTBUfYrE8YryY5PAQTRPst',0,'2017-08-25 15:32:55','2017-08-25 15:50:18'),(19,0,'82','83','456','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-08-28 13:51:46','2017-08-28 13:51:46'),(20,1,'828项目','828项目','2','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','1','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-08-28 14:16:11','2017-08-28 14:16:11'),(21,0,'828平台','123','2','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','1','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-08-28 14:18:23','2017-08-30 11:16:11'),(22,0,'string1','string1','string1','string1','string1','string1',0,'2017-08-29 15:14:01','2017-08-30 11:16:13'),(25,0,'123456','1234','567','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','456','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-09-01 11:04:09','2017-09-01 11:04:09'),(26,1,'931','542','789','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','456','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-09-01 11:08:23','2017-09-01 11:08:23'),(28,1132897105,'945','测试5','3455','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','2345','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-09-04 16:52:12','2017-09-04 16:52:35'),(30,1535741440,'96','96','966','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','96','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-09-06 10:04:38','2017-09-06 10:04:38'),(31,1410277206,'789456','789456','456','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI','123','http://or7x902xd.bkt.clouddn.com/FpOkxXlRhS0qxS71mXCl-b7iTeaI',0,'2017-09-06 10:38:43','2017-09-06 10:38:43');
/*!40000 ALTER TABLE `bd_portal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_tag`
--

DROP TABLE IF EXISTS `bd_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_type` varchar(64) NOT NULL COMMENT '标签类型，user, pay_policy etc',
  `name` varchar(32) NOT NULL COMMENT '标签名',
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT '所属项目,默认0为平台标签',
  `created_at` datetime COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_pn_tagtype` (`pn`,`tag_type`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_tag`
--

LOCK TABLES `bd_tag` WRITE;
/*!40000 ALTER TABLE `bd_tag` DISABLE KEYS */;
INSERT INTO `bd_tag` VALUES (1,'account','司机',1,'2017-07-31 15:12:20'),(6,'account','优惠',12,'2017-08-01 09:46:51'),(7,'account','优惠',12,'2017-08-01 09:47:13'),(8,'account','优惠',12,'2017-08-01 09:47:15'),(9,'account','优惠',12,'2017-08-01 09:47:16'),(10,'account','老师',1,'2017-08-01 10:13:56'),(12,'account','学生',1,'2017-08-01 10:18:09'),(15,'account','租客',1,'2017-08-01 14:02:07'),(17,'account','店员',1,'2017-08-01 14:02:19'),(32,'account','克瑞斯',0,'2017-08-04 16:34:26'),(46,'account','test',0,'2017-08-25 10:40:25'),(48,'account','828',0,'2017-08-28 11:05:50'),(49,'ap','南沙',1,'2017-08-28 14:33:59'),(50,'ap','番禺',1,'2017-08-28 14:34:56'),(56,'account','test',0,'2017-08-29 11:30:24'),(69,'account','cdd',1,'2017-08-31 15:04:42'),(76,'account','213',1674191091,'2017-09-01 15:33:30'),(77,'ap','12',1131221010,'2017-09-01 16:03:44'),(79,'ap','11',1146852709,'2017-09-01 17:36:51'),(81,'account','test1',0,'2017-09-04 13:27:03'),(82,'ap','201794',1132897105,'2017-09-04 15:16:00'),(83,'ap','201795',1132897105,'2017-09-04 15:22:18'),(84,'account','94用户标签',1132897105,'2017-09-04 15:32:37'),(86,'ap','南沙',1146852709,'2017-09-04 16:56:26'),(87,'ap','离线',1146852709,'2017-09-04 16:56:30'),(88,'ap','南横',1146852709,'2017-09-04 16:56:43'),(89,'ap','天河',1146852709,'2017-09-04 16:56:47'),(90,'ap','95ap',1535741440,'2017-09-05 09:10:50'),(91,'account','95项目用户标签',1535741440,'2017-09-05 13:50:10'),(92,'account','语文',1132897105,'2017-09-05 16:19:35'),(93,'account','数学',1132897105,'2017-09-05 16:19:40'),(94,'account','英语',1132897105,'2017-09-05 16:19:44'),(95,'account','化学',1132897105,'2017-09-05 16:19:49'),(96,'account','物理',1132897105,'2017-09-05 16:19:52'),(97,'account','生物',1132897105,'2017-09-05 16:19:56'),(98,'ap','111',1131221010,'2017-09-06 09:16:58');
/*!40000 ALTER TABLE `bd_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_ticket`
--

DROP TABLE IF EXISTS `bd_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_ticket` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(64) NOT NULL COMMENT '上网账号',
  `acct_session_id` varchar(64) NOT NULL COMMENT 'session id',
  `acct_session_time` int(11) NOT NULL DEFAULT '0' COMMENT '上网时长',
  `session_timeout` int(11) NOT NULL DEFAULT '0',
  `acct_terminate_cause` int(11) NOT NULL DEFAULT '0' COMMENT '连接结束原因,空闲|主动断开|上网到期',
  `acct_input_octets` int(11) DEFAULT '0' COMMENT '下行数据',
  `acct_output_octets` int(11) DEFAULT '0' COMMENT '上行数据',
  `acct_input_packets` int(11) DEFAULT '0' COMMENT '下行数据包',
  `acct_output_packets` int(11) DEFAULT '0' COMMENT '上行数据包',
  `nas_addr` varchar(24) NOT NULL COMMENT 'ac IP地址',
  `mac_addr` varchar(24) NOT NULL COMMENT '用户mac地址',
  `ap_mac` varchar(24) NOT NULL DEFAULT '' COMMENT 'ap mac地址',
  `framed_ipaddr` varchar(24) NOT NULL DEFAULT '' COMMENT '用户ip地址',
  `start_source` smallint(6) NOT NULL DEFAULT '0',
  `stop_source` smallint(6) NOT NULL DEFAULT '0',
  `acct_start_time` datetime COMMENT '会话起始时间',
  `acct_stop_time` datetime  COMMENT '会话结束时间',
  `pn` varchar(128) NOT NULL DEFAULT '' COMMENT '网络所属项目',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_ticket`
--

LOCK TABLES `bd_ticket` WRITE;
/*!40000 ALTER TABLE `bd_ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_user`
--

DROP TABLE IF EXISTS `bd_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(64) NOT NULL COMMENT '关联的bd_account.user字段',
  `mask` int(11) unsigned NOT NULL COMMENT '账号标识',
  `value` varchar(128) NOT NULL COMMENT '存储与mask相关的信息字段',
  `note` varchar(256) NOT NULL COMMENT '若微信账号注册，则此字段为appid+tid, 否则为null',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_value` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_user`
--

LOCK TABLES `bd_user` WRITE;
/*!40000 ALTER TABLE `bd_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_wechat_official_account`
--

DROP TABLE IF EXISTS `bd_wechat_official_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_wechat_official_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL COMMENT '所属项目',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '公众号名称',
  `appid` varchar(32) NOT NULL COMMENT '微信公众号appid',
  `shopid` varchar(32) NOT NULL COMMENT '门店ID，用于微信上网',
  `secret` varchar(64) NOT NULL COMMENT '公众号secret',
  `note` varchar(128) NOT NULL DEFAULT '' COMMENT '备注',
  `is_deleted` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_wx_appid` (`pn`,`appid`,`is_deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_wechat_official_account`
--

LOCK TABLES `bd_wechat_official_account` WRITE;
/*!40000 ALTER TABLE `bd_wechat_official_account` DISABLE KEYS */;
INSERT INTO `bd_wechat_official_account` VALUES (1,1,'1','1','1','1','1',1,'2017-08-11 17:35:17','2017-08-11 17:36:47'),(2,1,'啊啊啊阿道夫','323','346','6','767',1,'2017-08-11 17:36:53','2017-08-11 17:41:22'),(3,1,'南沙科技园','fd9834l','f9324f8902rccdd','df982wefj98341','南沙资讯科技园1',1,'2017-08-11 17:41:58','2017-08-14 09:46:07'),(4,1,'参差错落1','sdaf902odf01','d0f901','df0f2','ss1',0,'2017-08-14 09:46:37','2017-08-14 09:59:17'),(5,1,'车联网公众号','1','1','1','',0,'2017-08-15 15:55:13','2017-08-22 15:25:18'),(6,1,'中科','gwerg32','g4b4352g','2345h23t3234','',1,'2017-08-22 15:26:34','2017-08-22 15:26:39'),(7,1,'中科','gwerg32','g4b4352g','2345h23t3234','',0,'2017-08-22 15:26:43','2017-08-22 15:26:43'),(8,1,'中科2','gwerg3232','g4b4352g231','2345h23t32341','',0,'2017-08-22 15:26:51','2017-08-22 15:26:59'),(9,1,'828公众号111','1111','22','32','4',1,'2017-08-28 14:21:37','2017-08-28 14:25:35'),(10,1,'828公众号','111','2','3','4',0,'2017-08-28 14:26:37','2017-08-28 14:26:55'),(11,1,'91','91','91','91','',0,'2017-09-01 11:08:48','2017-09-01 11:08:48'),(12,1131221010,'1','123344555','1','1','1',0,'2017-09-01 17:19:54','2017-09-01 17:19:54'),(13,1146852709,'aa','aaa','aa','aa','aa',0,'2017-09-04 11:29:38','2017-09-04 11:29:38'),(14,1132897105,'201794公众号123','111111111','2','3','4',0,'2017-09-04 16:33:43','2017-09-04 16:33:43'),(15,1131221010,'3','4','5','6','7',0,'2017-09-04 16:46:11','2017-09-04 16:46:11'),(16,1131221010,'89','99','109','119','129',1,'2017-09-04 16:47:32','2017-09-04 16:48:11'),(17,1535741440,'95','95','96','97','98',0,'2017-09-05 09:17:55','2017-09-05 09:17:55'),(18,1410277206,'111','111','222','333','444',0,'2017-09-06 10:37:05','2017-09-06 10:37:05'),(19,1101310510,'南沙日报','111111','111111111','1111111111','日报',0,'2017-09-07 15:02:20','2017-09-07 15:02:20');
/*!40000 ALTER TABLE `bd_wechat_official_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bd_wechat_user`
--

DROP TABLE IF EXISTS `bd_wechat_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_wechat_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL COMMENT '关联平台用户id',
  `appid` varchar(64) NOT NULL COMMENT '公众号appid',
  `openid` varchar(64) NOT NULL COMMENT '用户openid',
  `mask` int(11) unsigned NOT NULL COMMENT '账号标识, mask & 1 > 0已关注公众号',
  `note` varchar(256) NOT NULL DEFAULT '' COMMENT '备注',
  `created_at` datetime COMMENT '创建时间',
  `updated_at` datetime COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_wechat_user` (`account_id`,`appid`,`openid`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bd_wechat_user`
--

LOCK TABLES `bd_wechat_user` WRITE;
/*!40000 ALTER TABLE `bd_wechat_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `bd_wechat_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managers`
--

DROP TABLE IF EXISTS `managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `managers` (
  `id` int(10) NOT NULL COMMENT '主键,manager_id',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'name of the manager',
  `description` varchar(256) NOT NULL DEFAULT '' COMMENT 'brief of the manager',
  `mobile` bigint(20) NOT NULL DEFAULT '0' COMMENT '手機號',
  `status` tinyint(5) NOT NULL DEFAULT '1' COMMENT '状态，2为删除，1为可用，0为不可用',
  `create_time` int(10) NOT NULL DEFAULT '0' COMMENT '创建时间，时间戳',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managers`
--

LOCK TABLES `managers` WRITE;
/*!40000 ALTER TABLE `managers` DISABLE KEYS */;
INSERT INTO `managers` VALUES (1087029815,'鹏','没有',13211112222,1,1504252616),(1100350806,'18925152233','',18925152233,1,1504573546),(1411410731,'韩梅梅','李雷的初恋女友',15555555555,1,1504240475),(1450895554,'Jimmy','I am 美国人',17777777777,1,1504240949),(1517121291,'Poly','一只鹦鹉',16666666666,1,1504240671),(1545224857,'18925151111','测试',18925151111,1,1504495153),(1608581031,'奥地利','测试',13233332222,1,1504254250),(1609968344,'此手机号不存在','',18925154444,0,1504253827),(1710487325,'Sick','I am sick',12222222222,1,1504241176),(1811074577,'东方','东方管理员',13456665565,1,1504599911),(1815352072,'此手机号不存在','第一次出道，有点紧张',11111111111,1,1504246274),(1954999235,'18925153333','测试',18925153333,1,1504495984),(2147483647,'李雷','韩梅梅的初恋男友',18888888888,1,1504240174);
/*!40000 ALTER TABLE `managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managers_authorization`
--

DROP TABLE IF EXISTS `managers_authorization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `managers_authorization` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `authorization_holder` int(10) NOT NULL COMMENT '被授权主体的身份ID，可以是管理员id也可以是管理员组id',
  `holder_type` int(10) NOT NULL DEFAULT '0' COMMENT '被授权主体的类型,比如管理员,管理员组,默认为0代表一般的管理员个体, 将来扩展时详细定义',
  `resource_id` int(11) NOT NULL COMMENT '资源id, 对应于resource_registry表中的id字段',
  `resource_name` varchar(64) NOT NULL DEFAULT '' COMMENT '资源名称, public_name',
  `resource_locator` varchar(128) NOT NULL DEFAULT '' COMMENT '资源定位符, 一个具体资源在其所属类别中的标识符, 根据resource_id和resource_locator可以定位到一个资源, 类似uri的作用，留空时表示该类别中的所有资源',
  `allow_method` tinyint(4) NOT NULL DEFAULT '15' COMMENT '参考Linux文件权限,8为读,4为增,2为改,1为删,如有多个权限,累加.判断是否有某个权限时,比如最终结果为15,15 and 8 = 8,那么则为有读权限.',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否生效,1为是,0为否',
  PRIMARY KEY (`id`),
  UNIQUE KEY `authorization_holder` (`authorization_holder`,`resource_name`,`resource_locator`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managers_authorization`
--

LOCK TABLES `managers_authorization` WRITE;
/*!40000 ALTER TABLE `managers_authorization` DISABLE KEYS */;
INSERT INTO `managers_authorization` VALUES (1,2147483647,0,10,'client_portal_page_management','1674191091',15,2),(2,2147483647,0,8,'client_user_management','1131221010',15,2),(3,2147483647,0,11,'client_wx_management','1131221010',15,2),(4,2147483647,0,8,'client_user_management','1674191091',15,2),(5,2147483647,0,7,'client_project_management','1131221010',15,2),(6,2147483647,0,7,'client_project_management','1674191091',15,2),(7,1815352072,0,11,'client_wx_management','1131221010',15,1),(8,1815352072,0,11,'client_wx_management','1674191091',15,1),(9,1815352072,0,8,'client_user_management','1131221010',15,1),(10,1815352072,0,7,'client_project_management','1131221010',15,1),(11,1815352072,0,10,'client_portal_page_management','1674191091',15,1),(12,1087029815,0,7,'client_project_management','1131221010',15,1),(13,1087029815,0,9,'client_finance_management','1131221010',15,1),(14,1087029815,0,10,'client_portal_page_management','1131221010',15,1),(15,1087029815,0,11,'client_wx_management','1131221010',15,1),(16,1087029815,0,8,'client_user_management','1131221010',15,1),(17,1609968344,0,7,'client_project_management','1316118103',15,1),(18,1609968344,0,7,'client_project_management','1131221010',15,1),(19,1609968344,0,11,'client_wx_management','1316118103',15,1),(20,1609968344,0,10,'client_portal_page_management','1131221010',15,1),(21,1609968344,0,11,'client_wx_management','1131221010',15,1),(22,1609968344,0,9,'client_finance_management','1131221010',15,1),(23,1609968344,0,9,'client_finance_management','1316118103',15,1),(24,1609968344,0,8,'client_user_management','1316118103',15,1),(25,1609968344,0,8,'client_user_management','1131221010',15,1),(26,1609968344,0,10,'client_portal_page_management','1316118103',15,1),(27,1608581031,0,8,'client_user_management','1316118103',15,1),(28,1608581031,0,11,'client_wx_management','1253910457',15,1),(29,1608581031,0,10,'client_portal_page_management','1316118103',15,1),(30,1608581031,0,10,'client_portal_page_management','1674191091',15,1),(31,1608581031,0,9,'client_finance_management','1131221010',15,1),(32,1608581031,0,11,'client_wx_management','1316118103',15,1),(33,1608581031,0,9,'client_finance_management','1674191091',15,1),(34,1608581031,0,11,'client_wx_management','1342451022',15,1),(35,1608581031,0,10,'client_portal_page_management','1131221010',15,1),(36,2147483647,0,11,'client_wx_management','1146852709',15,1),(37,2147483647,0,10,'client_portal_page_management','1146852709',15,1),(38,2147483647,0,7,'client_project_management','1146852709',15,1),(39,2147483647,0,7,'client_project_management','1253910457',15,1),(40,2147483647,0,9,'client_finance_management','1146852709',15,1),(41,2147483647,0,9,'client_finance_management','1253910457',15,1),(42,2147483647,0,8,'client_user_management','1146852709',15,1),(43,2147483647,0,10,'client_portal_page_management','1253910457',15,1),(44,2147483647,0,8,'client_user_management','1132897105',15,1),(45,2147483647,0,10,'client_portal_page_management','1132897105',15,1),(46,2147483647,0,11,'client_wx_management','1132897105',15,1),(47,2147483647,0,7,'client_project_management','1132897105',15,1),(48,2147483647,0,9,'client_finance_management','1132897105',15,1),(49,1545224857,0,8,'client_user_management','1132897105',15,1),(50,1545224857,0,10,'client_portal_page_management','1132897105',15,1),(51,1545224857,0,11,'client_wx_management','1132897105',15,1),(52,1545224857,0,9,'client_finance_management','1132897105',15,1),(53,1545224857,0,7,'client_project_management','1132897105',15,1),(54,1954999235,0,7,'client_project_management','1132897105',15,1),(55,1954999235,0,10,'client_portal_page_management','1132897105',15,1),(56,1954999235,0,9,'client_finance_management','1132897105',15,1),(57,1100350806,0,11,'client_wx_management','1535741440',15,1),(58,1100350806,0,10,'client_portal_page_management','1535741440',15,1),(59,1100350806,0,8,'client_user_management','1535741440',15,1),(60,1100350806,0,7,'client_project_management','1535741440',15,1),(61,1100350806,0,9,'client_finance_management','1535741440',15,1),(62,2147483647,0,8,'client_user_management','1535741440',15,1),(63,2147483647,0,9,'client_finance_management','1535741440',15,1),(64,2147483647,0,11,'client_wx_management','1535741440',15,1),(65,2147483647,0,10,'client_portal_page_management','1535741440',15,1),(66,2147483647,0,7,'client_project_management','1535741440',15,1),(67,2147483647,0,7,'client_project_management','1399911227',15,2),(68,2147483647,0,8,'client_user_management','1399911227',15,2),(69,2147483647,0,9,'client_finance_management','1399911227',15,2),(70,1811074577,0,10,'client_portal_page_management','1674191091',15,2),(71,1811074577,0,11,'client_wx_management','1674191091',15,2),(72,1811074577,0,9,'client_finance_management','1399911227',15,2),(73,1811074577,0,8,'client_user_management','1132897105',15,1),(74,1811074577,0,10,'client_portal_page_management','1342451022',15,2),(75,1811074577,0,8,'client_user_management','1399911227',15,2),(76,1811074577,0,8,'client_user_management','1535741440',15,2),(77,1811074577,0,7,'client_project_management','1131221010',15,2),(78,1811074577,0,11,'client_wx_management','1535741440',15,2),(79,1811074577,0,9,'client_finance_management','1342451022',15,2),(80,1811074577,0,9,'client_finance_management','1146852709',15,2),(81,1811074577,0,11,'client_wx_management','1316118103',15,2),(82,1811074577,0,10,'client_portal_page_management','1253910457',15,2),(83,1811074577,0,11,'client_wx_management','1132897105',15,1),(84,2147483647,0,11,'client_wx_management','1122327156',15,1),(85,2147483647,0,8,'client_user_management','1410277206',15,1),(86,2147483647,0,10,'client_portal_page_management','1410277206',15,1),(87,2147483647,0,9,'client_finance_management','1410277206',15,1),(88,2147483647,0,7,'client_project_management','1410277206',15,1),(89,2147483647,0,11,'client_wx_management','1410277206',15,1),(90,1100350806,0,10,'client_portal_page_management','1410277206',15,1),(91,1100350806,0,11,'client_wx_management','1410277206',15,1),(92,1100350806,0,9,'client_finance_management','1410277206',15,1),(93,1100350806,0,8,'client_user_management','1410277206',15,1),(94,1100350806,0,7,'client_project_management','1410277206',15,1),(95,1811074577,0,8,'client_user_management','1131221010',15,2),(96,1811074577,0,8,'client_user_management','1122327156',15,1),(97,1811074577,0,9,'client_finance_management','1122327156',15,1),(98,1811074577,0,11,'client_wx_management','1122327156',15,1),(99,1811074577,0,10,'client_portal_page_management','1122327156',15,1),(100,1811074577,0,7,'client_project_management','1122327156',15,1),(101,2147483647,0,9,'client_finance_management','1101310510',15,1),(102,2147483647,0,8,'client_user_management','1101310510',15,1),(103,2147483647,0,7,'client_project_management','1101310510',15,1),(104,2147483647,0,11,'client_wx_management','1101310510',15,1),(105,2147483647,0,10,'client_portal_page_management','1101310510',15,1),(106,1811074577,0,7,'client_project_management','1441956746',15,1);
/*!40000 ALTER TABLE `managers_authorization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managers_password`
--

DROP TABLE IF EXISTS `managers_password`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `managers_password` (
  `id` int(10) NOT NULL COMMENT 'manager_id',
  `user_name` varchar(64) NOT NULL DEFAULT '' COMMENT '登錄的用戶名',
  `email` varchar(128) NOT NULL DEFAULT '' COMMENT '登錄用郵箱',
  `mobile` bigint(20) NOT NULL DEFAULT '0' COMMENT '登錄用手機號',
  `password` varchar(512) NOT NULL COMMENT '當前加鹽的密碼',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否已經重置 1為是 0為否',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managers_password`
--

LOCK TABLES `managers_password` WRITE;
/*!40000 ALTER TABLE `managers_password` DISABLE KEYS */;
INSERT INTO `managers_password` VALUES (1021675061,'','',12222222222,'pbkdf2:sha256:50000$z15AQSUu$55e299869189b4a84cccdb75bc056aceb43e248313c201758816a4645de4abe5',0),(1087029815,'','',13211112222,'pbkdf2:sha256:50000$QEkHEla4$629a8c1f720c937150fe0d90f5d5d8fbe82c8b3a0222a5a81294e73a437b5bec',0),(1100350806,'','',18925152233,'pbkdf2:sha256:50000$9F0uwTlM$211cddfcd96eae8090eae4790d46d8189cc477fd1876ac9d41e9226d0407fa47',0),(1103646091,'','',12222222222,'pbkdf2:sha256:50000$aaQGtK11$98539268e8098a2e8deefdf094cdea2755498d7583e8a61a05b3409f5ee6cabc',0),(1411410731,'','',15555555555,'pbkdf2:sha256:50000$tljv0sqS$6893c4da82f7c03c245ec18e18a9464848b139721671cc679f23e7f96008bb54',0),(1450895554,'','',16666666666,'pbkdf2:sha256:50000$g9Wed4Rn$62bba157c9bd183f89c6e32b3a1bd79e02c14de0db21f170f3aebee9dd2213b6',0),(1485102429,'','',12222222222,'pbkdf2:sha256:50000$4hBhsBPm$51dc0a3b9eaf150878004bb6b0bb8ded1fa42e6e3cbaec60a94b25b936fe0cdf',0),(1517121291,'','',16666666666,'pbkdf2:sha256:50000$3jRwrM9I$1933650aa22c4dc9e30283c22afef349b3f9f80d84c08bdbd2885d8b18d55806',0),(1545224857,'','',18925151111,'pbkdf2:sha256:50000$RNzlzr6G$984139208870cd2aa4216477457c5a06ac86e426f2fb44c429f2d5ee0e6bd41f',0),(1608581031,'','',13233332222,'pbkdf2:sha256:50000$O09QonyF$9aa4e89fb7549dabcf01b492cfc8e7a8dc0d69e990936818a3ba8f841b6089fa',0),(1609968344,'','',18925154444,'pbkdf2:sha256:50000$XSUkaJfA$09f62180e5545ec194ea68fa07c4d305dd8e0504262a69e08c61b21655db3dde',0),(1710487325,'','',12222222222,'pbkdf2:sha256:50000$SLZEU0Rt$315b97ae245cfd0db73ab52d81acad8896b2c158084e91950853476a52aa0b2a',0),(1811074577,'','',13456665565,'pbkdf2:sha256:50000$tYnoshtJ$b9cb791b971b3b7c84cba99feb5515b52d741e5bfc84a39c1d78f317bebdde44',0),(1815352072,'','',11111111111,'pbkdf2:sha256:50000$aAZ8ibP0$4c98d1c3bb91a3cd6f6d1c64d56bf279cfce0c1f7cf46fa2d0ff29ec9b70c940',0),(1954999235,'','',18925153333,'pbkdf2:sha256:50000$1l7myuYJ$c3cec38d435cb7efe7328f80fe7c4c6fdb76fa154d8c73c3f319010c2d288e8a',0),(1971588755,'','',12222222222,'pbkdf2:sha256:50000$EWkHfsgl$332560107f52623a93bc9ba7d04c5d0b151ccefbaa55416808cb3bb1f8611aa0',0),(2147483647,'','',18888888888,'pbkdf2:sha256:50000$y0bGG2Yq$062e3ad686ea6bc1b9813ad752de36787b40c8ac24796ef8324afdd71c896495',1);
/*!40000 ALTER TABLE `managers_password` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects` (
  `id` int(10) NOT NULL COMMENT '主键, project_id',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'name of the project',
  `description` varchar(256) NOT NULL DEFAULT '' COMMENT 'brief of the project',
  `location` varchar(256) NOT NULL DEFAULT '' COMMENT 'As its literal meaning',
  `contact` varchar(64) NOT NULL DEFAULT '' COMMENT 'As its literal meaning',
  `contact_number` bigint(20) NOT NULL DEFAULT '0' COMMENT '联系电话',
  `email` varchar(128) NOT NULL DEFAULT '' COMMENT 'contact''s e-mail',
  `status` tinyint(5) NOT NULL DEFAULT '1' COMMENT '状态，2为删除，1为可用，0为不可用',
  `create_time` int(10) NOT NULL DEFAULT '0' COMMENT '创建时间，时间戳',
  `auth_ap_amount` int(10) NOT NULL DEFAULT '0' COMMENT '授權AP數量',
  `expiration_time` int(10) NOT NULL DEFAULT '0' COMMENT '有效时间，时间戳',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1101310510,'201797','201797','南沙','李小姐',18925157788,'1',1,1504762399,800,1511971200),(1122327156,'测试95','测试9511','测试95','1',18925156699,'11',0,1504602746,1,1504602646),(1131221010,'我想象我们的相遇','在一场隆重的死亡背面','奥廖尔省叶列茨市涅瓦街221号','拉夫烈茨基',15187836756,'lancerpilgrim@outlook.com',0,1504244337,784,2304000),(1132897105,'20170904测试','测试','南沙','李小姐',18925153756,'wen@163.com',1,1504492795,500,1511971200),(1143978008,'20170904测试','测试','1234','王',18925153755,'wen@163.com',2,1504492028,2000,1509379200),(1146852709,'茨维塔耶娃','这是我最后一次呼唤你的名字。\n大雪落在，\n我锈迹斑斑的气管和肺叶上，\n说吧：今夜，我的嗓音是一列被截停的火车\n你的名字是俄罗斯漫长的国境线。\n','列科夫大街13号米高扬设计局','涅佐夫',18988988573,'rim@outlook.com',1,1504255636,527,1506009600),(1253910457,'一九二七年的春夜','我们在国境线相遇。\n因此错过了，\n这个呼啸着奔向终点的世界。\n而今夜，你是舞曲，世界是错误。','德国北威斯特法伦州波恩大学','曾韶',15973881118,'Shao@gmail.com',1,1504249441,768,2476800),(1316118103,'20170902测试','测试','12345','李',13925153755,'wen_wen_li',1,1504253433,1500,1506700800),(1342451022,'20170901下午','12345678','测试','测试',18925153756,'wen_wen_li@163.com',1,1504249909,1500,20170930),(1349800005,'20170904测试','20170904test','南沙','李',18925153756,'wen@163.com',1,1504490481,1000,1506700800),(1399911227,'201795下午测试','测试项目','南沙','李小姐',18925153666,'1',1,1504593855,5001,1506700800),(1410277206,'20170906','测试','南沙','王先生',18925153788,'wjx@163.com',1,1504663941,10001,1509379200),(1441956746,'2','2','2','2',18925154477,'2',1,1504602763,3,1504602801),(1535741440,'20170905','测试','南沙','LI',18925151122,'123',0,1504573448,1000,1509379200),(1674191091,'北京市云江科技有限公司','五道口的月亮','北京市海淀区五道口优盛大厦','曾鼎',17710320836,'lancer@gmail.com',0,1504242095,1000,1512209873),(1723055899,'测禁用的项目','测禁用的项目','测禁用的项目','咚咚咚',13866662222,'deed',0,1504690241,1,1506700800);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_authorization`
--

DROP TABLE IF EXISTS `projects_authorization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_authorization` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `authorization_holder` int(10) NOT NULL COMMENT 'project_id,也可扩展为项目组id',
  `resource_name` varchar(64) NOT NULL DEFAULT '' COMMENT '资源名称, public_name',
  `resource_locator` varchar(128) NOT NULL DEFAULT '' COMMENT '资源定位符, 一个具体资源在其所属类别中的标识符，根据resource_id和resource_locator可以定位到一个资源, 类似uri的作用，留空时表示该类别中的所有资源',
  `holder_type` smallint(5) NOT NULL DEFAULT '0' COMMENT '被授权主体的类型,可以是项目组, 默认为0,代表单个项目,将来扩展时详细定义',
  `resource_id` int(11) NOT NULL COMMENT '资源id, 对应于resource_registry表中的id字段',
  `allow_method` smallint(5) NOT NULL DEFAULT '15' COMMENT '参考Linux文件权限, 8为读，4为增，2为改, 1为删，如有多个权限，累加。判断是否有某个权限时，比如最终结果为15，15&8 = 8 那么则为有读权限。',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否生效，1为是，0为否',
  `resource_amount` int(11) NOT NULL DEFAULT '1' COMMENT '如果该授权的资源具有数量限制，则为授权数量，默认为1',
  `effective_time` int(10) NOT NULL DEFAULT '0' COMMENT '生效时间，时间戳',
  `expiration_time` int(10) NOT NULL DEFAULT '0' COMMENT '有效时间，时间戳',
  PRIMARY KEY (`id`),
  UNIQUE KEY `authorization_holder` (`authorization_holder`,`resource_name`,`resource_locator`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_authorization`
--

LOCK TABLES `projects_authorization` WRITE;
/*!40000 ALTER TABLE `projects_authorization` DISABLE KEYS */;
INSERT INTO `projects_authorization` VALUES (1,1674191091,'client_user_management','',0,8,15,1,1,1504242095,0),(2,1674191091,'client_wx_management','',0,11,15,1,1,1504242095,0),(3,1674191091,'client_finance_management','',0,9,15,1,1,1504242095,0),(4,1674191091,'client_project_management','',0,7,15,1,1,1504242095,0),(5,1674191091,'client_portal_page_management','',0,10,15,1,1,1504242095,0),(6,1131221010,'client_project_management','',0,7,15,1,1,1504244337,0),(7,1131221010,'client_user_management','',0,8,15,1,1,1504244337,0),(8,1131221010,'client_portal_page_management','',0,10,15,2,1,1504244337,0),(9,1131221010,'client_finance_management','',0,9,15,2,1,1504244337,0),(10,1131221010,'client_wx_management','',0,11,15,2,1,1504244337,0),(11,1253910457,'client_user_management','',0,8,15,1,1,1504249441,0),(12,1253910457,'client_wx_management','',0,11,15,1,1,1504249441,0),(13,1342451022,'client_finance_management','',0,9,15,1,1,1504249909,0),(14,1342451022,'client_user_management','',0,8,15,1,1,1504249909,0),(15,1342451022,'client_portal_page_management','',0,10,15,1,1,1504249909,0),(16,1342451022,'client_project_management','',0,7,15,1,1,1504249909,0),(17,1342451022,'client_wx_management','',0,11,15,1,1,1504249909,0),(18,1316118103,'client_project_management','',0,7,15,1,1,1504253433,0),(19,1316118103,'client_wx_management','',0,11,15,1,1,1504253433,0),(20,1316118103,'client_user_management','',0,8,15,1,1,1504253433,0),(21,1316118103,'client_finance_management','',0,9,15,1,1,1504253433,0),(22,1316118103,'client_portal_page_management','',0,10,15,1,1,1504253433,0),(23,1146852709,'client_wx_management','',0,11,15,1,1,1504255636,0),(24,1146852709,'client_user_management','',0,8,15,1,1,1504255636,0),(25,1146852709,'client_finance_management','',0,9,15,1,1,1504255636,0),(26,1146852709,'client_portal_page_management','',0,10,15,1,1,1504255636,0),(27,1146852709,'client_project_management','',0,7,15,1,1,1504255636,0),(28,1253910457,'client_portal_page_management','',0,10,15,1,1,1504256016,0),(29,1253910457,'client_finance_management','',0,9,15,1,1,1504256016,0),(30,1253910457,'client_project_management','',0,7,15,1,1,1504256016,0),(31,1349800005,'client_finance_management','',0,9,15,1,1,1504490481,0),(32,1349800005,'client_user_management','',0,8,15,1,1,1504490481,0),(33,1349800005,'client_portal_page_management','',0,10,15,1,1,1504490481,0),(34,1349800005,'client_wx_management','',0,11,15,1,1,1504490481,0),(35,1349800005,'client_project_management','',0,7,15,1,1,1504490481,0),(36,1143978008,'client_user_management','',0,8,15,1,1,1504492028,0),(37,1132897105,'client_wx_management','',0,11,15,1,1,1504492795,0),(38,1132897105,'client_project_management','',0,7,15,1,1,1504492795,0),(39,1132897105,'client_user_management','',0,8,15,1,1,1504492795,0),(40,1132897105,'client_finance_management','',0,9,15,1,1,1504492795,0),(41,1132897105,'client_portal_page_management','',0,10,15,1,1,1504492795,0),(42,1535741440,'client_project_management','',0,7,15,1,1,1504573448,0),(43,1535741440,'client_portal_page_management','',0,10,15,1,1,1504573448,0),(44,1535741440,'client_finance_management','',0,9,15,1,1,1504573448,0),(45,1535741440,'client_wx_management','',0,11,15,1,1,1504573448,0),(46,1535741440,'client_user_management','',0,8,15,1,1,1504573448,0),(47,1399911227,'client_user_management','',0,8,15,1,1,1504593855,0),(48,1399911227,'client_finance_management','',0,9,15,1,1,1504593855,0),(49,1399911227,'client_project_management','',0,7,15,1,1,1504593855,0),(50,1399911227,'client_wx_management','',0,11,15,2,1,1504593855,0),(51,1399911227,'client_portal_page_management','',0,10,15,2,1,1504593855,0),(52,1122327156,'client_user_management','',0,8,15,1,1,1504602746,0),(53,1122327156,'client_project_management','',0,7,15,1,1,1504602746,0),(54,1122327156,'client_wx_management','',0,11,15,1,1,1504602746,0),(55,1122327156,'client_portal_page_management','',0,10,15,1,1,1504602746,0),(56,1122327156,'client_finance_management','',0,9,15,1,1,1504602746,0),(57,1441956746,'client_project_management','',0,7,15,1,1,1504602763,0),(58,1410277206,'client_project_management','',0,7,15,1,1,1504663941,0),(59,1410277206,'client_user_management','',0,8,15,1,1,1504663941,0),(60,1410277206,'client_wx_management','',0,11,15,1,1,1504663941,0),(61,1410277206,'client_finance_management','',0,9,15,1,1,1504663941,0),(62,1410277206,'client_portal_page_management','',0,10,15,1,1,1504663941,0),(63,1723055899,'client_project_management','',0,7,15,1,1,1504690241,0),(64,1723055899,'client_user_management','',0,8,15,1,1,1504690241,0),(65,1101310510,'client_finance_management','',0,9,15,1,1,1504762399,0),(66,1101310510,'client_user_management','',0,8,15,1,1,1504762399,0),(67,1101310510,'client_portal_page_management','',0,10,15,1,1,1504762399,0),(68,1101310510,'client_wx_management','',0,11,15,1,1,1504762399,0),(69,1101310510,'client_project_management','',0,7,15,1,1,1504762399,0);
/*!40000 ALTER TABLE `projects_authorization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources_registry`
--

DROP TABLE IF EXISTS `resources_registry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resources_registry` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '资源的注册id，做成自增',
  `resource_type` smallint(5) NOT NULL DEFAULT '0' COMMENT '资源类型，暂时未定义，留待将来使用',
  `public_name` varchar(128) NOT NULL DEFAULT '' COMMENT '资源公有名称，要求全局唯一',
  `private_name` varchar(128) NOT NULL DEFAULT '' COMMENT '资源私有名称，用来拼接uri',
  `description` varchar(256) NOT NULL DEFAULT '0' COMMENT '资源的描述',
  `update_time` datetime,
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否有效，1为是，0为否',
  `ascription` smallint(6) NOT NULL DEFAULT '0' COMMENT '资源归属, 0通用,1为platform的资源,2为client的资源',
  PRIMARY KEY (`id`),
  UNIQUE KEY `KET` (`public_name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources_registry`
--

LOCK TABLES `resources_registry` WRITE;
/*!40000 ALTER TABLE `resources_registry` DISABLE KEYS */;
INSERT INTO `resources_registry` VALUES (1,1,'platform_project_management','项目管理','项目管理','2017-08-31 11:13:59',1,1),(2,1,'platform_user_management','用户管理','用户管理','2017-08-31 11:13:59',1,1),(4,1,'platform_executor_management','账号管理','账号管理','2017-08-31 11:13:59',1,1),(5,1,'platform_finance_management','财务管理','财务管理','2017-08-31 11:13:59',1,1),(6,1,'platform_operation_management','运营管理','运营管理','2017-08-31 11:13:59',1,1),(7,1,'client_project_management','项目管理','项目管理','2017-08-31 11:13:59',1,2),(8,1,'client_user_management','用户管理','用户管理','2017-08-31 11:13:59',1,2),(9,1,'client_finance_management','计费管理','计费管理','2017-08-31 11:13:59',1,2),(10,1,'client_portal_page_management','认证页管理','认证页管理','2017-08-31 11:13:59',1,2),(11,1,'client_wx_management','微信公众号管理','微信公众号管理','2017-08-31 11:13:59',1,2);
/*!40000 ALTER TABLE `resources_registry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources_tree`
--

DROP TABLE IF EXISTS `resources_tree`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resources_tree` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ancestor` int(10) NOT NULL DEFAULT '0' COMMENT '祖先资源id',
  `descendant` int(10) NOT NULL DEFAULT '0' COMMENT '后代资源id',
  `ancestor_name` varchar(64) NOT NULL DEFAULT '' COMMENT '祖先资源名称, private_name, 如果我们的API采用统一的url生成方案, 可以直接根据规则拼接出来',
  `descendant_name` varchar(64) NOT NULL DEFAULT '' COMMENT '后代资源名称, private_name',
  `distance` int(11) NOT NULL COMMENT '祖先到后代在树上的距离',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ancestor_descendant` (`ancestor`,`descendant`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources_tree`
--

LOCK TABLES `resources_tree` WRITE;
/*!40000 ALTER TABLE `resources_tree` DISABLE KEYS */;
/*!40000 ALTER TABLE `resources_tree` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-11  9:56:14
