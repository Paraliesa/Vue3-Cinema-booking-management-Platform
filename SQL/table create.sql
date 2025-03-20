/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80028 (8.0.28)
 Source Host           : localhost:3306
 Source Schema         : test_db

 Target Server Type    : MySQL
 Target Server Version : 80028 (8.0.28)
 File Encoding         : 65001

 Date: 30/12/2024 10:47:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cinema
-- ----------------------------
DROP TABLE IF EXISTS `cinema`;
CREATE TABLE `cinema`  (
  `cid` bigint NOT NULL AUTO_INCREMENT,
  `cname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`cid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for film_arrangement
-- ----------------------------
DROP TABLE IF EXISTS `film_arrangement`;
CREATE TABLE `film_arrangement`  (
  `fid` bigint NOT NULL AUTO_INCREMENT,
  `fstarttime` datetime(6) NOT NULL,
  `fendtime` datetime(6) NOT NULL,
  `fcost` bigint NOT NULL,
  `cid_id` bigint NOT NULL,
  `hid_id` bigint NOT NULL,
  `mid_id` bigint NOT NULL,
  `seatid_id` bigint NOT NULL,
  `f_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`fid`) USING BTREE,
  INDEX `film_arrangement_seatid_id_02276f33_fk`(`seatid_id` ASC) USING BTREE,
  INDEX `film_arrangement_cid_id_e09a2a25_fk`(`cid_id` ASC) USING BTREE,
  INDEX `film_arrangement_hid_id_0859a1c4_fk`(`hid_id` ASC) USING BTREE,
  INDEX `film_arrangement_mid_id_21cfc40a_fk`(`mid_id` ASC) USING BTREE,
  CONSTRAINT `film_arrangement_cid_id_e09a2a25_fk` FOREIGN KEY (`cid_id`) REFERENCES `cinema` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `film_arrangement_hid_id_0859a1c4_fk` FOREIGN KEY (`hid_id`) REFERENCES `hall` (`hid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `film_arrangement_mid_id_21cfc40a_fk` FOREIGN KEY (`mid_id`) REFERENCES `movie` (`mid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `film_arrangement_seatid_id_02276f33_fk` FOREIGN KEY (`seatid_id`) REFERENCES `seat` (`seatid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 80000024 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for hall
-- ----------------------------
DROP TABLE IF EXISTS `hall`;
CREATE TABLE `hall`  (
  `hid` bigint NOT NULL AUTO_INCREMENT,
  `hname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cid_id` bigint NOT NULL,
  `sid_id` bigint NOT NULL,
  `h_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`hid`) USING BTREE,
  INDEX `hall_cid_id_f1be4775_fk`(`cid_id` ASC) USING BTREE,
  INDEX `hall_sid_id_41648fa4_fk`(`sid_id` ASC) USING BTREE,
  CONSTRAINT `hall_cid_id_f1be4775_fk` FOREIGN KEY (`cid_id`) REFERENCES `cinema` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `hall_sid_id_41648fa4_fk` FOREIGN KEY (`sid_id`) REFERENCES `seat_model` (`sid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 50021 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie`  (
  `mid` bigint NOT NULL AUTO_INCREMENT,
  `mtime` bigint NOT NULL,
  `mname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mhot` bigint NOT NULL,
  `mscore` double NOT NULL,
  `myear` date NOT NULL,
  `mtext` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `pid_id` bigint NOT NULL,
  `tid_id` bigint NOT NULL,
  `m_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`mid`) USING BTREE,
  INDEX `movie_pid_id_fc43f6f2_fk`(`pid_id` ASC) USING BTREE,
  INDEX `movie_tid_id_76ae88dd_fk`(`tid_id` ASC) USING BTREE,
  CONSTRAINT `movie_pid_id_fc43f6f2_fk` FOREIGN KEY (`pid_id`) REFERENCES `place` (`pid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `movie_tid_id_76ae88dd_fk` FOREIGN KEY (`tid_id`) REFERENCES `type` (`tid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 200006 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `oid` bigint NOT NULL AUTO_INCREMENT,
  `otime` datetime(6) NOT NULL,
  `fid_id` bigint NOT NULL,
  `uid_id` bigint NOT NULL,
  `oprice` bigint NOT NULL,
  `oseats` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`oid`) USING BTREE,
  INDEX `orders_fid_id_c85c4592_fk`(`fid_id` ASC) USING BTREE,
  INDEX `orders_uid_id_9b7f6984_fk`(`uid_id` ASC) USING BTREE,
  CONSTRAINT `orders_fid_id_c85c4592_fk` FOREIGN KEY (`fid_id`) REFERENCES `film_arrangement` (`fid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_uid_id_9b7f6984_fk` FOREIGN KEY (`uid_id`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 90000039 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for place
-- ----------------------------
DROP TABLE IF EXISTS `place`;
CREATE TABLE `place`  (
  `pid` bigint NOT NULL AUTO_INCREMENT,
  `pname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`pid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for seat
-- ----------------------------
DROP TABLE IF EXISTS `seat`;
CREATE TABLE `seat`  (
  `seatid` bigint NOT NULL AUTO_INCREMENT,
  `seats` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sid_id` bigint NOT NULL,
  PRIMARY KEY (`seatid`) USING BTREE,
  INDEX `seat_sid_id_fb97fb53_fk`(`sid_id` ASC) USING BTREE,
  CONSTRAINT `seat_sid_id_fb97fb53_fk` FOREIGN KEY (`sid_id`) REFERENCES `seat_model` (`sid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 40021 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for seat_model
-- ----------------------------
DROP TABLE IF EXISTS `seat_model`;
CREATE TABLE `seat_model`  (
  `sid` bigint NOT NULL AUTO_INCREMENT,
  `smodel` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`sid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for type
-- ----------------------------
DROP TABLE IF EXISTS `type`;
CREATE TABLE `type`  (
  `tid` bigint NOT NULL AUTO_INCREMENT,
  `tname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`tid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `utype` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `uid` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ugender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `uphone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `upassword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
