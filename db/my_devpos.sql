/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50703
Source Host           : 127.0.0.1:3306
Source Database       : my_devpos

Target Server Type    : MYSQL
Target Server Version : 50703
File Encoding         : 65001

Date: 2018-11-28 10:00:01
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
INSERT INTO `auth_group` VALUES ('1', '查看');
INSERT INTO `auth_group` VALUES ('5', '添加');
INSERT INTO `auth_group` VALUES ('4', '编辑');
INSERT INTO `auth_group` VALUES ('3', '超级管理员');

-- ----------------------------
-- Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
INSERT INTO `auth_group_permissions` VALUES ('1', '1', '22');
INSERT INTO `auth_group_permissions` VALUES ('6', '3', '22');
INSERT INTO `auth_group_permissions` VALUES ('7', '3', '23');
INSERT INTO `auth_group_permissions` VALUES ('4', '3', '24');
INSERT INTO `auth_group_permissions` VALUES ('5', '3', '25');
INSERT INTO `auth_group_permissions` VALUES ('10', '4', '22');
INSERT INTO `auth_group_permissions` VALUES ('11', '4', '23');
INSERT INTO `auth_group_permissions` VALUES ('8', '4', '24');
INSERT INTO `auth_group_permissions` VALUES ('9', '4', '25');
INSERT INTO `auth_group_permissions` VALUES ('12', '5', '23');

-- ----------------------------
-- Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add user', '3', 'add_user');
INSERT INTO `auth_permission` VALUES ('8', 'Can change user', '3', 'change_user');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete user', '3', 'delete_user');
INSERT INTO `auth_permission` VALUES ('10', 'Can add group', '4', 'add_group');
INSERT INTO `auth_permission` VALUES ('11', 'Can change group', '4', 'change_group');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete group', '4', 'delete_group');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('17', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete session', '6', 'delete_session');
INSERT INTO `auth_permission` VALUES ('19', 'Can add quanxian', '7', 'add_quanxian');
INSERT INTO `auth_permission` VALUES ('20', 'Can change quanxian', '7', 'change_quanxian');
INSERT INTO `auth_permission` VALUES ('21', 'Can delete quanxian', '7', 'delete_quanxian');
INSERT INTO `auth_permission` VALUES ('22', '查看', '7', 'can_view');
INSERT INTO `auth_permission` VALUES ('23', '添加', '7', 'can_add');
INSERT INTO `auth_permission` VALUES ('24', '编辑', '7', 'can_edit');
INSERT INTO `auth_permission` VALUES ('25', '删除', '7', 'can_delete');
INSERT INTO `auth_permission` VALUES ('26', '超级', '7', 'can_super');

-- ----------------------------
-- Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES ('2', 'pbkdf2_sha256$120000$vC4LqeuPSiTP$QUgLuPjMR413BxAJDfRKyQqrc0K00bbwmGHADXuBQt8=', '2018-11-02 10:06:41.845773', '1', '12345', '', '', '123@123.com', '0', '1', '2018-01-04 06:26:40.000000');
INSERT INTO `auth_user` VALUES ('6', 'pbkdf2_sha256$30000$zyxrCI8GUNUN$U2PJB8GrXaCNmpsXnBMp4TI9+ykXAe6Ae03hjmsaa9U=', '2018-01-10 17:49:07.199684', '0', 'test3', '', '', '', '0', '1', '2018-01-04 07:15:07.000000');
INSERT INTO `auth_user` VALUES ('8', 'pbkdf2_sha256$120000$0wxdnNmiQW5r$PdZHrZHG1CE0xC7ka8+xS0uZLVxESJ8hRJs4eM6VPWY=', '2018-11-28 09:50:18.599482', '1', 'root', 'a', 'a', '123@123.com', '1', '1', '2018-01-04 07:15:22.000000');
INSERT INTO `auth_user` VALUES ('9', 'pbkdf2_sha256$120000$0wxdnNmiQW5r$PdZHrZHG1CE0xC7ka8+xS0uZLVxESJ8hRJs4eM6VPWY=', null, '0', 'test1', '', '', '', '0', '1', '2018-11-26 16:46:56.101839');

-- ----------------------------
-- Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
INSERT INTO `auth_user_groups` VALUES ('1', '2', '3');
INSERT INTO `auth_user_groups` VALUES ('8', '6', '4');

-- ----------------------------
-- Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for `device_status`
-- ----------------------------
DROP TABLE IF EXISTS `device_status`;
CREATE TABLE `device_status` (
  `ip` varchar(20) NOT NULL,
  `cpu` varchar(20) DEFAULT NULL,
  `memory` varchar(20) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `product` varchar(50) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `sn` varchar(50) DEFAULT NULL,
  `Createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of device_status
-- ----------------------------
INSERT INTO `device_status` VALUES ('172.17.0.3', '12', '32', '上海洚', 's', 'linux', '1', '2017-08-08 17:17:41', '2017-08-08 17:17:41');
INSERT INTO `device_status` VALUES ('172.17.0.4', '12', '32', '武汉', 'Intel', 'linux', '2', '2017-08-08 17:09:31', '2017-08-08 17:09:31');
INSERT INTO `device_status` VALUES ('172.17.0.5', '12', '12', '美国日本', 'X86', 'wiodows', '3', '2017-08-08 17:18:53', '2017-08-08 17:18:53');
INSERT INTO `device_status` VALUES ('172.17.0.6', '12', '24', '香港', 'P50', 'wiodows', '4', '2017-08-08 17:09:41', '2017-08-08 17:09:41');
INSERT INTO `device_status` VALUES ('192.168.153.135', '12', '64', '英国', null, 'wiodows', null, '2017-08-08 10:34:05', '2017-08-08 10:34:05');

-- ----------------------------
-- Table structure for `disk_usage`
-- ----------------------------
DROP TABLE IF EXISTS `disk_usage`;
CREATE TABLE `disk_usage` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) DEFAULT NULL,
  `minion_id` varchar(40) DEFAULT NULL,
  `partition` varchar(20) DEFAULT NULL,
  `total` varchar(20) DEFAULT NULL,
  `used` varchar(20) DEFAULT NULL,
  `available` varchar(20) DEFAULT NULL,
  `capacity` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of disk_usage
-- ----------------------------
INSERT INTO `disk_usage` VALUES ('1', '192.168.153.136', 'windows10_app', 'D:\\', '383519712', '213231132', '170288580', '56%');
INSERT INTO `disk_usage` VALUES ('2', '192.168.153.136', 'windows10_app', 'C:\\', '104864252', '71704556', '33159696', '68%');
INSERT INTO `disk_usage` VALUES ('3', '172.17.39.96', '172.17.39.96_web1_centos7_2', 'tmpfs', '501580', '7220', '494360', '2%');
INSERT INTO `disk_usage` VALUES ('4', '172.17.39.96', '172.17.39.96_web1_centos7_2', 'tmpfs', '501580', '152', '501428', '1%');
INSERT INTO `disk_usage` VALUES ('5', '172.17.39.96', '172.17.39.96_web1_centos7_2', '/dev/sda1', '303788', '113236', '190552', '38%');
INSERT INTO `disk_usage` VALUES ('6', '172.17.39.96', '172.17.39.96_web1_centos7_2', '/dev/sr1', '4209322', '4209322', '0', '100%');
INSERT INTO `disk_usage` VALUES ('7', '172.17.39.96', '172.17.39.96_web1_centos7_2', '/dev/sda3', '18555904', '3878532', '14677372', '21%');
INSERT INTO `disk_usage` VALUES ('8', '172.17.39.96', '172.17.39.96_web1_centos7_2', 'tmpfs', '501580', '0', '501580', '0%');
INSERT INTO `disk_usage` VALUES ('9', '172.17.39.96', '172.17.39.96_web1_centos7_2', '/dev/sr0', '54530', '54530', '0', '100%');
INSERT INTO `disk_usage` VALUES ('10', '172.17.39.96', '172.17.39.96_web1_centos7_2', 'devtmpfs', '492548', '0', '492548', '0%');
INSERT INTO `disk_usage` VALUES ('11', 'sss', 'windows10_app', 'D:\\', '383519712', '214161040', '169358672', '56%');
INSERT INTO `disk_usage` VALUES ('12', 'sss', 'windows10_app', 'C:\\', '104864252', '71814256', '33049996', '68%');
INSERT INTO `disk_usage` VALUES ('13', '172.17.39.208', '172.17.39.208_windows10_app', 'F:\\', null, null, null, null);
INSERT INTO `disk_usage` VALUES ('14', '172.17.39.208', '172.17.39.208_windows10_app', 'D:\\', '383519712', '214147008', '169372704', '56%');
INSERT INTO `disk_usage` VALUES ('15', '172.17.39.208', '172.17.39.208_windows10_app', 'C:\\', '104864252', '70135024', '34729228', '67%');
INSERT INTO `disk_usage` VALUES ('16', '172.17.39.2089', '172.17.39.208_windows10_app', 'C:\\', '104864252', '75892584', '28971668', '72%');
INSERT INTO `disk_usage` VALUES ('17', '172.17.39.2089', '172.17.39.208_windows10_app', 'F:\\', null, null, null, null);
INSERT INTO `disk_usage` VALUES ('18', '172.17.39.2089', '172.17.39.208_windows10_app', 'D:\\', '383519712', '224947648', '158572064', '59%');
INSERT INTO `disk_usage` VALUES ('19', '192.168.213.129', 'windows', 'E:\\', '395244540', '146540264', '248704276', '37%');
INSERT INTO `disk_usage` VALUES ('20', '192.168.213.129', 'windows', 'C:\\', '104034532', '57029072', '47005460', '55%');
INSERT INTO `disk_usage` VALUES ('21', '192.168.1.11', 'windows', 'E:\\', '395244540', '156912112', '238332428', '40%');
INSERT INTO `disk_usage` VALUES ('22', '192.168.1.11', 'windows', 'C:\\', '104034532', '60791140', '43243392', '58%');
INSERT INTO `disk_usage` VALUES ('23', '192.168.216.129', '192.168.168.129_web1', 'tmpfs', '949068', '92', '948976', '1%');
INSERT INTO `disk_usage` VALUES ('24', '192.168.216.129', '192.168.168.129_web1', '/dev/dm-1', '10474496', '148752', '10325744', '2%');
INSERT INTO `disk_usage` VALUES ('25', '192.168.216.129', '192.168.168.129_web1', 'devtmpfs', '940036', '0', '940036', '0%');
INSERT INTO `disk_usage` VALUES ('26', '192.168.216.129', '192.168.168.129_web1', '/dev/sda1', '303788', '114244', '189544', '38%');
INSERT INTO `disk_usage` VALUES ('27', '192.168.216.129', '192.168.168.129_web1', 'tmpfs', '949068', '92', '948976', '1%');
INSERT INTO `disk_usage` VALUES ('28', '192.168.216.129', '192.168.168.129_web1', '/dev/sda3', '18555904', '15426580', '3129324', '84%');
INSERT INTO `disk_usage` VALUES ('29', '192.168.216.129', '192.168.168.129_web1', 'tmpfs', '949068', '92', '948976', '1%');
INSERT INTO `disk_usage` VALUES ('30', '192.168.216.129', '192.168.168.129_web1', 'shm', '65536', '0', '65536', '0%');
INSERT INTO `disk_usage` VALUES ('31', '192.168.216.129', '192.168.168.129_web1', 'tmpfs', '949068', '92', '948976', '1%');
INSERT INTO `disk_usage` VALUES ('32', '192.168.216.129', '192.168.168.129_web1', 'shm', '65536', '0', '65536', '0%');
INSERT INTO `disk_usage` VALUES ('33', '192.168.216.129', '192.168.168.129_web1', '/dev/dm-2', '10474496', '148752', '10325744', '2%');
INSERT INTO `disk_usage` VALUES ('34', '192.168.216.129', '192.168.168.129_web1', 'tmpfs', '949068', '92', '948976', '1%');
INSERT INTO `disk_usage` VALUES ('35', '999', 'windows', 'E:\\', '395244540', '156942928', '238301612', '40%');
INSERT INTO `disk_usage` VALUES ('36', '999', 'windows', 'C:\\', '104034532', '60931092', '43103440', '59%');

-- ----------------------------
-- Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES ('1', '2018-01-04 06:56:02.010252', '2', 'admin', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('2', '2018-01-04 06:56:22.695182', '1', 'root', '3', '', '3', '2');
INSERT INTO `django_admin_log` VALUES ('3', '2018-01-04 06:56:28.853660', '2', 'admin', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('4', '2018-01-04 06:56:50.992983', '3', 'root', '1', '[{\"added\": {}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('5', '2018-01-04 07:09:58.516097', '1', '普通用户', '1', '[{\"added\": {}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('6', '2018-01-04 07:10:22.150829', '2', '普通管理员', '1', '[{\"added\": {}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('7', '2018-01-04 07:10:43.014422', '3', '超级管理员', '1', '[{\"added\": {}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('8', '2018-01-04 07:11:36.806793', '1', '普通用户', '2', '[]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('9', '2018-01-04 07:12:30.847168', '3', 'root', '2', '[{\"changed\": {\"fields\": [\"is_staff\", \"is_superuser\"]}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('10', '2018-01-04 07:14:16.960435', '2', 'admin', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('11', '2018-01-04 07:14:37.581642', '4', 'TEST1', '1', '[{\"added\": {}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('12', '2018-01-04 07:14:45.778287', '5', 'test2', '1', '[{\"added\": {}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('13', '2018-01-04 07:15:07.228778', '6', 'test3', '1', '[{\"added\": {}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('14', '2018-01-04 07:16:05.892997', '4', 'TEST1', '2', '[{\"changed\": {\"fields\": [\"is_active\"]}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('15', '2018-01-04 07:16:30.075243', '4', 'TEST1', '2', '[{\"changed\": {\"fields\": [\"is_active\"]}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('16', '2018-01-04 07:16:37.722700', '5', 'test2', '2', '[{\"changed\": {\"fields\": [\"is_active\"]}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('17', '2018-01-04 07:16:52.200660', '4', 'TEST1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('18', '2018-01-04 07:17:54.314787', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('19', '2018-01-04 07:18:27.248679', '4', 'TEST1', '2', '[{\"changed\": {\"fields\": [\"is_active\"]}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('20', '2018-01-04 07:18:32.043080', '4', 'TEST1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('21', '2018-01-04 07:19:12.977064', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('22', '2018-01-04 07:19:35.998096', '6', 'test3', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('23', '2018-01-04 07:22:14.037452', '4', 'TEST1', '2', '[{\"changed\": {\"fields\": [\"is_active\"]}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('24', '2018-01-04 07:22:21.988790', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('25', '2018-01-04 07:22:28.397344', '6', 'test3', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('26', '2018-01-04 07:29:44.499291', '4', 'TEST1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('27', '2018-01-04 07:29:52.235633', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('28', '2018-01-04 07:31:24.382106', '4', 'TEST1', '3', '', '3', '2');
INSERT INTO `django_admin_log` VALUES ('29', '2018-01-04 07:31:36.160543', '7', 'test1', '1', '[{\"added\": {}}]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('30', '2018-01-04 07:31:47.434916', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('31', '2018-01-04 07:33:17.754049', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('32', '2018-01-04 07:34:08.561710', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('33', '2018-01-05 09:25:07.183790', '6', 'test3', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('34', '2018-01-05 09:29:21.870833', '2', 'admin', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('35', '2018-01-08 08:54:43.198386', '4', '空权限', '1', '[{\"added\": {}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('36', '2018-01-08 08:54:59.669615', '6', 'test3', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('37', '2018-01-08 08:55:05.399976', '6', 'test3', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('38', '2018-01-08 08:56:44.417804', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('39', '2018-01-09 03:20:13.240524', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('40', '2018-01-09 03:20:40.037830', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('41', '2018-01-09 03:21:10.622722', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('42', '2018-01-09 03:21:36.224009', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('43', '2018-01-09 03:21:52.811467', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('44', '2018-01-09 03:53:08.168779', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('45', '2018-01-09 03:53:15.627353', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('46', '2018-01-09 03:59:33.104397', '1', '查看', '2', '[{\"changed\": {\"fields\": [\"name\"]}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('47', '2018-01-09 03:59:41.503437', '2', '添加', '2', '[{\"changed\": {\"fields\": [\"name\"]}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('48', '2018-01-09 03:59:55.879994', '4', '编辑', '2', '[{\"changed\": {\"fields\": [\"name\"]}}]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('49', '2018-01-09 04:00:05.028736', '3', '超级管理员', '2', '[]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('50', '2018-01-09 04:00:15.717554', '7', 'test1', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('51', '2018-01-09 04:00:26.689512', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('52', '2018-01-09 04:00:41.456157', '6', 'test3', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('53', '2018-01-09 04:06:52.408919', '2', '添加', '3', '', '4', '2');
INSERT INTO `django_admin_log` VALUES ('54', '2018-01-09 04:07:07.704185', '4', '编辑', '2', '[]', '4', '2');
INSERT INTO `django_admin_log` VALUES ('55', '2018-01-09 04:07:25.631639', '5', 'test2', '2', '[]', '3', '2');
INSERT INTO `django_admin_log` VALUES ('56', '2018-01-09 04:07:49.403740', '5', '添加', '1', '[{\"added\": {}}]', '4', '2');

-- ----------------------------
-- Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('7', 'login', 'quanxian');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2018-01-04 04:16:37.227984');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2018-01-04 04:16:55.199050');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2018-01-04 04:16:58.764389');
INSERT INTO `django_migrations` VALUES ('4', 'admin', '0002_logentry_remove_auto_add', '2018-01-04 04:16:58.904633');
INSERT INTO `django_migrations` VALUES ('5', 'contenttypes', '0002_remove_content_type_name', '2018-01-04 04:17:00.806681');
INSERT INTO `django_migrations` VALUES ('6', 'auth', '0002_alter_permission_name_max_length', '2018-01-04 04:17:01.975915');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0003_alter_user_email_max_length', '2018-01-04 04:17:02.996208');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0004_alter_user_username_opts', '2018-01-04 04:17:03.040385');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0005_alter_user_last_login_null', '2018-01-04 04:17:03.972657');
INSERT INTO `django_migrations` VALUES ('10', 'auth', '0006_require_contenttypes_0002', '2018-01-04 04:17:04.036001');
INSERT INTO `django_migrations` VALUES ('11', 'auth', '0007_alter_validators_add_error_messages', '2018-01-04 04:17:04.103416');
INSERT INTO `django_migrations` VALUES ('12', 'auth', '0008_alter_user_username_max_length', '2018-01-04 04:17:05.085805');
INSERT INTO `django_migrations` VALUES ('13', 'sessions', '0001_initial', '2018-01-04 04:17:06.201027');
INSERT INTO `django_migrations` VALUES ('14', 'login', '0001_initial', '2018-01-04 07:04:33.451848');
INSERT INTO `django_migrations` VALUES ('15', 'login', '0002_auto_20180112_1735', '2018-01-12 17:37:12.251685');

-- ----------------------------
-- Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('00wd89pplhvag9bd5nqy9i6zhfqrddt6', 'MWQwY2U2MTdmY2ZjYzRkNDRkYzA5OGJjZTgxMDMyYzg5MGU2MGFmZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOiJ0ZXN0MiIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTU6MzU6MTFcIiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 15:45:14.422817');
INSERT INTO `django_session` VALUES ('06j6m9u2yh9pm12o71kpeuhk3vvtevpl', 'OGM5OGZkZjM1ZGFmNjBkZTFiM2UwYmI2Mzk3MDYxMDVlZjRjZTg0NTp7Il9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJ1c2VyaWQiOiJ0ZXN0MiIsIl9hdXRoX3VzZXJfaWQiOiI1Iiwic2Vzc2lvbl90eHQiOnsibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAwOTo1MTo1OFwiIiwidXNlcm5hbWUiOiJ0ZXN0MiIsInVzZXJpZCI6NSwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In19', '2018-01-11 10:18:25.325819');
INSERT INTO `django_session` VALUES ('0e47v1qa99nbwti9680dbxqcie0x4q2t', 'MzJjYWVkMWRhOWYzOWUxYTk2YmJmZDA5MWM5ZDZjMmQzM2I5ZWRlMTp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMCAxNDo1NzoyNlwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-20 18:19:37.102302');
INSERT INTO `django_session` VALUES ('10r4e6ig0xyspnkpsef52zdvec53r02z', 'M2VjZTAyMTg4NzcyYTZkZmM2MmE5MThiNjdiYzUwZjBhMmQ4NjgwYjp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMiAxNDoxMTowMlwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-23 12:44:02.359785');
INSERT INTO `django_session` VALUES ('1e0znt4eau24ybpfihb9fxg4ia2yghei', 'Njg0YmJkZjUwNTBmMjVhNWJmZTI2YTc1YzM4OWYwNDhjYjcxMDE4OTp7InVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsIl9hdXRoX3VzZXJfaWQiOiI1IiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2Iiwic2Vzc2lvbl90eHQiOnsidXNlcmlkIjo1LCJsYXN0X2xvZ2luIjoiXCIyMDE4LTAxLTExIDExOjU2OjU4XCIiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJ1c2VybmFtZSI6InRlc3QyIn19', '2018-01-11 12:17:55.373970');
INSERT INTO `django_session` VALUES ('2vdzohlrpob6y2m5k72xw4e9fme4xauy', 'NDM1NTVjMThkYmVhMDM3MWI0ZDYyODIyODdlMmE3ODgzNWE2MWY4Yzp7Il9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfYXV0aF91c2VyX2lkIjoiNSIsInVzZXJpZCI6InRlc3QyIiwic2Vzc2lvbl90eHQiOnsibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxNDoxNjo0OVwiIiwidXNlcmlkIjo1LCJ1c2VybmFtZSI6InRlc3QyIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2018-01-12 14:43:17.680941');
INSERT INTO `django_session` VALUES ('344d7qgh3ouynxfq6qymlustufwdwng4', 'ZjcxYTgyNDU2YjQ2ZTI1NzZmYTIyYzYxNzA0YWM3ZjZhOGNhYzA1Mzp7Il9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsInNlc3Npb25fdHh0Ijp7InBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJuYW1lIjoidGVzdDIiLCJ1c2VyaWQiOjUsImxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTIgMTI6MjQ6MTNcIiJ9LCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-12 14:09:32.844294');
INSERT INTO `django_session` VALUES ('3s3p4lhdsggk6komyy5kxeli9giw2rkv', 'MGRmNDg2ZjM1ZTc5MTBkNmY3ZDAwMjUwZWIxODhlMWE3MDc1M2QxZTp7InVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI1Iiwic2Vzc2lvbl90eHQiOnsidXNlcmlkIjo1LCJ1c2VybmFtZSI6InRlc3QyIiwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxMTo0OTo1OFwiIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyJ9', '2018-01-12 12:17:00.433536');
INSERT INTO `django_session` VALUES ('4jgnlgtpau2438azoqahahmpslxhj3oj', 'YTZiNjY5NWJjNTM3ZGI2OWI1MDJlNDYyNTU2OWNmNTdkMGFhZmNmYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTIgMTA6MzE6MTFcIiIsInVzZXJuYW1lIjoidGVzdDIiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOjV9LCJfYXV0aF91c2VyX2hhc2giOiJhNDY5OTgwZTZiNGMyZWExZDc1MmIwMTZkMjQ1YzMxZTcxZmMyNTQ3IiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-12 10:54:12.531281');
INSERT INTO `django_session` VALUES ('4nnlyqxk1wlpcc0rk4411kq2l7gdnr34', 'YTJkNjk2Yjk2ZDIwYmQ5NGI3OWRmYWUzNDIyN2FlMTA4NTUxYWMwNDp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0xNSAxNDo0NjowM1wiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-15 16:43:47.705310');
INSERT INTO `django_session` VALUES ('4pq21rfpf4xwmxwjfuw1ws6rzd1gm2b7', 'YzliYzYzMDBlMGEyZTk3NGRlOTQ1MjE4ODNhYmJkODMzY2I5ZDZkZDp7InVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJzZXNzaW9uX3R4dCI6eyJ1c2VyaWQiOjUsImxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTIgMTU6MzY6NDVcIiIsInVzZXJuYW1lIjoidGVzdDIiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYifSwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyJ9', '2018-01-12 16:39:19.745423');
INSERT INTO `django_session` VALUES ('5otoe6uu7p6va7wbyink9g36mc73ajai', 'MGI3YzE2ODBmNTQ2ZDJjNzlkODQ1YmJiZGE5Mjg3YzY3NjYzMGNiNTp7Il9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2lkIjoiNSIsInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwic2Vzc2lvbl90eHQiOnsidXNlcmlkIjo1LCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJsYXN0X2xvZ2luIjoiXCIyMDE4LTAxLTEyIDE0OjMzOjE3XCIiLCJ1c2VybmFtZSI6InRlc3QyIn0sInVzZXJuYW1lIjoidGVzdDEyMzQ1NiJ9', '2018-01-12 15:12:52.067179');
INSERT INTO `django_session` VALUES ('5q2vhd3mcmd9m2jffaj11aofxogywzsf', 'NzU1MWRkOGQ5ZDg0ZjY4ZDRmNTFmODk5MmFjZWQ5NjA0YTZlYmIxZTp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMSAxMDo0NDozOFwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-21 12:34:16.094865');
INSERT INTO `django_session` VALUES ('5z7r2buiyzi27aqowfk1b3hqcg9q9r7o', 'NGMyNGE2YTAxMmE0Yzk3Nzk0Yjg1MmM4NTEwMmZhZjFhNWE3MGFjMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2lkIjoiNSIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTIgMTU6MDI6NTFcIiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiJ9LCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-12 15:23:38.581324');
INSERT INTO `django_session` VALUES ('6xj79x8ylv5kb9377bmj0w8b22ih3chk', 'ZjVjYThlYThlYTFlZDgwNTJkZjc5OTllYTRmMDg0ZTJlYmI2ZDViNDp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0xOSAxNjozNTo0NFwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-19 18:30:02.552234');
INSERT INTO `django_session` VALUES ('73yn1e4rnfrio79pjs6uus5n2d5pb625', 'YjVkMjk3NDI2Mjk4ZWFmNDBmZDYyZjliZmJhYjAxMTA4OGJmN2I4Nzp7InVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJzZXNzaW9uX3R4dCI6eyJ1c2VybmFtZSI6InRlc3QyIiwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxMDoxMzoyNVwiIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwidXNlcmlkIjo1fSwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDB9', '2018-01-12 10:41:11.517399');
INSERT INTO `django_session` VALUES ('7pmfd7bn94mh5zfyc4skxqyyemoedmr4', 'OThlODBjNDk5ZmE4MDQ5ZWI0MWUwNmE3NzJiN2VlYzdiMTI5ODg2Nzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcmlkIjoidGVzdDIiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTQ6NDU6MTNcIiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 15:05:56.286586');
INSERT INTO `django_session` VALUES ('8438ejx9kxrrglvpt719aslivlu7iw0w', 'ZmQ1OTk4MzViNDkxZTU3Y2Y2NDljYzNjODRmNThmOTA0YzRkNzg4ZTp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6MywibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMCAxNjo0ODo0M1wiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzIn0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMyJ9', '2018-11-01 19:56:58.907462');
INSERT INTO `django_session` VALUES ('8zi6b60gj0evs32jho1fvyntukyxada4', 'Y2UwNDZlNGIyZDNiMmY2OGZlZjE0OWE0NGI2MTk0N2VjODBiNGNlNTp7InNlc3Npb25fdHh0Ijp7InVzZXJuYW1lIjoidGVzdDIiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJsYXN0X2xvZ2luIjoiXCIyMDE4LTAxLTExIDE3OjA2OjQ5XCIiLCJ1c2VyaWQiOjV9LCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2hhc2giOiJhNDY5OTgwZTZiNGMyZWExZDc1MmIwMTZkMjQ1YzMxZTcxZmMyNTQ3IiwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-11 17:27:15.753264');
INSERT INTO `django_session` VALUES ('agpqza58qvr6194d8jfcvdnj3c555d4z', 'Mzg3M2JkOGI2MzZmYjQ0NzBkMjExNzJiNTY1ZDIxOWMwNGJlY2RmYTp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2Iiwic2Vzc2lvbl90eHQiOnsibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxMDo0NDoxMlwiIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwidXNlcmlkIjo1LCJ1c2VybmFtZSI6InRlc3QyIn0sInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyJ9', '2018-01-12 11:59:58.297593');
INSERT INTO `django_session` VALUES ('ai9ymgxo8l76tr2q2glqzhzaqg3rpjjj', 'MDQwZGUzODBhNGYwM2U3OGM4NmRhZGQ3N2VmMDM0OGI0ZDEzMjk2YTp7Il9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTAgMTc6NDY6MjRcIiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiJ9LCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-11 10:01:59.070158');
INSERT INTO `django_session` VALUES ('b2ecbsppnn3dn6x2y52vimjz14qtulpw', 'NmRhMTUzZGYyYzNkNzcwODI4YTg3MjcxZDkxMTc1NGMzYTkxZGQ5Zjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcmlkIjoidGVzdDIiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTQ6NTU6NTZcIiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 15:33:07.968969');
INSERT INTO `django_session` VALUES ('b6isisdadwosf8c4d4cwvzxn27745myf', 'ZTUzN2MwODE2MjVjYjUyZjc1OTBiNzc3NWYzMTAxMzdlMDQwY2NiYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcmlkIjoidGVzdDIiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTQ6MzA6MjVcIiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 14:55:13.554113');
INSERT INTO `django_session` VALUES ('bxqoj00nh8cs1904jvwds5ulyogr9id3', 'ZThhNmU0MTlkM2M2MzMxNWNjMGMyZTI3NzE4ZTAwZGU1ZmIwN2NjNDp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJzZXNzaW9uX3R4dCI6eyJ1c2VybmFtZSI6InRlc3QyIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxMjowNzowMFwiIiwidXNlcmlkIjo1fSwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJ1c2VyaWQiOiJ0ZXN0MiIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiJ9', '2018-01-12 12:34:13.725362');
INSERT INTO `django_session` VALUES ('cnxkwps5ln2qmngoruffuwgugvfaxm38', 'OTcxNDIzOTEwZWEwZTZmMmU4NDUwYmM1ZjMwYjlkMzBiMzhmZjk5YTp7Il9zZXNzaW9uX2V4cGlyeSI6NjAwLCJzZXNzaW9uX3R4dCI6eyJ1c2VybmFtZSI6InRlc3QyIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAxMDowODoyNFwiIiwidXNlcmlkIjo1fSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VyaWQiOiJ0ZXN0MiIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiJ9', '2018-01-11 10:35:52.352641');
INSERT INTO `django_session` VALUES ('co8hh2dusgmdj0uygy5kp1zs1cpm0blh', 'YjUxZjBjYTYxNzFkOWE3YWIzNThkNjQ1MjljZmIxZGVhMTU5YjU2Mzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcmlkIjoidGVzdDIiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTQ6MTk6MjVcIiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 14:40:25.578177');
INSERT INTO `django_session` VALUES ('cpdlrh2z3svn2ldjeq2z6jpe8ijaeaog', 'MTc1YmU1NmU4NDVkNDI2NDczZDk3MTBkZTgxNzQwN2IwMGMzYWM3ZDp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMSAxNzoxNToxMFwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-21 19:17:36.341701');
INSERT INTO `django_session` VALUES ('cxo2x65h6yvvkvqh8ictskausdtlp0sj', 'MDI5NmQ2ODlmNGRkYmY3NmQ0YmRmZmQ3ZDk0N2Y4OWQ0ZGVkY2UyNDp7InNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTA6MjU6NDlcIiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJ1c2VyaWQiOiJ0ZXN0MiIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2lkIjoiNSIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2018-01-11 10:46:00.089028');
INSERT INTO `django_session` VALUES ('ddfay8mf6g3wycgw3juzi2pqhld6xh0y', 'YjEyZWFhYTg4ZjA0NDMxYzI3MTRlMTI1ZjQzOTlkNjZkNGI0ZDEwMTp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJ1c2VyaWQiOiJ0ZXN0MiIsInNlc3Npb25fdHh0Ijp7InVzZXJpZCI6NSwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxNjoyOToxOVwiIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2hhc2giOiJhNDY5OTgwZTZiNGMyZWExZDc1MmIwMTZkMjQ1YzMxZTcxZmMyNTQ3IiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiJ9', '2018-01-12 16:54:08.962674');
INSERT INTO `django_session` VALUES ('e7o1pp12zszzpc4n0vdwnvuy00e6gna2', 'NDgxY2RiMTkzMDg2Zjk1OGNiMGNlM2RhZjQ5MDYyNjViNGEzYTBiMDp7InVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJ1c2VyaWQiOiJ0ZXN0MiIsInNlc3Npb25fdHh0Ijp7InVzZXJuYW1lIjoidGVzdDIiLCJ1c2VyaWQiOjUsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsImxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTI6MTg6NDBcIiJ9LCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2018-01-11 14:13:46.110031');
INSERT INTO `django_session` VALUES ('emmzui6ups6gntm2g6cy3j5ps8qly7l9', 'NjM1NTdjNzE2OTE4NDQwOGNkN2FmMmMxZjdkYTNkOWM3NGRkNTQ2Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwidXNlcmlkIjoidGVzdDIiLCJfYXV0aF91c2VyX2hhc2giOiJhNDY5OTgwZTZiNGMyZWExZDc1MmIwMTZkMjQ1YzMxZTcxZmMyNTQ3IiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsInNlc3Npb25fdHh0Ijp7InVzZXJpZCI6NSwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAxNDowMzo0NVwiIiwidXNlcm5hbWUiOiJ0ZXN0MiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiJ9LCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 14:29:26.039109');
INSERT INTO `django_session` VALUES ('exwbyg278wzrofxb8vickfir6qg93kjn', 'OWFiZjcwNzdjNWVjZDk0NTkzNjJiMjAxMTYzNmZmMDdjMGEwYzM4Njp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0xNSAxNTowMzo0N1wiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-16 12:32:51.392168');
INSERT INTO `django_session` VALUES ('fdbx0qxfjumvyakced1jlmo9h20dkqom', 'ZmU0ZWUxMmQ1M2Y0MWUyNDhiNzllY2ZmNDI1ZjkzMDliMTc5Nzc3Nzp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMyAxMTowNDowMlwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-28 11:30:18.607910');
INSERT INTO `django_session` VALUES ('glzwd20t2171wnz85nkummecmocilcbd', 'MGQ2MmU5OWViYWFlZjcxYWNlYTQwZDgzMmVhOTQ2YmMyMTdlMTM3OTp7Il9hdXRoX3VzZXJfaWQiOiI1IiwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2IiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInNlc3Npb25fdHh0Ijp7InBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsImxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTA6MzU6NTlcIiIsInVzZXJuYW1lIjoidGVzdDIiLCJ1c2VyaWQiOjV9LCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-11 11:30:22.917198');
INSERT INTO `django_session` VALUES ('gwbmnudt6qejxcl6q2ucn88ebimq3eei', 'NGU5NTkzMDk5MjY2NDdkNTUyMDkyYWNmYWViZGY3YWI2NTVkN2EwZjp7Il9hdXRoX3VzZXJfaWQiOiI1Iiwic2Vzc2lvbl90eHQiOnsibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAxMToyMDoyMlwiIiwidXNlcmlkIjo1LCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJ1c2VybmFtZSI6InRlc3QyIn0sInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyJ9', '2018-01-11 11:47:48.147185');
INSERT INTO `django_session` VALUES ('immul1rd14v0qgsk0dtcjzzgb2kxdqv0', 'MmMyM2Y0YTBhNmE3Yzc4MTU3ZGM4ZmI3MzhlYmM3NWI3NDVlMmRiODp7Il9zZXNzaW9uX2V4cGlyeSI6NjAwLCJzZXNzaW9uX3R4dCI6eyJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJsYXN0X2xvZ2luIjoiXCIyMDE4LTAxLTExIDEyOjA3OjU0XCIiLCJ1c2VyaWQiOjUsInVzZXJuYW1lIjoidGVzdDIifSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJ1c2VyaWQiOiJ0ZXN0MiIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2lkIjoiNSIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiJ9', '2018-01-11 12:28:40.750295');
INSERT INTO `django_session` VALUES ('kfkdey5pyncpn0ovesmxudot5kagjk80', 'NGI1YmE4NjY1MTQxZTg0NWVkNmRmOGI0ZjVkZTUyYTZkMWEyYjE1Yjp7InVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTU6NTI6MjVcIiIsInVzZXJpZCI6NSwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 17:06:38.203844');
INSERT INTO `django_session` VALUES ('kviryi1i4kvec79p2kso9nos8vpx3yqp', 'YmFiYTllZDIxOTUzNTgwYjk3MmQzNDE4MDViNjY0YjFhMTQwOWQ2Mzp7InNlc3Npb25fdHh0Ijp7InBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJuYW1lIjoidGVzdDIiLCJsYXN0X2xvZ2luIjoiXCIyMDE4LTAxLTExIDE4OjAwOjU1XCIiLCJ1c2VyaWQiOjV9LCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-12 10:09:47.220466');
INSERT INTO `django_session` VALUES ('o01e5v9ud43s7rct09uv68snkhtf0go8', 'NzBmYWQ5MDE2ZDcyZDAxYjhmZmVjNGY2ZWY3NzczNmE5YTg1OTFiOTp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMSAxMDo1NDoxNlwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-21 15:50:33.161004');
INSERT INTO `django_session` VALUES ('odzlf8oks5so53qcx7wkm9exetaklqct', 'OTU3Y2Y5M2FmODI1MjNlMjRhY2JmODA0MDQxODgwYmE1MTkwNTI4Nzp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMCAxMToyOTo1NFwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-20 13:26:58.360889');
INSERT INTO `django_session` VALUES ('pfasrwngp59do3ad5h8h0fuda5m7xfha', 'MzFlNGY0MTFkYWJhMDlhMDIyOGNhMzUyNTRlNzA2MzE1ZDlmODQxMDp7Il9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInNlc3Npb25fdHh0Ijp7InBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJuYW1lIjoidGVzdDIiLCJ1c2VyaWQiOjUsImxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTEgMTc6Mzk6NThcIiJ9LCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOiJ0ZXN0MiIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-11 18:10:55.219080');
INSERT INTO `django_session` VALUES ('r7s4e0l9m728mb85i3p7k6e3uywhdbgl', 'ODA3OGEzOGQ0ZTUzMzc3MGZmMjgzNGVjYTkyNDFhMmQwYjFmY2E0ZDp7InVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJzZXNzaW9uX3R4dCI6eyJ1c2VybmFtZSI6InRlc3QyIiwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAxNjo1NjozOFwiIiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwidXNlcmlkIjo1fSwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-11 17:16:50.067809');
INSERT INTO `django_session` VALUES ('svcls4n90t7h0kdkzr0osuqewhcdn5es', 'NDc3YjVlZTgwOTljN2RlYzIyMDMxZmU0ZTZkOWY3YTg0ZTllNjAyNzp7InNlc3Npb25fdHh0Ijp7InVzZXJuYW1lIjoidGVzdDIiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJsYXN0X2xvZ2luIjoiXCIyMDE4LTAxLTExIDExOjM3OjQ3XCIiLCJ1c2VyaWQiOjV9LCJfYXV0aF91c2VyX2lkIjoiNSIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-11 12:06:58.841205');
INSERT INTO `django_session` VALUES ('td525g01wkz0vm9rbeltol05q6j8z37h', 'MWMwOTIxYmNlN2YzMWM3MjUyNmZjZDgwMmM4NWFlNmZmZjJkZjlhYzp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsInNlc3Npb25fdHh0Ijp7Imxhc3RfbG9naW4iOiJcIjIwMTgtMDEtMTIgMTU6MTM6MzhcIiIsInVzZXJpZCI6NSwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJ1c2VybmFtZSI6InRlc3QxMjM0NTYiLCJ1c2VyaWQiOiJ0ZXN0MiJ9', '2018-01-12 15:46:45.565282');
INSERT INTO `django_session` VALUES ('tuncnjtx9glww2kolbqqy02jd8vycpki', 'MTBkZmIwMTU4OGI5YjY3NjM0ZjRmOWZkY2E4OTcyZjA4NDljY2I2Nzp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMSAxNzozNzozNlwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-22 12:46:54.307423');
INSERT INTO `django_session` VALUES ('u5ayld7ea4guix4jdjlvu53len6o34b5', 'NTMxNTQzYTY5NTE0ZTY5NDFhYjIyZWRlMWFmYmYzNDBkYjVlNWNjMjp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIiwic2Vzc2lvbl90eHQiOnsidXNlcmlkIjo4LCJsYXN0X2xvZ2luIjoiXCIyMDE4LTExLTAyIDEwOjQ4OjQ5XCIiLCJ1c2VybmFtZSI6InJvb3QiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYifSwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDAwLCJ1c2VyaWQiOiJyb290IiwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2In0=', '2018-11-02 15:49:03.870797');
INSERT INTO `django_session` VALUES ('vb8spi8jxp15nnv23hwmkhl4jnx9nb0f', 'ZjEyODBiNzBjZGE2ZGZiMmY2ZWU0MjM1YTQ2YzdjMTEzMzFlMjRlZTp7InVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInVzZXJpZCI6InRlc3QyIiwic2Vzc2lvbl90eHQiOnsibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAwOTo1OTo0N1wiIiwidXNlcm5hbWUiOiJ0ZXN0MiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6NX0sIl9hdXRoX3VzZXJfaWQiOiI1IiwiX3Nlc3Npb25fZXhwaXJ5Ijo2MDB9', '2018-01-12 10:23:25.231808');
INSERT INTO `django_session` VALUES ('vnenwvedy56ad6m4v9dnfyznozh7ndev', 'MDZkNDk1YzM1YjBiMjQyNmQzN2ZlYWM1MDk4MmFjZGM0NDRmMjc0YTp7Il9hdXRoX3VzZXJfaGFzaCI6ImE0Njk5ODBlNmI0YzJlYTFkNzUyYjAxNmQyNDVjMzFlNzFmYzI1NDciLCJfYXV0aF91c2VyX2lkIjoiNSIsInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfc2Vzc2lvbl9leHBpcnkiOjYwMCwidXNlcm5hbWUiOiJ0ZXN0MTIzNDU2Iiwic2Vzc2lvbl90eHQiOnsibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAxNzoxNzoxNVwiIiwidXNlcm5hbWUiOiJ0ZXN0MiIsInVzZXJpZCI6NSwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In19', '2018-01-11 17:49:58.667920');
INSERT INTO `django_session` VALUES ('x3lmu5zem1ef22i6ln8jvidefgtwhxau', 'NjM1YjM5MjFhN2VjMGRkNWFmNzA1YmExODgwMDdlMGU5NWI2OGY4MDp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMCAxNDoxNzoxNFwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-20 16:37:26.070570');
INSERT INTO `django_session` VALUES ('x9o9y493gbfb4eow61f98airl56rh8df', 'MmY4Zjk1MjlmNTk4M2JkNDQ3MDM2YTg5YmRkZWI2Nzg1Yjc5NjE0Njp7InVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsInVzZXJpZCI6InRlc3QyIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ2OTk4MGU2YjRjMmVhMWQ3NTJiMDE2ZDI0NWMzMWU3MWZjMjU0NyIsIl9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInNlc3Npb25fdHh0Ijp7InVzZXJpZCI6NSwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMiAxMzo1OTozMlwiIiwidXNlcm5hbWUiOiJ0ZXN0MiIsInBhc3N3b3JkIjoidGVzdDEyMzQ1NiJ9LCJfYXV0aF91c2VyX2lkIjoiNSJ9', '2018-01-12 14:26:50.147516');
INSERT INTO `django_session` VALUES ('xaaot0njr2uvc6ya5rwlel1a42avasm9', 'YWU5NDkwZWM2YWE4NzQ2YThjYTE1NGZiMjA1N2U0MjRmZWM2OTVjMjp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0yMiAxNDowODo0M1wiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-22 15:51:02.073637');
INSERT INTO `django_session` VALUES ('xeaoqcb5lipmycugclk0ty0m6slmgh6y', 'YzMxZWMyYmEwZmU4NWMyZDQ2MjAxODg0ZDM2ODk0OTM4NzdkOWZlZDp7InNlc3Npb25fdHh0Ijp7InVzZXJpZCI6OCwibGFzdF9sb2dpbiI6IlwiMjAxOC0xMS0xNiAxNTo1MjoyMlwiIiwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2In0sIl9zZXNzaW9uX2V4cGlyeSI6NjAwMCwidXNlcmlkIjoicm9vdCIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiIsIl9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYWEzNjkwODRjM2Q0ODAwMmQ5OTc1Mjg2MzlmNmJhY2U5ODU0NGUxIn0=', '2018-11-16 17:43:35.109741');
INSERT INTO `django_session` VALUES ('zcqc6msjxpjtzqqh3jw4t25y9t5l1ml6', 'YmZjYmU5ZGMyNDEzNTE3OTdkZjE4NGQwNWEzMzIyODhjMzUxMTA2Mjp7Il9zZXNzaW9uX2V4cGlyeSI6NjAwLCJfYXV0aF91c2VyX2hhc2giOiJhNDY5OTgwZTZiNGMyZWExZDc1MmIwMTZkMjQ1YzMxZTcxZmMyNTQ3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiNSIsInNlc3Npb25fdHh0Ijp7InVzZXJpZCI6NSwicGFzc3dvcmQiOiJ0ZXN0MTIzNDU2IiwibGFzdF9sb2dpbiI6IlwiMjAxOC0wMS0xMSAxNTozNToxNFwiIiwidXNlcm5hbWUiOiJ0ZXN0MiJ9LCJ1c2VyaWQiOiJ0ZXN0MiIsInVzZXJuYW1lIjoidGVzdDEyMzQ1NiJ9', '2018-01-11 16:02:26.205725');

-- ----------------------------
-- Table structure for `host`
-- ----------------------------
DROP TABLE IF EXISTS `host`;
CREATE TABLE `host` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `ip` varchar(30) NOT NULL,
  `minion_id` varchar(40) DEFAULT NULL,
  `minion_key_stat` int(1) DEFAULT '2' COMMENT '\r\n1为接受\r\n2为未接受\r\n3为Denied0为已删除的4为拒绝的',
  `hostname` varchar(40) DEFAULT NULL,
  `ostype` varchar(15) DEFAULT NULL,
  `application` varchar(50) DEFAULT NULL,
  `status` int(1) DEFAULT '0' COMMENT 'salt主机是否能连上客户机，能为1，否为0',
  `pwd` varchar(128) NOT NULL,
  `group_id` int(5) DEFAULT NULL,
  `group_name` varchar(20) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `port` varchar(20) NOT NULL DEFAULT '22',
  `groupid` varchar(20) NOT NULL DEFAULT '1',
  `Createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`ip`),
  UNIQUE KEY `ip` (`ip`) USING BTREE,
  KEY `minion_idx` (`minion_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host
-- ----------------------------
INSERT INTO `host` VALUES ('1', '192.168.216.129', '192.168.168.129_web1', '1', '2', 'Others', '2', '0', '5e543256c480ac577d30f76f9120eb74', '1', '1', '1', '22', '1', '2018-11-23 11:05:25', '2018-11-23 11:05:25');
INSERT INTO `host` VALUES ('87', '192.168.1.11', 'windows', '1', 'a', 'Windows', 'a', '1', 'b6d767d2f8ed5d21a44b0e5886680cb9', null, '无', 'administrator', 'ss', '1', '2018-11-21 14:11:59', '2018-11-21 14:11:59');
INSERT INTO `host` VALUES ('88', '192.168.77.123', 'windows1', '2', 'undefined', 'Linux', 'undefined', '0', '0cc175b9c0f1b6a831c399e269772661', null, '无', 'a', 'a', '1', '2018-11-21 14:17:12', '2018-11-21 14:17:12');
INSERT INTO `host` VALUES ('89', '999', 'windows', '1', 'undefined', 'Linux', '9', '1', '45c48cce2e2d7fbdea1afc51c7c6ad26', null, '无', '9', '9', '1', '2018-11-21 14:19:42', '2018-11-21 14:19:42');

-- ----------------------------
-- Table structure for `host_details`
-- ----------------------------
DROP TABLE IF EXISTS `host_details`;
CREATE TABLE `host_details` (
  `ip` varchar(20) NOT NULL,
  `cpu` varchar(20) DEFAULT NULL,
  `memory` varchar(20) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `product` varchar(50) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `sn` varchar(50) DEFAULT NULL,
  `Createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host_details
-- ----------------------------

-- ----------------------------
-- Table structure for `host_group`
-- ----------------------------
DROP TABLE IF EXISTS `host_group`;
CREATE TABLE `host_group` (
  `group_id` int(5) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) NOT NULL,
  `category` varchar(50) DEFAULT NULL COMMENT '类别',
  `remark` varchar(100) DEFAULT NULL COMMENT '描述信息',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host_group
-- ----------------------------
INSERT INTO `host_group` VALUES ('1', 'oracle组', null, null);
INSERT INTO `host_group` VALUES ('2', 'apache组', null, null);
INSERT INTO `host_group` VALUES ('3', 'redis组', null, null);
INSERT INTO `host_group` VALUES ('13', 'mysql组', null, null);
INSERT INTO `host_group` VALUES ('14', 'vftp组', null, null);
INSERT INTO `host_group` VALUES ('15', '无', null, null);

-- ----------------------------
-- Table structure for `operation_record`
-- ----------------------------
DROP TABLE IF EXISTS `operation_record`;
CREATE TABLE `operation_record` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(40) NOT NULL,
  `user_id` varchar(40) NOT NULL,
  `action` varchar(200) NOT NULL COMMENT '操作记录',
  `target_ids` varchar(40) NOT NULL DEFAULT '0' COMMENT '作为表opertion_minions的外键，表明此次执行了哪些minion_id的机器,如果此处为0则表明没有相应的主机列表',
  `result` varchar(40) NOT NULL COMMENT '是否成功',
  `exec_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `target_ids_idx` (`target_ids`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of operation_record
-- ----------------------------
INSERT INTO `operation_record` VALUES ('13', 'test2', '5', '添加主机', 'c48b37a4-f697-11e7-991b-e4a471e21cf0', 'True', '2018-01-11 14:22:16', '2018-01-11 14:22:15');
INSERT INTO `operation_record` VALUES ('14', 'test2', '5', '添加主机', 'efa40698-f697-11e7-97c5-e4a471e21cf0', 'True', '2018-01-11 14:23:28', '2018-01-11 14:23:27');
INSERT INTO `operation_record` VALUES ('15', 'test2', '5', '添加主机', '116cd7b6-f698-11e7-9ed7-e4a471e21cf0', 'True', '2018-01-11 14:24:25', '2018-01-11 14:24:24');
INSERT INTO `operation_record` VALUES ('16', 'test2', '5', '添加主机', '3bc3075e-f698-11e7-913d-e4a471e21cf0', 'True', '2018-01-11 14:25:36', '2018-01-11 14:25:35');
INSERT INTO `operation_record` VALUES ('17', 'test2', '5', '添加主机', 'd25c113a-f740-11e7-b671-e4a471e21cf0', 'True', '2018-01-12 10:32:24', '2018-01-12 10:32:23');
INSERT INTO `operation_record` VALUES ('18', 'test2', '5', '修改主机', '809d0dd4-f742-11e7-a799-e4a471e21cf0', 'True', '2018-01-12 10:44:26', '2018-01-12 10:44:25');
INSERT INTO `operation_record` VALUES ('19', 'test2', '5', '修改主机', '9585b822-f742-11e7-a8c4-e4a471e21cf0', 'True', '2018-01-12 10:45:01', '2018-01-12 10:45:00');
INSERT INTO `operation_record` VALUES ('28', 'test2', '5', '删除主机', 'c9c6e4e4-f74c-11e7-8fef-e4a471e21cf0', 'True', '2018-01-12 11:58:03', '2018-01-12 11:58:03');
INSERT INTO `operation_record` VALUES ('29', 'test2', '5', '删除主机', 'e8481f82-f74c-11e7-a99a-e4a471e21cf0', 'True', '2018-01-12 11:58:54', '2018-01-12 11:58:54');
INSERT INTO `operation_record` VALUES ('30', 'test2', '5', '更新主机详情', '1b9b5024-f74e-11e7-87ff-e4a471e21cf0', 'True', '2018-01-12 12:07:30', '2018-01-12 12:07:30');
INSERT INTO `operation_record` VALUES ('31', 'test2', '5', '更新主机详情', 'ec52aaf8-f750-11e7-baed-e4a471e21cf0', 'False', '2018-01-12 12:27:39', '2018-01-12 12:27:39');
INSERT INTO `operation_record` VALUES ('32', 'test2', '5', '更新主机详情', '10d67a4c-f751-11e7-82ab-e4a471e21cf0', 'False', '2018-01-12 12:28:40', '2018-01-12 12:28:40');
INSERT INTO `operation_record` VALUES ('33', 'test2', '5', '添加主机组', 'd91b74d0-f75d-11e7-b5ce-e4a471e21cf0', 'True', '2018-01-12 14:00:10', '2018-01-12 14:00:10');
INSERT INTO `operation_record` VALUES ('34', 'test2', '5', '添加主机组', 'a87d47e4-f75e-11e7-9568-e4a471e21cf0', 'True', '2018-01-12 14:05:58', '2018-01-12 14:05:58');
INSERT INTO `operation_record` VALUES ('35', 'test2', '5', '创建主机组', 'bf81d09a-f75e-11e7-8bfe-e4a471e21cf0', 'True', '2018-01-12 14:06:37', '2018-01-12 14:06:37');
INSERT INTO `operation_record` VALUES ('36', 'test2', '5', '将主机IP添加主机组', 'afcdc390-f766-11e7-9e5e-e4a471e21cf0', 'True', '2018-01-12 15:03:27', '2018-01-12 15:03:26');
INSERT INTO `operation_record` VALUES ('47', 'test2', '5', '172.17.39.208_windows10_app执行salt命令:test.ping', '5cb5c128-f769-11e7-843d-e4a471e21cf0', 'True', '2018-01-12 15:22:36', '2018-01-12 15:22:35');
INSERT INTO `operation_record` VALUES ('48', 'test2', '5', 'docker_images_minion1执行salt命令:test.ping参数或者', '5cc35f90-f769-11e7-8217-e4a471e21cf0', 'True', '2018-01-12 15:22:36', '2018-01-12 15:22:35');
INSERT INTO `operation_record` VALUES ('49', 'test2', '5', '上传文件命令', '7548fdfe-f773-11e7-9aab-e4a471e21cf0', 'True', '2018-01-12 16:34:52', '2018-01-12 16:34:51');
INSERT INTO `operation_record` VALUES ('50', 'test2', '5', '本地yum初始化', 'cd852d86-f774-11e7-8ace-e4a471e21cf0', 'True', '2018-01-12 16:44:29', '2018-01-12 16:44:29');
INSERT INTO `operation_record` VALUES ('51', 'test2', '5', '本地yum初始化', '16c64bca-f775-11e7-8dea-e4a471e21cf0', 'True', '2018-01-12 16:46:32', '2018-01-12 16:46:32');
INSERT INTO `operation_record` VALUES ('52', 'root', '8', '修改主机', 'ae450702-de41-11e8-9f96-80c5f2966cd8', 'True', '2018-11-02 09:50:31', '2018-11-02 09:50:31');
INSERT INTO `operation_record` VALUES ('53', 'admin', '2', '修改主机', '0e74df12-de44-11e8-a93a-80c5f2966cd8', 'True', '2018-11-02 10:07:32', '2018-11-02 10:07:31');
INSERT INTO `operation_record` VALUES ('54', 'admin', '2', '修改主机', '1807dad4-de44-11e8-abc8-80c5f2966cd8', 'True', '2018-11-02 10:07:48', '2018-11-02 10:07:47');
INSERT INTO `operation_record` VALUES ('55', 'root', '8', '将主机IP添加主机组', '8602c0ba-de4a-11e8-93b7-80c5f2966cd8', 'True', '2018-11-02 10:53:49', '2018-11-02 10:53:49');
INSERT INTO `operation_record` VALUES ('56', 'root', '8', 'windows执行salt命令:test.ping', '9bd023d8-de4b-11e8-8057-80c5f2966cd8', 'True', '2018-11-02 11:01:35', '2018-11-02 11:01:35');
INSERT INTO `operation_record` VALUES ('57', 'root', '8', '修改主机', 'df00d11e-de4b-11e8-b3c4-80c5f2966cd8', 'True', '2018-11-02 11:03:28', '2018-11-02 11:03:28');
INSERT INTO `operation_record` VALUES ('58', 'root', '8', '修改主机', 'fb9ec62e-de4b-11e8-9fb4-80c5f2966cd8', 'True', '2018-11-02 11:04:16', '2018-11-02 11:04:16');
INSERT INTO `operation_record` VALUES ('59', 'root', '8', '更新主机详情', '267eac28-de4c-11e8-980d-80c5f2966cd8', 'True', '2018-11-02 11:05:28', '2018-11-02 11:05:27');
INSERT INTO `operation_record` VALUES ('60', 'root', '8', '修改主机', '7037251e-de4c-11e8-ad73-80c5f2966cd8', 'True', '2018-11-02 11:07:32', '2018-11-02 11:07:31');
INSERT INTO `operation_record` VALUES ('61', 'root', '8', '更新主机详情', '7fc8cf64-de4c-11e8-b19a-80c5f2966cd8', 'True', '2018-11-02 11:07:58', '2018-11-02 11:07:57');
INSERT INTO `operation_record` VALUES ('62', 'root', '8', '更新主机详情', '7fca84da-de4c-11e8-839f-80c5f2966cd8', 'True', '2018-11-02 11:07:58', '2018-11-02 11:07:57');
INSERT INTO `operation_record` VALUES ('63', 'root', '8', '修改主机', '036150e4-de4d-11e8-8389-80c5f2966cd8', 'True', '2018-11-02 11:11:39', '2018-11-02 11:11:38');
INSERT INTO `operation_record` VALUES ('64', 'root', '8', '修改主机', '12a44e7e-de4d-11e8-9623-80c5f2966cd8', 'True', '2018-11-02 11:12:04', '2018-11-02 11:12:04');
INSERT INTO `operation_record` VALUES ('65', 'root', '8', '修改主机', '2ab31b74-de4d-11e8-8b5e-80c5f2966cd8', 'True', '2018-11-02 11:12:45', '2018-11-02 11:12:44');
INSERT INTO `operation_record` VALUES ('66', 'root', '8', '删除salt_key', '41556afa-de4d-11e8-9f5e-80c5f2966cd8', 'True', '2018-11-02 11:13:22', '2018-11-02 11:13:22');
INSERT INTO `operation_record` VALUES ('67', 'root', '8', '删除salt_key', '5f07012e-de4d-11e8-a1b6-80c5f2966cd8', 'True', '2018-11-02 11:14:12', '2018-11-02 11:14:12');
INSERT INTO `operation_record` VALUES ('68', 'root', '8', '修改主机', '9a5a7d68-de4d-11e8-b11e-80c5f2966cd8', 'True', '2018-11-02 11:15:52', '2018-11-02 11:15:51');
INSERT INTO `operation_record` VALUES ('69', 'root', '8', '修改主机', 'a4b2b642-de4d-11e8-87ff-80c5f2966cd8', 'True', '2018-11-02 11:16:09', '2018-11-02 11:16:09');
INSERT INTO `operation_record` VALUES ('70', 'root', '8', '修改主机', 'af5a3f0a-de4d-11e8-a136-80c5f2966cd8', 'True', '2018-11-02 11:16:27', '2018-11-02 11:16:27');
INSERT INTO `operation_record` VALUES ('71', 'root', '8', '修改主机', 'b56fc4f8-de4d-11e8-a4cf-80c5f2966cd8', 'True', '2018-11-02 11:16:37', '2018-11-02 11:16:37');
INSERT INTO `operation_record` VALUES ('72', 'root', '8', '修改主机', 'c398d4e2-de4d-11e8-ac2d-80c5f2966cd8', 'True', '2018-11-02 11:17:01', '2018-11-02 11:17:01');
INSERT INTO `operation_record` VALUES ('73', 'root', '8', '修改主机', 'c802ce94-de4d-11e8-9d1f-80c5f2966cd8', 'True', '2018-11-02 11:17:08', '2018-11-02 11:17:08');
INSERT INTO `operation_record` VALUES ('74', 'root', '8', '修改主机', 'd378b398-de4d-11e8-9a50-80c5f2966cd8', 'True', '2018-11-02 11:17:28', '2018-11-02 11:17:27');
INSERT INTO `operation_record` VALUES ('75', 'root', '8', '修改主机', 'dd50d078-de4d-11e8-bb73-80c5f2966cd8', 'True', '2018-11-02 11:17:44', '2018-11-02 11:17:44');
INSERT INTO `operation_record` VALUES ('76', 'root', '8', '修改主机', 'e3558990-de4d-11e8-9b7c-80c5f2966cd8', 'True', '2018-11-02 11:17:54', '2018-11-02 11:17:54');
INSERT INTO `operation_record` VALUES ('77', 'root', '8', '修改主机', 'ecb0451e-de4d-11e8-ad07-80c5f2966cd8', 'True', '2018-11-02 11:18:10', '2018-11-02 11:18:09');
INSERT INTO `operation_record` VALUES ('78', 'root', '8', '修改主机', 'f2a4c394-de4d-11e8-a4f7-80c5f2966cd8', 'True', '2018-11-02 11:18:20', '2018-11-02 11:18:19');
INSERT INTO `operation_record` VALUES ('79', 'root', '8', '修改主机', 'fa9de842-de4d-11e8-a50e-80c5f2966cd8', 'True', '2018-11-02 11:18:33', '2018-11-02 11:18:33');
INSERT INTO `operation_record` VALUES ('80', 'root', '8', '修改主机', 'fffc67c2-de4d-11e8-8c24-80c5f2966cd8', 'True', '2018-11-02 11:18:42', '2018-11-02 11:18:42');
INSERT INTO `operation_record` VALUES ('81', 'root', '8', '修改主机', 'eb98ef70-de4f-11e8-8756-80c5f2966cd8', 'True', '2018-11-02 11:32:27', '2018-11-02 11:32:27');
INSERT INTO `operation_record` VALUES ('82', 'root', '8', '删除salt_key', '13ebd4a4-de50-11e8-aac3-80c5f2966cd8', 'True', '2018-11-02 11:33:35', '2018-11-02 11:33:34');
INSERT INTO `operation_record` VALUES ('83', 'root', '8', '删除salt_key', '1bda901c-de50-11e8-a089-80c5f2966cd8', 'True', '2018-11-02 11:33:48', '2018-11-02 11:33:48');
INSERT INTO `operation_record` VALUES ('84', 'root', '8', '删除salt_key', '2563e9fa-de50-11e8-801b-80c5f2966cd8', 'True', '2018-11-02 11:34:04', '2018-11-02 11:34:04');
INSERT INTO `operation_record` VALUES ('85', 'root', '8', '删除salt_key', '270affa4-de50-11e8-94a5-80c5f2966cd8', 'True', '2018-11-02 11:34:07', '2018-11-02 11:34:06');
INSERT INTO `operation_record` VALUES ('86', 'root', '8', '删除salt_key', '2b8de140-de50-11e8-9e97-80c5f2966cd8', 'True', '2018-11-02 11:34:14', '2018-11-02 11:34:14');
INSERT INTO `operation_record` VALUES ('87', 'root', '8', '删除salt_key', '2cb18934-de50-11e8-85a5-80c5f2966cd8', 'True', '2018-11-02 11:34:16', '2018-11-02 11:34:16');
INSERT INTO `operation_record` VALUES ('88', 'root', '8', 'windows执行salt命令:test.ping', 'be9ee898-de50-11e8-bc2f-80c5f2966cd8', 'True', '2018-11-02 11:38:21', '2018-11-02 11:38:21');
INSERT INTO `operation_record` VALUES ('89', 'root', '8', '修改主机', 'da67f986-de50-11e8-8d8b-80c5f2966cd8', 'True', '2018-11-02 11:39:08', '2018-11-02 11:39:07');
INSERT INTO `operation_record` VALUES ('90', 'root', '8', '192.168.168.129_web1执行salt命令:test.ping', 'e6c9df5c-de50-11e8-95e4-80c5f2966cd8', 'True', '2018-11-02 11:39:29', '2018-11-02 11:39:28');
INSERT INTO `operation_record` VALUES ('91', 'root', '8', '192.168.168.129_web1执行salt命令:test.ping', 'ed1b5dfe-de50-11e8-82ab-80c5f2966cd8', 'True', '2018-11-02 11:39:39', '2018-11-02 11:39:39');
INSERT INTO `operation_record` VALUES ('92', 'root', '8', 'windows执行salt命令:test.ping', 'ed1c808c-de50-11e8-a17e-80c5f2966cd8', 'True', '2018-11-02 11:39:39', '2018-11-02 11:39:39');
INSERT INTO `operation_record` VALUES ('93', 'root', '8', '删除主机', 'd37aabf0-e8a2-11e8-b608-80c5f2966cd8', 'True', '2018-11-15 14:51:07', '2018-11-15 14:51:06');
INSERT INTO `operation_record` VALUES ('94', 'root', '8', '删除salt_key', '164b498a-e8a3-11e8-a223-80c5f2966cd8', 'True', '2018-11-15 14:52:59', '2018-11-15 14:52:58');
INSERT INTO `operation_record` VALUES ('95', 'root', '8', '删除salt_key', '8878b31e-e8a3-11e8-ac69-80c5f2966cd8', 'True', '2018-11-15 14:56:10', '2018-11-15 14:56:10');
INSERT INTO `operation_record` VALUES ('96', 'root', '8', '删除salt_key', 'c181fe8a-e8a3-11e8-aac0-80c5f2966cd8', 'True', '2018-11-15 14:57:46', '2018-11-15 14:57:45');
INSERT INTO `operation_record` VALUES ('97', 'root', '8', '删除salt_key', 'cca15c1c-e8a3-11e8-9bb5-80c5f2966cd8', 'True', '2018-11-15 14:58:05', '2018-11-15 14:58:04');
INSERT INTO `operation_record` VALUES ('98', 'root', '8', '删除salt_key', '7c98538c-e8a4-11e8-b4d2-80c5f2966cd8', 'True', '2018-11-15 15:03:00', '2018-11-15 15:02:59');
INSERT INTO `operation_record` VALUES ('99', 'root', '8', '修改主机', 'cb30a3c6-e8a4-11e8-8a7b-80c5f2966cd8', 'True', '2018-11-15 15:05:12', '2018-11-15 15:05:11');
INSERT INTO `operation_record` VALUES ('100', 'root', '8', '修改主机', '83869188-e8a5-11e8-a710-80c5f2966cd8', 'True', '2018-11-15 15:10:21', '2018-11-15 15:10:20');
INSERT INTO `operation_record` VALUES ('101', 'root', '8', '更新主机详情', '92b10212-e8a5-11e8-b4d9-80c5f2966cd8', 'True', '2018-11-15 15:10:46', '2018-11-15 15:10:46');
INSERT INTO `operation_record` VALUES ('102', 'root', '8', '更新主机详情', 'bb7512de-e8a5-11e8-8b6e-80c5f2966cd8', 'True', '2018-11-15 15:11:55', '2018-11-15 15:11:54');
INSERT INTO `operation_record` VALUES ('103', 'root', '8', '修改主机', '091992e8-e8a6-11e8-ac7c-80c5f2966cd8', 'True', '2018-11-15 15:14:05', '2018-11-15 15:14:04');
INSERT INTO `operation_record` VALUES ('104', 'root', '8', '更新主机详情', '5b528ae4-e8aa-11e8-8bbf-80c5f2966cd8', 'True', '2018-11-15 15:45:01', '2018-11-15 15:45:00');
INSERT INTO `operation_record` VALUES ('105', 'root', '8', '更新主机详情', '5b573c5c-e8aa-11e8-a1fe-80c5f2966cd8', 'True', '2018-11-15 15:45:01', '2018-11-15 15:45:00');
INSERT INTO `operation_record` VALUES ('106', 'root', '8', '更新主机详情', '9454c75c-e8aa-11e8-bcb6-80c5f2966cd8', 'True', '2018-11-15 15:46:37', '2018-11-15 15:46:36');
INSERT INTO `operation_record` VALUES ('107', 'root', '8', '更新主机详情', '94569858-e8aa-11e8-812b-80c5f2966cd8', 'True', '2018-11-15 15:46:37', '2018-11-15 15:46:36');
INSERT INTO `operation_record` VALUES ('108', 'root', '8', '命令:git log -2执行成功', 'c9fa2086-e94d-11e8-9fd9-80c5f2966cd8', 'True', '2018-11-16 11:14:55', '2018-11-16 11:14:54');
INSERT INTO `operation_record` VALUES ('109', 'root', '8', '命令:git log -2执行成功', 'ebf0e710-e94d-11e8-88f5-80c5f2966cd8', 'True', '2018-11-16 11:15:51', '2018-11-16 11:15:51');
INSERT INTO `operation_record` VALUES ('110', 'root', '8', '命令:git log 1执行成功', 'b572a5cc-e94f-11e8-95a7-80c5f2966cd8', 'True', '2018-11-16 11:28:39', '2018-11-16 11:28:39');
INSERT INTO `operation_record` VALUES ('111', 'root', '8', '更新主机详情', 'dddc40e2-e969-11e8-be29-80c5f2966cd8', 'False', '2018-11-16 14:35:54', '2018-11-16 14:35:53');
INSERT INTO `operation_record` VALUES ('112', 'root', '8', '更新主机详情', 'f4803826-ec91-11e8-98d3-80c5f2966cd8', 'True', '2018-11-20 15:00:25', '2018-11-20 15:00:25');
INSERT INTO `operation_record` VALUES ('113', 'root', '8', '更新主机详情', 'f483ed52-ec91-11e8-a1d0-80c5f2966cd8', 'True', '2018-11-20 15:00:25', '2018-11-20 15:00:25');
INSERT INTO `operation_record` VALUES ('114', 'root', '8', '删除主机', 'b4a33fc8-ed37-11e8-8b8e-80c5f2966cd8', 'True', '2018-11-21 10:46:54', '2018-11-21 10:46:54');
INSERT INTO `operation_record` VALUES ('115', 'root', '8', '删除主机', '2e45a50c-ed39-11e8-8d2f-80c5f2966cd8', 'True', '2018-11-21 10:57:28', '2018-11-21 10:57:28');
INSERT INTO `operation_record` VALUES ('116', 'root', '8', '修改主机', '982ccb1a-ed39-11e8-8bae-80c5f2966cd8', 'True', '2018-11-21 11:00:26', '2018-11-21 11:00:25');
INSERT INTO `operation_record` VALUES ('117', 'root', '8', '修改主机', '9e3323d0-ed39-11e8-95ae-80c5f2966cd8', 'True', '2018-11-21 11:00:36', '2018-11-21 11:00:35');
INSERT INTO `operation_record` VALUES ('118', 'root', '8', '添加主机', 'ebd69840-ed39-11e8-95eb-80c5f2966cd8', 'True', '2018-11-21 11:02:46', '2018-11-21 11:02:46');
INSERT INTO `operation_record` VALUES ('119', 'root', '8', '更新主机详情', '1251530c-ed3a-11e8-8219-80c5f2966cd8', 'True', '2018-11-21 11:03:51', '2018-11-21 11:03:50');
INSERT INTO `operation_record` VALUES ('120', 'root', '8', '更新主机详情', '1253f928-ed3a-11e8-9425-80c5f2966cd8', 'True', '2018-11-21 11:03:51', '2018-11-21 11:03:50');
INSERT INTO `operation_record` VALUES ('121', 'root', '8', '更新主机详情', '2094b208-ed3a-11e8-b765-80c5f2966cd8', 'True', '2018-11-21 11:04:15', '2018-11-21 11:04:14');
INSERT INTO `operation_record` VALUES ('122', 'root', '8', '更新主机详情', '20969bda-ed3a-11e8-b833-80c5f2966cd8', 'True', '2018-11-21 11:04:15', '2018-11-21 11:04:14');
INSERT INTO `operation_record` VALUES ('123', 'root', '8', '更新主机详情', 'ec805118-ed3a-11e8-9871-80c5f2966cd8', 'True', '2018-11-21 11:09:57', '2018-11-21 11:09:56');
INSERT INTO `operation_record` VALUES ('124', 'root', '8', '更新主机详情', 'ec822862-ed3a-11e8-b403-80c5f2966cd8', 'True', '2018-11-21 11:09:57', '2018-11-21 11:09:56');
INSERT INTO `operation_record` VALUES ('125', 'root', '8', '更新主机详情', '4d7be348-ed3b-11e8-8470-80c5f2966cd8', 'True', '2018-11-21 11:12:39', '2018-11-21 11:12:39');
INSERT INTO `operation_record` VALUES ('126', 'root', '8', '更新主机详情', '4d7da11c-ed3b-11e8-85c9-80c5f2966cd8', 'True', '2018-11-21 11:12:39', '2018-11-21 11:12:39');
INSERT INTO `operation_record` VALUES ('127', 'root', '8', '更新主机详情', '57de0b28-ed3b-11e8-9fc7-80c5f2966cd8', 'True', '2018-11-21 11:12:57', '2018-11-21 11:12:56');
INSERT INTO `operation_record` VALUES ('128', 'root', '8', '更新主机详情', '57df7b5c-ed3b-11e8-bcd8-80c5f2966cd8', 'True', '2018-11-21 11:12:57', '2018-11-21 11:12:56');
INSERT INTO `operation_record` VALUES ('129', 'root', '8', '删除主机', 'a5bd5476-ed3c-11e8-976a-80c5f2966cd8', 'True', '2018-11-21 11:22:17', '2018-11-21 11:22:16');
INSERT INTO `operation_record` VALUES ('130', 'root', '8', '添加主机', 'd9380b92-ed3c-11e8-a74c-80c5f2966cd8', 'True', '2018-11-21 11:23:43', '2018-11-21 11:23:43');
INSERT INTO `operation_record` VALUES ('131', 'root', '8', '删除主机', '0422a0ee-ed3d-11e8-b9b8-80c5f2966cd8', 'True', '2018-11-21 11:24:55', '2018-11-21 11:24:55');
INSERT INTO `operation_record` VALUES ('132', 'root', '8', '添加主机', '0c13a828-ed3d-11e8-9787-80c5f2966cd8', 'True', '2018-11-21 11:25:09', '2018-11-21 11:25:08');
INSERT INTO `operation_record` VALUES ('133', 'root', '8', '删除主机', '2fe34b22-ed3d-11e8-87f0-80c5f2966cd8', 'True', '2018-11-21 11:26:09', '2018-11-21 11:26:08');
INSERT INTO `operation_record` VALUES ('134', 'root', '8', '添加主机', '422fd18c-ed3d-11e8-a702-80c5f2966cd8', 'True', '2018-11-21 11:26:39', '2018-11-21 11:26:39');
INSERT INTO `operation_record` VALUES ('135', 'root', '8', '删除主机', '5f9e4cd8-ed3d-11e8-b6b1-80c5f2966cd8', 'True', '2018-11-21 11:27:29', '2018-11-21 11:27:28');
INSERT INTO `operation_record` VALUES ('136', 'root', '8', '添加主机', '7d1042a2-ed3d-11e8-8204-80c5f2966cd8', 'True', '2018-11-21 11:28:18', '2018-11-21 11:28:18');
INSERT INTO `operation_record` VALUES ('137', 'root', '8', '删除主机', '9579ce38-ed3d-11e8-83bf-80c5f2966cd8', 'True', '2018-11-21 11:28:59', '2018-11-21 11:28:59');
INSERT INTO `operation_record` VALUES ('138', 'root', '8', '添加主机', 'a1f02930-ed3d-11e8-9e8e-80c5f2966cd8', 'True', '2018-11-21 11:29:20', '2018-11-21 11:29:20');
INSERT INTO `operation_record` VALUES ('139', 'root', '8', '删除主机', '0ec8ed12-ed3e-11e8-94ba-80c5f2966cd8', 'True', '2018-11-21 11:32:23', '2018-11-21 11:32:22');
INSERT INTO `operation_record` VALUES ('140', 'root', '8', '添加主机', '183a3546-ed3e-11e8-b11f-80c5f2966cd8', 'True', '2018-11-21 11:32:39', '2018-11-21 11:32:38');
INSERT INTO `operation_record` VALUES ('141', 'root', '8', '删除主机', '61f78d90-ed3e-11e8-826e-80c5f2966cd8', 'True', '2018-11-21 11:34:42', '2018-11-21 11:34:42');
INSERT INTO `operation_record` VALUES ('142', 'root', '8', '添加主机', '68c123b4-ed3e-11e8-b9b8-80c5f2966cd8', 'True', '2018-11-21 11:34:54', '2018-11-21 11:34:53');
INSERT INTO `operation_record` VALUES ('143', 'root', '8', '删除主机', 'c5d370ca-ed3e-11e8-a800-80c5f2966cd8', 'True', '2018-11-21 11:37:30', '2018-11-21 11:37:29');
INSERT INTO `operation_record` VALUES ('144', 'root', '8', '添加主机', 'ce27b214-ed3e-11e8-bd3f-80c5f2966cd8', 'True', '2018-11-21 11:37:44', '2018-11-21 11:37:43');
INSERT INTO `operation_record` VALUES ('145', 'root', '8', '添加主机', '7a766ede-ed3f-11e8-9cd7-80c5f2966cd8', 'True', '2018-11-21 11:42:33', '2018-11-21 11:42:32');
INSERT INTO `operation_record` VALUES ('146', 'root', '8', '删除主机', '32b0a4a2-ed54-11e8-95e2-80c5f2966cd8', 'True', '2018-11-21 14:10:52', '2018-11-21 14:10:51');
INSERT INTO `operation_record` VALUES ('147', 'root', '8', '添加主机', '44a181f0-ed54-11e8-892a-80c5f2966cd8', 'True', '2018-11-21 14:11:22', '2018-11-21 14:11:21');
INSERT INTO `operation_record` VALUES ('148', 'root', '8', '添加主机', '15b52dac-ed55-11e8-b5ca-80c5f2966cd8', 'True', '2018-11-21 14:17:13', '2018-11-21 14:17:12');
INSERT INTO `operation_record` VALUES ('149', 'root', '8', '添加主机', '6295990a-ed55-11e8-a17a-80c5f2966cd8', 'True', '2018-11-21 14:19:22', '2018-11-21 14:19:21');
INSERT INTO `operation_record` VALUES ('150', 'root', '8', '更新主机详情', '909cb6a4-ed55-11e8-bd7b-80c5f2966cd8', 'True', '2018-11-21 14:20:39', '2018-11-21 14:20:38');

-- ----------------------------
-- Table structure for `opertion_minions`
-- ----------------------------
DROP TABLE IF EXISTS `opertion_minions`;
CREATE TABLE `opertion_minions` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `target_ids` varchar(40) NOT NULL,
  `minion_id` varchar(100) DEFAULT NULL,
  `edit_before` varchar(100) DEFAULT NULL COMMENT '修改前内容',
  `edit_after` varchar(100) DEFAULT NULL COMMENT '修改后内容',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `remark` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fogn_key_target_ids` (`target_ids`),
  CONSTRAINT `fogn_key_target_ids` FOREIGN KEY (`target_ids`) REFERENCES `operation_record` (`target_ids`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of opertion_minions
-- ----------------------------
INSERT INTO `opertion_minions` VALUES ('8', 'c48b37a4-f697-11e7-991b-e4a471e21cf0', 'dddd', null, null, '2018-01-11 14:22:15', '没有目标主机');
INSERT INTO `opertion_minions` VALUES ('9', 'efa40698-f697-11e7-97c5-e4a471e21cf0', 'ddd', null, null, '2018-01-11 14:23:27', '没有目标主机');
INSERT INTO `opertion_minions` VALUES ('10', '116cd7b6-f698-11e7-9ed7-e4a471e21cf0', 'None', null, null, '2018-01-11 14:24:24', 'None');
INSERT INTO `opertion_minions` VALUES ('11', '3bc3075e-f698-11e7-913d-e4a471e21cf0', 'asdfasf', null, null, '2018-01-11 14:25:35', 'None');
INSERT INTO `opertion_minions` VALUES ('15', 'd25c113a-f740-11e7-b671-e4a471e21cf0', 'ad', 'None', 'None', '2018-01-12 10:32:23', 'None');
INSERT INTO `opertion_minions` VALUES ('16', '809d0dd4-f742-11e7-a799-e4a471e21cf0', 'windows10_app3', '不分组', '新组', '2018-01-12 10:44:25', 'None');
INSERT INTO `opertion_minions` VALUES ('17', '809d0dd4-f742-11e7-a799-e4a471e21cf0', 'windows10_app3', 'addddddddddddd', 'addddddddd', '2018-01-12 10:44:26', 'None');
INSERT INTO `opertion_minions` VALUES ('18', '9585b822-f742-11e7-a8c4-e4a471e21cf0', 'windows10_app', 'Ubuntu', 'RedHat', '2018-01-12 10:45:00', 'None');
INSERT INTO `opertion_minions` VALUES ('19', '9585b822-f742-11e7-a8c4-e4a471e21cf0', 'windows10_app', 'addddddddd', 'addd', '2018-01-12 10:45:00', 'None');
INSERT INTO `opertion_minions` VALUES ('20', '9585b822-f742-11e7-a8c4-e4a471e21cf0', 'windows10_app', '38022', '22', '2018-01-12 10:45:00', 'None');
INSERT INTO `opertion_minions` VALUES ('21', '9585b822-f742-11e7-a8c4-e4a471e21cf0', 'windows10_app', 'windows10_app3', 'windows10_app', '2018-01-12 10:45:01', 'None');
INSERT INTO `opertion_minions` VALUES ('22', '9585b822-f742-11e7-a8c4-e4a471e21cf0', 'windows10_app', '新组', '新组2', '2018-01-12 10:45:01', 'None');
INSERT INTO `opertion_minions` VALUES ('23', 'c9c6e4e4-f74c-11e7-8fef-e4a471e21cf0', 'as', 'None', 'None', '2018-01-12 11:58:03', '删除主机');
INSERT INTO `opertion_minions` VALUES ('24', 'e8481f82-f74c-11e7-a99a-e4a471e21cf0', 'ip', 'None', 'None', '2018-01-12 11:58:54', '删除主机');
INSERT INTO `opertion_minions` VALUES ('25', '1b9b5024-f74e-11e7-87ff-e4a471e21cf0', '172.17.39.208_windows10_app', 'None', 'None', '2018-01-12 12:07:30', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('26', 'ec52aaf8-f750-11e7-baed-e4a471e21cf0', 'docker_images_minion1', 'None', 'None', '2018-01-12 12:27:39', '更新操作失败');
INSERT INTO `opertion_minions` VALUES ('27', '10d67a4c-f751-11e7-82ab-e4a471e21cf0', 'docker_images_minion1', 'None', 'None', '2018-01-12 12:28:40', '更新操作失败未能连接到指定的miniondocker_images_minion1');
INSERT INTO `opertion_minions` VALUES ('28', 'd91b74d0-f75d-11e7-b5ce-e4a471e21cf0', '127000', 'None', 'None', '2018-01-12 14:00:10', '将主机添加到组中新组2');
INSERT INTO `opertion_minions` VALUES ('29', 'd91b74d0-f75d-11e7-b5ce-e4a471e21cf0', '172.17.39.96', 'None', 'None', '2018-01-12 14:00:10', '将主机添加到组中新组2');
INSERT INTO `opertion_minions` VALUES ('30', 'd91b74d0-f75d-11e7-b5ce-e4a471e21cf0', '192.168.153.1363', 'None', 'None', '2018-01-12 14:00:10', '将主机添加到组中新组2');
INSERT INTO `opertion_minions` VALUES ('31', 'a87d47e4-f75e-11e7-9568-e4a471e21cf0', '测试', 'None', 'None', '2018-01-12 14:05:58', '测试:已添加成功');
INSERT INTO `opertion_minions` VALUES ('32', 'bf81d09a-f75e-11e7-8bfe-e4a471e21cf0', '测试2', 'None', 'None', '2018-01-12 14:06:37', '测试2:已添加成功');
INSERT INTO `opertion_minions` VALUES ('33', 'afcdc390-f766-11e7-9e5e-e4a471e21cf0', '172.17.0.1', 'None', 'None', '2018-01-12 15:03:26', '将主机添加db组中');
INSERT INTO `opertion_minions` VALUES ('48', '5cb5c128-f769-11e7-843d-e4a471e21cf0', '172.17.39.208_windows10_app', 'None', 'None', '2018-01-12 15:22:35', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('49', '5cc35f90-f769-11e7-8217-e4a471e21cf0', 'docker_images_minion1', 'None', 'None', '2018-01-12 15:22:35', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('50', '7548fdfe-f773-11e7-9aab-e4a471e21cf0', 'ss', 'None', 'None', '2018-01-12 16:34:51', '上传文件D:\\Program Files\\Python_Workspace\\test_ui\\upload\\manifest.json');
INSERT INTO `opertion_minions` VALUES ('51', 'ae450702-de41-11e8-9f96-80c5f2966cd8', 'windows10_app11', '192.168.153.1361', '192.168.213.129', '2018-11-02 09:50:31', '修改主机');
INSERT INTO `opertion_minions` VALUES ('52', '0e74df12-de44-11e8-a93a-80c5f2966cd8', 'windows', 'windows10_app11', 'windows', '2018-11-02 10:07:31', '修改主机');
INSERT INTO `opertion_minions` VALUES ('53', '1807dad4-de44-11e8-abc8-80c5f2966cd8', '192.168.216.129', '172.17.39.208_windows10_app', '192.168.216.129', '2018-11-02 10:07:47', '修改主机');
INSERT INTO `opertion_minions` VALUES ('54', '8602c0ba-de4a-11e8-93b7-80c5f2966cd8', '192.168.213.129', 'None', 'None', '2018-11-02 10:53:49', '将主机添加192.168.213.129,db组中');
INSERT INTO `opertion_minions` VALUES ('55', '8602c0ba-de4a-11e8-93b7-80c5f2966cd8', '172.17.39.2089', 'None', 'None', '2018-11-02 10:53:49', '将主机添加172.17.39.2089,db组中');
INSERT INTO `opertion_minions` VALUES ('56', '9bd023d8-de4b-11e8-8057-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-02 11:01:35', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('57', 'fb9ec62e-de4b-11e8-9fb4-80c5f2966cd8', 'this is a', '127000', '192.168.77.16', '2018-11-02 11:04:16', '修改主机');
INSERT INTO `opertion_minions` VALUES ('58', '267eac28-de4c-11e8-980d-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-02 11:05:27', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('59', '7037251e-de4c-11e8-ad73-80c5f2966cd8', 'windows', '38022', '22', '2018-11-02 11:07:31', '修改主机');
INSERT INTO `opertion_minions` VALUES ('60', '7037251e-de4c-11e8-ad73-80c5f2966cd8', 'windows', 'Fedora', 'Linux', '2018-11-02 11:07:31', '修改主机');
INSERT INTO `opertion_minions` VALUES ('61', '7fc8cf64-de4c-11e8-b19a-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-02 11:07:57', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('62', '7fca84da-de4c-11e8-839f-80c5f2966cd8', 'windows', '更新主机详情', 'None', '2018-11-02 11:07:57', 'None');
INSERT INTO `opertion_minions` VALUES ('63', '036150e4-de4d-11e8-8389-80c5f2966cd8', '192.168.216.129_web1', '172.17.39.2089', '192.168.216.129', '2018-11-02 11:11:38', '修改主机');
INSERT INTO `opertion_minions` VALUES ('64', '036150e4-de4d-11e8-8389-80c5f2966cd8', '192.168.216.129_web1', '192.168.216.129', '192.168.216.129_web1', '2018-11-02 11:11:38', '修改主机');
INSERT INTO `opertion_minions` VALUES ('65', '12a44e7e-de4d-11e8-9623-80c5f2966cd8', '192.168.216.128', '192.168.213.129', '192.168.213.128', '2018-11-02 11:12:04', '修改主机');
INSERT INTO `opertion_minions` VALUES ('66', '12a44e7e-de4d-11e8-9623-80c5f2966cd8', '192.168.216.128', 'Linux', 'Others', '2018-11-02 11:12:04', '修改主机');
INSERT INTO `opertion_minions` VALUES ('67', '12a44e7e-de4d-11e8-9623-80c5f2966cd8', '192.168.216.128', 'windows', '192.168.216.128', '2018-11-02 11:12:04', '修改主机');
INSERT INTO `opertion_minions` VALUES ('68', '2ab31b74-de4d-11e8-8b5e-80c5f2966cd8', 'windows1', '127000', '22', '2018-11-02 11:12:44', '修改主机');
INSERT INTO `opertion_minions` VALUES ('69', '2ab31b74-de4d-11e8-8b5e-80c5f2966cd8', 'windows1', 'Ubuntu', 'CentOS', '2018-11-02 11:12:44', '修改主机');
INSERT INTO `opertion_minions` VALUES ('70', '2ab31b74-de4d-11e8-8b5e-80c5f2966cd8', 'windows1', '新组2', 'web组', '2018-11-02 11:12:44', '修改主机');
INSERT INTO `opertion_minions` VALUES ('71', '2ab31b74-de4d-11e8-8b5e-80c5f2966cd8', 'windows1', 'this is a', 'windows1', '2018-11-02 11:12:44', '修改主机');
INSERT INTO `opertion_minions` VALUES ('72', '9a5a7d68-de4d-11e8-b11e-80c5f2966cd8', 'windows10_app', '192.168.153.1363', '192.168.153.17', '2018-11-02 11:15:51', '修改主机');
INSERT INTO `opertion_minions` VALUES ('73', 'a4b2b642-de4d-11e8-87ff-80c5f2966cd8', '192.168.216.129_web1', 'bbb', 'EC', '2018-11-02 11:16:09', '修改主机');
INSERT INTO `opertion_minions` VALUES ('74', 'af5a3f0a-de4d-11e8-a136-80c5f2966cd8', '192.168.216.129_web1', 'bbb', '22', '2018-11-02 11:16:27', '修改主机');
INSERT INTO `opertion_minions` VALUES ('75', 'b56fc4f8-de4d-11e8-a4cf-80c5f2966cd8', 'windows1', '127000', 'hostEC_MY', '2018-11-02 11:16:37', '修改主机');
INSERT INTO `opertion_minions` VALUES ('76', 'c398d4e2-de4d-11e8-ac2d-80c5f2966cd8', '172.17.39.96_web1_centos7_2', '177', '38022', '2018-11-02 11:17:01', '修改主机');
INSERT INTO `opertion_minions` VALUES ('77', 'c802ce94-de4d-11e8-9d1f-80c5f2966cd8', 'windows1', 'hostEC_MY', 'hostEC_MY1', '2018-11-02 11:17:08', '修改主机');
INSERT INTO `opertion_minions` VALUES ('78', 'c802ce94-de4d-11e8-9d1f-80c5f2966cd8', 'windows1', 'EC_MY', 'EC_MY1', '2018-11-02 11:17:08', '修改主机');
INSERT INTO `opertion_minions` VALUES ('79', 'd378b398-de4d-11e8-9a50-80c5f2966cd8', '192.168.216.129_web1', 'hostEC', 'hostEC3', '2018-11-02 11:17:27', '修改主机');
INSERT INTO `opertion_minions` VALUES ('80', 'd378b398-de4d-11e8-9a50-80c5f2966cd8', '192.168.216.129_web1', 'Debian', 'CentOS', '2018-11-02 11:17:27', '修改主机');
INSERT INTO `opertion_minions` VALUES ('81', 'd378b398-de4d-11e8-9a50-80c5f2966cd8', '192.168.216.129_web1', 'EC', 'EC3', '2018-11-02 11:17:27', '修改主机');
INSERT INTO `opertion_minions` VALUES ('82', 'dd50d078-de4d-11e8-bb73-80c5f2966cd8', '192.168.216.129_web1', 'hostEC3', 'host_EC3', '2018-11-02 11:17:44', '修改主机');
INSERT INTO `opertion_minions` VALUES ('83', 'e3558990-de4d-11e8-9b7c-80c5f2966cd8', '192.168.216.129_web1', 'EC3', 'EC_MY3', '2018-11-02 11:17:54', '修改主机');
INSERT INTO `opertion_minions` VALUES ('84', 'ecb0451e-de4d-11e8-ad07-80c5f2966cd8', '192.168.216.129_web1', 'host_EC3', 'host_ECMY3', '2018-11-02 11:18:09', '修改主机');
INSERT INTO `opertion_minions` VALUES ('85', 'f2a4c394-de4d-11e8-a4f7-80c5f2966cd8', '192.168.216.129_web1', 'host_ECMY3', 'hostEC_MY3', '2018-11-02 11:18:19', '修改主机');
INSERT INTO `opertion_minions` VALUES ('86', 'fa9de842-de4d-11e8-a50e-80c5f2966cd8', 'windows1', 'CentOS', 'Windows', '2018-11-02 11:18:33', '修改主机');
INSERT INTO `opertion_minions` VALUES ('87', 'fffc67c2-de4d-11e8-8c24-80c5f2966cd8', 'windows', 'windows1', 'windows', '2018-11-02 11:18:42', '修改主机');
INSERT INTO `opertion_minions` VALUES ('88', 'eb98ef70-de4f-11e8-8756-80c5f2966cd8', '192.168.216.129_web1', 'db组', 'web组', '2018-11-02 11:32:27', '修改主机');
INSERT INTO `opertion_minions` VALUES ('89', 'be9ee898-de50-11e8-bc2f-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-02 11:38:21', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('90', 'da67f986-de50-11e8-8d8b-80c5f2966cd8', '192.168.168.129_web1', '192.168.216.129_web1', '192.168.168.129_web1', '2018-11-02 11:39:07', '修改主机');
INSERT INTO `opertion_minions` VALUES ('91', 'e6c9df5c-de50-11e8-95e4-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-02 11:39:28', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('92', 'ed1b5dfe-de50-11e8-82ab-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-02 11:39:39', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('93', 'ed1c808c-de50-11e8-a17e-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-02 11:39:39', '执行salt命令:test.ping参数或者');
INSERT INTO `opertion_minions` VALUES ('94', 'd37aabf0-e8a2-11e8-b608-80c5f2966cd8', '192.168.77.16', 'None', 'None', '2018-11-15 14:51:06', '删除主机');
INSERT INTO `opertion_minions` VALUES ('95', '7c98538c-e8a4-11e8-b4d2-80c5f2966cd8', '192.168.216.128', 'None', 'None', '2018-11-15 15:02:59', '删除salt_key192.168.216.128');
INSERT INTO `opertion_minions` VALUES ('96', 'cb30a3c6-e8a4-11e8-8a7b-80c5f2966cd8', '192.168.216.128', '192.168.213.128', '192.168.216.128', '2018-11-15 15:05:11', '修改主机');
INSERT INTO `opertion_minions` VALUES ('97', '83869188-e8a5-11e8-a710-80c5f2966cd8', 'windows', '192.168.153.17', '192.168.1.11', '2018-11-15 15:10:20', '修改主机');
INSERT INTO `opertion_minions` VALUES ('98', '83869188-e8a5-11e8-a710-80c5f2966cd8', 'windows', 'windows10_app', 'windows', '2018-11-15 15:10:20', '修改主机');
INSERT INTO `opertion_minions` VALUES ('99', '92b10212-e8a5-11e8-b4d9-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-15 15:10:46', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('100', 'bb7512de-e8a5-11e8-8b6e-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-15 15:11:54', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('101', '091992e8-e8a6-11e8-ac7c-80c5f2966cd8', 'windows', 'RedHat', 'Windows', '2018-11-15 15:14:04', '修改主机');
INSERT INTO `opertion_minions` VALUES ('102', '5b528ae4-e8aa-11e8-8bbf-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-15 15:45:00', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('103', '5b573c5c-e8aa-11e8-a1fe-80c5f2966cd8', '192.168.168.129_web1', '更新主机详情', 'None', '2018-11-15 15:45:00', 'None');
INSERT INTO `opertion_minions` VALUES ('104', '9454c75c-e8aa-11e8-bcb6-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-15 15:46:36', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('105', '94569858-e8aa-11e8-812b-80c5f2966cd8', 'windows', '更新主机详情', 'None', '2018-11-15 15:46:36', 'None');
INSERT INTO `opertion_minions` VALUES ('106', 'c9fa2086-e94d-11e8-9fd9-80c5f2966cd8', '172.17.39.96_web1_centos7_2', 'None', 'None', '2018-11-16 11:14:54', '项目EC_MY命令git log -2 执行成功');
INSERT INTO `opertion_minions` VALUES ('107', 'c9fa2086-e94d-11e8-9fd9-80c5f2966cd8', '192.168.174.133_web1', 'None', 'None', '2018-11-16 11:14:54', '项目EC_MY命令git log -2 执行成功');
INSERT INTO `opertion_minions` VALUES ('108', 'ebf0e710-e94d-11e8-88f5-80c5f2966cd8', 'docker_images_minion4', 'None', 'None', '2018-11-16 11:15:51', '项目OMS命令git log -2 执行成功');
INSERT INTO `opertion_minions` VALUES ('109', 'ebf0e710-e94d-11e8-88f5-80c5f2966cd8', 'docker_images_minion2', 'None', 'None', '2018-11-16 11:15:51', '项目OMS命令git log -2 执行成功');
INSERT INTO `opertion_minions` VALUES ('110', 'ebf0e710-e94d-11e8-88f5-80c5f2966cd8', 'docker_images_minion3', 'None', 'None', '2018-11-16 11:15:51', '项目OMS命令git log -2 执行成功');
INSERT INTO `opertion_minions` VALUES ('111', 'b572a5cc-e94f-11e8-95a7-80c5f2966cd8', '172.17.39.96_web1_centos7_2', 'None', 'None', '2018-11-16 11:28:39', '项目EC_MY命令git log 1 执行成功');
INSERT INTO `opertion_minions` VALUES ('112', 'b572a5cc-e94f-11e8-95a7-80c5f2966cd8', '192.168.174.133_web1', 'None', 'None', '2018-11-16 11:28:39', '项目EC_MY命令git log 1 执行成功');
INSERT INTO `opertion_minions` VALUES ('113', 'dddc40e2-e969-11e8-be29-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-16 14:35:53', '更新操作失败未能连接到指定的minion192.168.168.129_web1');
INSERT INTO `opertion_minions` VALUES ('114', 'f4803826-ec91-11e8-98d3-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-20 15:00:25', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('115', 'f483ed52-ec91-11e8-a1d0-80c5f2966cd8', '192.168.168.129_web1', '更新主机详情', 'None', '2018-11-20 15:00:25', 'None');
INSERT INTO `opertion_minions` VALUES ('116', 'b4a33fc8-ed37-11e8-8b8e-80c5f2966cd8', '192.16.8.2', 'None', 'None', '2018-11-21 10:46:54', '删除主机');
INSERT INTO `opertion_minions` VALUES ('117', '2e45a50c-ed39-11e8-8d2f-80c5f2966cd8', '192.16.8.2', 'None', 'None', '2018-11-21 10:57:28', '删除主机');
INSERT INTO `opertion_minions` VALUES ('118', '982ccb1a-ed39-11e8-8bae-80c5f2966cd8', '192.168.168.129_web1', '1', '192.168.168.129_web1', '2018-11-21 11:00:25', '修改主机');
INSERT INTO `opertion_minions` VALUES ('119', '982ccb1a-ed39-11e8-8bae-80c5f2966cd8', '192.168.168.129_web1', '2', 'Others', '2018-11-21 11:00:25', '修改主机');
INSERT INTO `opertion_minions` VALUES ('120', '982ccb1a-ed39-11e8-8bae-80c5f2966cd8', '192.168.168.129_web1', '192.16.8.2', '192.168.216.128', '2018-11-21 11:00:25', '修改主机');
INSERT INTO `opertion_minions` VALUES ('121', '9e3323d0-ed39-11e8-95ae-80c5f2966cd8', '192.168.168.129_web1', '192.168.216.128', '192.168.216.129', '2018-11-21 11:00:35', '修改主机');
INSERT INTO `opertion_minions` VALUES ('122', 'ebd69840-ed39-11e8-95eb-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:02:46', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('123', '1251530c-ed3a-11e8-8219-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-21 11:03:50', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('124', '1253f928-ed3a-11e8-9425-80c5f2966cd8', '192.168.168.129_web1', '更新主机详情', 'None', '2018-11-21 11:03:50', 'None');
INSERT INTO `opertion_minions` VALUES ('125', '2094b208-ed3a-11e8-b765-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:04:14', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('126', '20969bda-ed3a-11e8-b833-80c5f2966cd8', 'windows', '更新主机详情', 'None', '2018-11-21 11:04:14', 'None');
INSERT INTO `opertion_minions` VALUES ('127', 'ec805118-ed3a-11e8-9871-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:09:56', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('128', 'ec822862-ed3a-11e8-b403-80c5f2966cd8', 'windows', '更新主机详情', 'None', '2018-11-21 11:09:56', 'None');
INSERT INTO `opertion_minions` VALUES ('129', '4d7be348-ed3b-11e8-8470-80c5f2966cd8', '192.168.168.129_web1', 'None', 'None', '2018-11-21 11:12:39', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('130', '4d7da11c-ed3b-11e8-85c9-80c5f2966cd8', '192.168.168.129_web1', '更新主机详情', 'None', '2018-11-21 11:12:39', 'None');
INSERT INTO `opertion_minions` VALUES ('131', '57de0b28-ed3b-11e8-9fc7-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:12:56', '更新主机详情');
INSERT INTO `opertion_minions` VALUES ('132', '57df7b5c-ed3b-11e8-bcd8-80c5f2966cd8', 'windows', '更新主机详情', 'None', '2018-11-21 11:12:56', 'None');
INSERT INTO `opertion_minions` VALUES ('133', 'a5bd5476-ed3c-11e8-976a-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:22:16', '删除主机');
INSERT INTO `opertion_minions` VALUES ('134', 'd9380b92-ed3c-11e8-a74c-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:23:43', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('135', '0422a0ee-ed3d-11e8-b9b8-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:24:55', '删除主机');
INSERT INTO `opertion_minions` VALUES ('136', '0c13a828-ed3d-11e8-9787-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:25:08', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('137', '2fe34b22-ed3d-11e8-87f0-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:26:08', '删除主机');
INSERT INTO `opertion_minions` VALUES ('138', '422fd18c-ed3d-11e8-a702-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:26:39', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('139', '5f9e4cd8-ed3d-11e8-b6b1-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:27:28', '删除主机');
INSERT INTO `opertion_minions` VALUES ('140', '7d1042a2-ed3d-11e8-8204-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:28:18', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('141', '9579ce38-ed3d-11e8-83bf-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:28:59', '删除主机');
INSERT INTO `opertion_minions` VALUES ('142', 'a1f02930-ed3d-11e8-9e8e-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:29:20', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('143', '0ec8ed12-ed3e-11e8-94ba-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:32:22', '删除主机');
INSERT INTO `opertion_minions` VALUES ('144', '183a3546-ed3e-11e8-b11f-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:32:38', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('145', '61f78d90-ed3e-11e8-826e-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:34:42', '删除主机');
INSERT INTO `opertion_minions` VALUES ('146', '68c123b4-ed3e-11e8-b9b8-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:34:53', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('147', 'c5d370ca-ed3e-11e8-a800-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 11:37:29', '删除主机');
INSERT INTO `opertion_minions` VALUES ('148', 'ce27b214-ed3e-11e8-bd3f-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:37:43', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('149', '7a766ede-ed3f-11e8-9cd7-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 11:42:32', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('150', '32b0a4a2-ed54-11e8-95e2-80c5f2966cd8', '192.168.1.11', 'None', 'None', '2018-11-21 14:10:51', '删除主机');
INSERT INTO `opertion_minions` VALUES ('151', '44a181f0-ed54-11e8-892a-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 14:11:21', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('152', '15b52dac-ed55-11e8-b5ca-80c5f2966cd8', 'windows1', 'None', 'None', '2018-11-21 14:17:12', '添加主机windows1');
INSERT INTO `opertion_minions` VALUES ('153', '6295990a-ed55-11e8-a17a-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 14:19:21', '添加主机windows');
INSERT INTO `opertion_minions` VALUES ('154', '909cb6a4-ed55-11e8-bd7b-80c5f2966cd8', 'windows', 'None', 'None', '2018-11-21 14:20:38', '更新主机详情');

-- ----------------------------
-- Table structure for `project_manage`
-- ----------------------------
DROP TABLE IF EXISTS `project_manage`;
CREATE TABLE `project_manage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(50) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `center_path` varchar(50) NOT NULL,
  `dest_path` varchar(50) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of project_manage
-- ----------------------------
INSERT INTO `project_manage` VALUES ('261', 'EC_MY', '172.17.39.208', '/soft/projects/EC_MY', '/soft/EC_MY', '2017-12-21 16:46:36', '2017-12-21 16:46:36');
INSERT INTO `project_manage` VALUES ('262', 'EC_MY', 'ip', '/soft/projects/EC_MY', '/soft/EC_MY', '2017-12-21 16:46:36', '2017-12-21 16:46:36');
INSERT INTO `project_manage` VALUES ('263', 'EC_MY', '127000', '/soft/projects/EC_MY', '/soft/EC_MY', '2017-12-21 16:46:36', '2017-12-21 16:46:36');
INSERT INTO `project_manage` VALUES ('264', 'EC_MY', '172.17.39.96', '/soft/projects/EC_MY', '/soft/EC_MY', '2017-12-21 16:46:36', '2017-12-21 16:46:36');
INSERT INTO `project_manage` VALUES ('265', 'EC_MY', '192.168.174.133', '/soft/projects/EC_MY', '/soft/EC_MY', '2017-12-21 16:46:36', '2017-12-21 16:46:36');
INSERT INTO `project_manage` VALUES ('266', 'OMS', '172.17.0.7', '/soft/projects/OMS', '/opt/OMS', '2017-12-22 10:16:11', '2017-12-22 10:16:11');
INSERT INTO `project_manage` VALUES ('267', 'OMS', '172.17.0.2', '/soft/projects/OMS', '/opt/OMS', '2017-12-22 10:16:11', '2017-12-22 10:16:11');
INSERT INTO `project_manage` VALUES ('268', 'OMS', '172.17.0.3', '/soft/projects/OMS', '/opt/OMS', '2017-12-22 10:16:11', '2017-12-22 10:16:11');
INSERT INTO `project_manage` VALUES ('269', 'OMS', '172.17.0.4', '/soft/projects/OMS', '/opt/OMS', '2017-12-22 10:16:11', '2017-12-22 10:16:11');

-- ----------------------------
-- Table structure for `salt_host_details`
-- ----------------------------
DROP TABLE IF EXISTS `salt_host_details`;
CREATE TABLE `salt_host_details` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(40) NOT NULL,
  `minion_id` varchar(40) NOT NULL,
  `kernel` varchar(40) DEFAULT NULL,
  `osversion` varchar(40) DEFAULT NULL,
  `cpu_model` varchar(100) DEFAULT NULL,
  `num_cpus` int(5) DEFAULT NULL,
  `manufacturer` varchar(40) DEFAULT NULL,
  `osfullname` varchar(40) DEFAULT NULL,
  `mem_total` varchar(40) DEFAULT NULL,
  `windowsdomain` varchar(40) DEFAULT NULL,
  `fqdn` varchar(40) DEFAULT NULL,
  `os` varchar(40) DEFAULT NULL,
  `cpuarch` varchar(40) DEFAULT NULL,
  `roles` varchar(40) DEFAULT NULL,
  `osrelease` varchar(40) DEFAULT NULL,
  `kernelrelease` varchar(40) DEFAULT NULL,
  `saltversion` varchar(40) DEFAULT NULL,
  `osmanufacturer` varchar(40) DEFAULT NULL,
  `saltpath` varchar(40) DEFAULT NULL,
  `timezone` varchar(40) DEFAULT NULL,
  `os_family` varchar(40) DEFAULT NULL,
  `shell` varchar(40) DEFAULT NULL,
  `username` varchar(40) DEFAULT NULL,
  `domain` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`uid`,`ip`),
  UNIQUE KEY `minion_id_idx` (`minion_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of salt_host_details
-- ----------------------------
INSERT INTO `salt_host_details` VALUES ('8', '192.168.216.129', '192.168.168.129_web1', 'Linux', 'undefined', 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz', '1', 'VMware, Inc.', 'CentOS Linux', '1853', 'undefined', 'client_host', 'CentOS', 'x86_64', 'undefined', '7.1.1503', '3.10.0-229.el7.x86_64', '2017.7.2', 'undefined', '/usr/lib/python2.7/site-packages/salt', 'undefined', 'RedHat', '/bin/sh', 'root', 'undefined');
INSERT INTO `salt_host_details` VALUES ('9', '192.168.1.11', 'windows', 'Windows', 'undefined', 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz', '8', 'ASUSTeK COMPUTER INC.', 'Microsoft Windows 10 教育版', '8071', 'undefined', 'DESKTOP-AM7NB6A', 'Windows', 'AMD64', 'undefined', '10', '10.0.17134', '2018.3.3', 'undefined', 'c:\\salt\\bin\\lib\\site-packages\\salt', 'undefined', 'Windows', 'C:\\WINDOWS\\system32\\cmd.exe', 'DESKTOP-AM7NB6A$', 'undefined');
INSERT INTO `salt_host_details` VALUES ('10', '999', 'windows1', 'Windows', 'undefined', 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz', '8', 'ASUSTeK COMPUTER INC.', 'Microsoft Windows 10 教育版', '8071', 'undefined', 'DESKTOP-AM7NB6A', 'Windows', 'AMD64', 'undefined', '10', '10.0.17134', '2018.3.3', 'undefined', 'c:\\salt\\bin\\lib\\site-packages\\salt', 'undefined', 'Windows', 'C:\\WINDOWS\\system32\\cmd.exe', 'DESKTOP-AM7NB6A$', 'undefined');

-- ----------------------------
-- Table structure for `service_manage`
-- ----------------------------
DROP TABLE IF EXISTS `service_manage`;
CREATE TABLE `service_manage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(30) CHARACTER SET utf8 NOT NULL,
  `service_name` varchar(100) DEFAULT NULL,
  `service_url` varchar(100) DEFAULT NULL,
  `path` varchar(150) DEFAULT NULL,
  `port` varchar(10) DEFAULT NULL,
  `cluster` varchar(10) DEFAULT NULL,
  `group` varchar(10) DEFAULT NULL,
  `status` int(5) DEFAULT NULL COMMENT '1为正常，0为不正常，3为未知状态',
  `remark` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `host_service` (`ip`) USING BTREE,
  CONSTRAINT `host_service` FOREIGN KEY (`ip`) REFERENCES `host` (`ip`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of service_manage
-- ----------------------------
INSERT INTO `service_manage` VALUES ('3', '192.168.216.129', 'apache', null, '/opt/apache/bin', '8001', null, null, null, null);
INSERT INTO `service_manage` VALUES ('6', '192.168.1.11', 'redis', null, '/opt/redis/bin', '6379', null, '无', null, null);
INSERT INTO `service_manage` VALUES ('7', '192.168.77.123', 'mysql', null, '/home/mysql/bin', '3006', null, '无', null, null);
INSERT INTO `service_manage` VALUES ('8', '999', 'test', null, '/home/test', '9', null, '无', null, null);
INSERT INTO `service_manage` VALUES ('9', '192.168.77.123', 'nginx', null, '/usr/local/nginx/bin', '8001', null, null, null, null);
INSERT INTO `service_manage` VALUES ('10', '192.168.77.123', 'httpd', null, '/usr/local/nginx/httpd/bin', '8080', null, null, null, null);
INSERT INTO `service_manage` VALUES ('11', '999', 'test', null, null, null, null, null, null, null);
INSERT INTO `service_manage` VALUES ('12', '192.168.1.11', 'ES', null, '/data/ES/bin', '9200', null, null, null, null);
INSERT INTO `service_manage` VALUES ('13', '192.168.1.11', 'kafka1', null, '/data/kafka/bin', '9020', 'true', null, null, null);
INSERT INTO `service_manage` VALUES ('14', '192.168.1.11', 'kafka2', null, '/data/kafka/bin', '9020', 'true', null, null, null);
INSERT INTO `service_manage` VALUES ('15', '192.168.1.11', 'kafka3', null, '/data/kafka/bin', '9020', 'true', null, null, null);
