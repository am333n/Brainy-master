/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - brainseg
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`brainseg` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `brainseg`;

/*Table structure for table `appointment` */

DROP TABLE IF EXISTS `appointment`;

CREATE TABLE `appointment` (
  `appointmentid` int(100) NOT NULL AUTO_INCREMENT,
  `userid` int(100) DEFAULT NULL,
  `scheduleid` int(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`appointmentid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;

/*Data for the table `appointment` */

insert  into `appointment`(`appointmentid`,`userid`,`scheduleid`,`date`,`status`) values 
(2,19,10,'2023-01-17','Pending'),
(3,0,0,'0000-00-00','Pending'),
(4,19,14,'2023-03-02','Consulted'),
(5,17,14,'2023-03-02','Pending'),
(6,17,14,'2023-03-02','Pending'),
(15,21,14,'2023-03-03','Consulted'),
(16,17,14,'2023-03-03','Pending'),
(18,21,15,'2023-03-03','Consulted'),
(19,21,16,'2023-03-03','Consulted'),
(20,21,14,'2023-03-05','Consulted'),
(21,21,13,'2023-03-05','Consulted'),
(22,21,14,'2023-03-05','Consulted'),
(23,21,15,'2023-03-05','Consulted'),
(24,21,13,'2023-03-23','Pending'),
(25,24,17,'2023-03-28','Consulted'),
(26,24,14,'2023-03-28','Consulted'),
(27,17,14,'2023-03-31','Pending'),
(28,24,13,'2023-04-01','Pending'),
(29,24,14,'2023-04-12','Pending'),
(30,24,17,'2023-04-12','Consulted');

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`chat_id`,`date`,`time`,`from_id`,`to_id`,`message`) values 
(1,'2023-03-23','04:05:42',0,10,'fsdfsdf sdf sdf sdf sd fsdf sdf sdf sd'),
(2,'2023-03-23','04:05:50',0,10,'sdf d fsd fsdf s fsd fsd fsd fsd fsd fsd fsd fsd fsdf s'),
(3,'2023-03-23','04:09:18',21,10,'gdfgsdfgfsxhfg hfg hfg hfg hf'),
(4,'2023-03-23','04:09:23',21,11,'fghfgh fg h'),
(5,'2023-03-23','04:09:27',21,12,'hfghf g'),
(6,'2023-03-23','04:13:15',21,0,'sdfsdfsdfs'),
(7,'2023-03-23','04:13:19',21,0,'fsdfsdfsd'),
(8,'2023-03-23','04:13:21',21,0,'fsdfsdfsd'),
(9,'2023-03-23','04:14:59',22,19,'dfgdfgdf'),
(10,'2023-03-23','04:15:05',22,21,'gdfgdfgdfgdfgdf'),
(11,'2023-03-23','04:16:10',22,19,'fgdfgdfgdf'),
(12,'2023-03-23','04:16:15',22,21,'dfgdfgdfgdfgdf'),
(13,'2023-03-23','04:16:18',22,21,'fgdfgfgdf'),
(14,'2023-03-23','04:16:24',22,19,'fdgdfgdfg  dfg df gdf gdf'),
(15,'2023-03-23','04:16:28',22,21,'dfgdf df gdf gdf g'),
(16,'2023-03-28','02:49:14',12,24,'hi'),
(17,'2023-03-28','02:50:49',12,0,'hi'),
(18,'2023-03-28','03:03:58',23,24,'hi'),
(19,'2023-04-01','00:19:22',23,19,'hi'),
(20,'2023-04-01','01:39:54',24,0,'hi'),
(21,'2023-04-01','01:41:28',12,24,'enthella'),
(22,'2023-04-01','02:33:29',24,0,'by'),
(23,'2023-04-01','02:34:17',12,24,'hi'),
(24,'2023-04-01','02:34:37',12,24,'kkkkkkkkk'),
(25,'2023-04-01','02:36:13',24,0,'mmmmm'),
(26,'2023-04-01','02:37:44',12,24,'Test'),
(27,'2023-04-01','02:39:16',24,0,'Test'),
(28,'2023-04-01','02:40:28',24,12,'Ok'),
(29,'2023-04-01','02:41:40',24,12,'by'),
(30,'2023-04-01','02:42:20',24,12,'tesss'),
(31,'2023-04-01','02:43:03',12,24,'afnas'),
(32,'2023-04-01','02:43:31',24,12,'jamal'),
(33,'2023-04-01','02:44:11',12,24,'Tres'),
(34,'2023-04-01','02:45:49',12,19,'hloo'),
(35,'2023-04-01','02:46:30',17,12,'rijass'),
(36,'2023-04-01','02:49:56',25,24,'aaaaaaaaa'),
(37,'2023-04-01','02:50:34',24,25,'eeeeeeeeee'),
(38,'2023-04-03','00:39:25',10,21,'hello'),
(39,'2023-04-03','00:39:33',10,21,'hi'),
(40,'2023-04-12','11:44:18',24,12,'hi'),
(41,'2023-04-12','11:44:23',24,12,'hi'),
(42,'2023-04-12','11:44:28',24,12,'hi'),
(43,'2023-04-12','11:45:21',12,24,'helo');

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaintid` int(100) NOT NULL AUTO_INCREMENT,
  `userid` int(100) DEFAULT NULL,
  `doctorid` int(100) DEFAULT NULL,
  `complaint` varchar(500) DEFAULT NULL,
  `reply` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `cmpstatus` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`complaintid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`complaintid`,`userid`,`doctorid`,`complaint`,`reply`,`date`,`cmpstatus`) values 
(1,7,8,'bad service','sorry for the inconvineince we will try our best','2022-12-14','replied'),
(2,7,8,'ok ','sorry','2022-12-27','replied'),
(3,24,28,'Testing','pending','2023-04-01','pending'),
(4,24,28,'hi all','pending','2023-04-01','pending'),
(5,24,28,'hi all by','pending','2023-04-01','pending'),
(6,24,9,'dfsef','pending','2023-04-01','pending'),
(7,24,11,'Test','ok','2023-04-01','replied'),
(8,24,11,'gggggg','kkkk','2023-04-01','replied'),
(9,24,11,'1234','pending','2023-04-03','pending');

/*Table structure for table `disease` */

DROP TABLE IF EXISTS `disease`;

CREATE TABLE `disease` (
  `diseaseid` int(100) NOT NULL AUTO_INCREMENT,
  `disease_name` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`diseaseid`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

/*Data for the table `disease` */

insert  into `disease`(`diseaseid`,`disease_name`,`description`) values 
(13,'chickenpox','virus'),
(15,'corona ','virus'),
(16,'jaundice','bacteria'),
(18,'malaria','bacteria\r\n'),
(19,'allergies','immunity\r\n');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `doctorid` int(25) NOT NULL AUTO_INCREMENT,
  `doctor_lid` int(25) DEFAULT NULL,
  `doctorname` varchar(40) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `house` varchar(150) DEFAULT NULL,
  `place` varchar(150) DEFAULT NULL,
  `post` varchar(150) DEFAULT NULL,
  `pin` int(6) DEFAULT NULL,
  `district` varchar(150) DEFAULT NULL,
  `state` varchar(150) DEFAULT NULL,
  `phone` bigint(13) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `qualification` varchar(150) DEFAULT NULL,
  `experience` varchar(150) DEFAULT NULL,
  `drstatus` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`doctorid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `doctor` */

insert  into `doctor`(`doctorid`,`doctor_lid`,`doctorname`,`dob`,`gender`,`photo`,`house`,`place`,`post`,`pin`,`district`,`state`,`phone`,`email`,`qualification`,`experience`,`drstatus`) values 
(8,10,'baburaj','2022-12-28','Female','/static/doctor/20230303-164644.jpg','nholayil','kadavathur','kadavathur',673542,'Vadakara/kadavathur','Kerala',0,'afnasnholayil@gmail.com','md, mbbs, llb, btech ','10','approved'),
(9,11,'shashi m','2022-12-05','Other','/static/doctor/20221227-231527.jpg','mangalasseri','vadakara','vadakara',25000,'Vadakara/kadavathur','Kerala',123456789,'gmail@gmail.com','mbbs,bca,MCa ,btech  ','3','approved'),
(10,12,'Rijas','2022-12-05','Female','/static/doctor/20221227-145752.jpg','gulaan parambath','banyel','banyel',673548,'Kozhikode','Bihar',8590123456,'rijas@gmail.com','bca 12','0','approved'),
(12,23,'sample Doctor','2023-03-02','Male','/static/doctor/20230328-113455.jpg','sample house','sample place','sample post',786567,'Kozhikode','Kerala',9090909090,'sampledoctor@gmail.com','mbbs in general','2','pending'),
(13,25,'aaa','2222-09-12','Male','/static/doctor/20230401-151934.jpg','aaaaaaa','aaaaa','aaa',222,'Kozhikode','Manipur',1231423424,'aaaaa.@123','12','12','pending');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedbackid` int(100) NOT NULL AUTO_INCREMENT,
  `doctorid` int(100) DEFAULT NULL,
  `userid` int(100) DEFAULT NULL,
  `feedback` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `appointmentid` int(100) DEFAULT NULL,
  PRIMARY KEY (`feedbackid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedbackid`,`doctorid`,`userid`,`feedback`,`date`,`appointmentid`) values 
(13,10,21,'qwfefe','2023-03-05',15),
(14,12,24,'sample feedback','2023-03-28',25),
(15,12,24,'hi all','2023-04-01',25),
(16,10,24,'mosham','2023-04-01',26);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `loginid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(25) DEFAULT NULL,
  `type` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`loginid`,`username`,`password`,`type`) values 
(1,'admin@gmail.com','admin','admin'),
(3,'tomas123','1234','doctor'),
(8,'mpc','123','patient'),
(10,'babu','babu','doctor'),
(11,'sase','sase','doctor'),
(12,'rijas','rijas','doctor'),
(17,'afnas','afnas','patient'),
(20,'rijas','rijass','patient'),
(21,'jamal','jamal','patient'),
(22,'fahid','fahid','doctor'),
(23,'sampleusername','123456789','doctor'),
(24,'sample patient','123456789','patient'),
(25,'aaa','aaaa','doctor');

/*Table structure for table `prescription` */

DROP TABLE IF EXISTS `prescription`;

CREATE TABLE `prescription` (
  `prescriptionid` int(100) NOT NULL AUTO_INCREMENT,
  `Findings` varchar(500) DEFAULT NULL,
  `prescription` varchar(500) DEFAULT NULL,
  `appointmentid` int(100) DEFAULT NULL,
  PRIMARY KEY (`prescriptionid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `prescription` */

insert  into `prescription`(`prescriptionid`,`Findings`,`prescription`,`appointmentid`) values 
(1,'valare mosham','pora',2),
(2,'3rg4rg','5gtb',0),
(3,'rgerg','rgrbr',4),
(4,'2 penadol\r\n3 borax\r\n2\r\nuranium','manja pitham',19),
(5,'ceve','evevev',21),
(6,'1 paracetomol a day','you have serious issues\r\n',25),
(7,'ffsdgsdg','dgdsfhs',26),
(8,'asdfghj','asdfghjk',30);

/*Table structure for table `review` */

DROP TABLE IF EXISTS `review`;

CREATE TABLE `review` (
  `reviewid` int(100) NOT NULL AUTO_INCREMENT,
  `userid` int(100) DEFAULT NULL,
  `doctorid` int(100) DEFAULT NULL,
  `reviewstar` int(5) DEFAULT NULL,
  `review` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`reviewid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `review` */

insert  into `review`(`reviewid`,`userid`,`doctorid`,`reviewstar`,`review`,`date`) values 
(1,5,9,3,'nice doctor , very friendly','2022-12-19'),
(2,24,10,1,'aert','2023-04-01'),
(3,24,10,5,'huh','2023-04-01'),
(4,24,10,2,'efef','2023-04-01'),
(5,24,10,5,'goood','2023-04-01'),
(6,24,11,3,'goog','2023-04-01'),
(7,24,12,4,'very bad','2023-04-01');

/*Table structure for table `schedule` */

DROP TABLE IF EXISTS `schedule`;

CREATE TABLE `schedule` (
  `scheduleid` int(100) NOT NULL AUTO_INCREMENT,
  `doctorid` int(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `starttime` time DEFAULT NULL,
  `endtime` time DEFAULT NULL,
  `prescriptionid` int(100) DEFAULT NULL,
  PRIMARY KEY (`scheduleid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

/*Data for the table `schedule` */

insert  into `schedule`(`scheduleid`,`doctorid`,`date`,`starttime`,`endtime`,`prescriptionid`) values 
(13,11,'2022-12-30','16:55:00','18:55:00',NULL),
(14,10,'2023-03-15','11:58:00','23:58:00',NULL),
(15,10,'2023-03-14','11:00:00','23:59:00',NULL),
(16,10,'2023-03-03','17:00:00','02:30:00',NULL),
(17,12,'2023-03-29','16:00:00','19:00:00',NULL),
(18,23,'2222-12-12','10:10:00','10:50:00',NULL);

/*Table structure for table `symptoms` */

DROP TABLE IF EXISTS `symptoms`;

CREATE TABLE `symptoms` (
  `symptomid` int(100) NOT NULL AUTO_INCREMENT,
  `symptom` varchar(500) DEFAULT NULL,
  `diseaseid` int(100) DEFAULT NULL,
  PRIMARY KEY (`symptomid`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

/*Data for the table `symptoms` */

insert  into `symptoms`(`symptomid`,`symptom`,`diseaseid`) values 
(1,NULL,NULL),
(3,'mook olipp , vayar vedhana',2),
(4,'thummal, thalavedhana',3),
(10,'temp,\r\ndiarria',9),
(13,'cough',14),
(14,'itchy skin\r\n',13),
(15,'fever',12),
(16,'fever , cough',15),
(17,'yellow skin',16),
(18,'tumor',17),
(19,'cough,fever',18);

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `userid` int(100) NOT NULL AUTO_INCREMENT,
  `user_lid` int(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `house` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pin` int(6) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `phone` bigint(13) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`userid`,`user_lid`,`username`,`dob`,`gender`,`photo`,`house`,`place`,`post`,`pin`,`district`,`state`,`phone`,`email`) values 
(7,19,'afnas','2022-12-07','Male','/static/patient/20221227-235744.jpg','najath','nholayil','kadavathur',0,'Kannur','Bihar',123456789,'gmail@gmail.com'),
(9,21,'jamal','2023-03-14','Other','/static/patient/20230302-151410.jpg','Makki Kandi','kolachi peediya','kadavathur',670676,'Kozhikode','Bihar',9026434512,'jamalmakki@gmail.com'),
(10,24,'sample patient','2023-03-02','Male','/static/patient/20230328-143902.jpg','sample hosue','sample place','sample post',879788,'Kannur','Kerala',9877890988,'samplpatient@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
