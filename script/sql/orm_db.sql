/*
 Navicat Premium Dump SQL

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80407 (8.4.7)
 Source Host           : localhost:3306
 Source Schema         : orm_db

 Target Server Type    : MySQL
 Target Server Version : 80407 (8.4.7)
 File Encoding         : 65001

 Date: 16/12/2025 15:17:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '图书ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图书标题',
  `author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作者',
  `genre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型(古典名著/武侠小说)',
  `era` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '年代/背景时代',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title` ASC) USING BTREE,
  INDEX `ix_books_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of books
-- ----------------------------
INSERT INTO `books` VALUES (1, '《红楼梦》', '曹雪芹', '古典名著', '清朝');
INSERT INTO `books` VALUES (2, '《三国演义》', '罗贯中', '古典名著', '明朝');
INSERT INTO `books` VALUES (3, '《水浒传》', '施耐庵', '古典名著', '元末明初');
INSERT INTO `books` VALUES (4, '《西游记》', '吴承恩', '古典名著', '明朝');
INSERT INTO `books` VALUES (5, '《射雕英雄传》', '金庸', '武侠小说', '南宋');
INSERT INTO `books` VALUES (6, '《神雕侠侣》', '金庸', '武侠小说', '南宋');
INSERT INTO `books` VALUES (7, '《倚天屠龙记》', '金庸', '武侠小说', '元末明初');
INSERT INTO `books` VALUES (8, '《天龙八部》', '金庸', '武侠小说', '北宋');
INSERT INTO `books` VALUES (9, '《笑傲江湖》', '金庸', '武侠小说', '明朝（架空）');
INSERT INTO `books` VALUES (10, '《鹿鼎记》', '金庸', '武侠小说', '清朝');
INSERT INTO `books` VALUES (11, '《书剑恩仇录》', '金庸', '武侠小说', '清朝');
INSERT INTO `books` VALUES (12, '《侠客行》', '金庸', '武侠小说', '明朝');
INSERT INTO `books` VALUES (13, '《连城诀》', '金庸', '武侠小说', '清朝');
INSERT INTO `books` VALUES (14, '《雪山飞狐》', '金庸', '武侠小说', '清朝');
INSERT INTO `books` VALUES (15, '《飞狐外传》', '金庸', '武侠小说', '清朝');
INSERT INTO `books` VALUES (16, '《雷雨》', '曹禺', '戏剧', '现代');

-- ----------------------------
-- Table structure for characters
-- ----------------------------
DROP TABLE IF EXISTS `characters`;
CREATE TABLE `characters`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `role_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色类型',
  `book_id` int NOT NULL COMMENT '图书ID',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `book_id`(`book_id` ASC) USING BTREE,
  INDEX `ix_characters_id`(`id` ASC) USING BTREE,
  CONSTRAINT `characters_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 58 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of characters
-- ----------------------------
INSERT INTO `characters` VALUES (1, '贾宝玉', '男', '主角', 1);
INSERT INTO `characters` VALUES (2, '林黛玉', '女', '主角', 1);
INSERT INTO `characters` VALUES (3, '薛宝钗', '女', '主角', 1);
INSERT INTO `characters` VALUES (4, '王熙凤', '女', '主要角色', 1);
INSERT INTO `characters` VALUES (5, '史湘云', '女', '金陵十二钗', 1);
INSERT INTO `characters` VALUES (6, '刘备', '男', '蜀汉君主', 2);
INSERT INTO `characters` VALUES (7, '关羽', '男', '五虎上将', 2);
INSERT INTO `characters` VALUES (8, '张飞', '男', '五虎上将', 2);
INSERT INTO `characters` VALUES (9, '诸葛亮', '男', '军师', 2);
INSERT INTO `characters` VALUES (10, '曹操', '男', '魏国奠基者', 2);
INSERT INTO `characters` VALUES (11, '宋江', '男', '梁山寨主', 3);
INSERT INTO `characters` VALUES (12, '武松', '男', '行者', 3);
INSERT INTO `characters` VALUES (13, '林冲', '男', '豹子头', 3);
INSERT INTO `characters` VALUES (14, '鲁智深', '男', '花和尚', 3);
INSERT INTO `characters` VALUES (15, '李逵', '男', '黑旋风', 3);
INSERT INTO `characters` VALUES (16, '孙悟空', '男', '主角', 4);
INSERT INTO `characters` VALUES (17, '唐僧', '男', '主角', 4);
INSERT INTO `characters` VALUES (18, '猪八戒', '男', '配角', 4);
INSERT INTO `characters` VALUES (19, '沙悟净', '男', '配角', 4);
INSERT INTO `characters` VALUES (20, '观音菩萨', '女', '神仙', 4);
INSERT INTO `characters` VALUES (21, '郭靖', '男', '主角', 5);
INSERT INTO `characters` VALUES (22, '黄蓉', '女', '主角', 5);
INSERT INTO `characters` VALUES (23, '杨康', '男', '主要反派', 5);
INSERT INTO `characters` VALUES (24, '洪七公', '男', '北丐', 5);
INSERT INTO `characters` VALUES (25, '黄药师', '男', '东邪', 5);
INSERT INTO `characters` VALUES (26, '杨过', '男', '主角', 6);
INSERT INTO `characters` VALUES (27, '小龙女', '女', '主角', 6);
INSERT INTO `characters` VALUES (28, '郭芙', '女', '配角', 6);
INSERT INTO `characters` VALUES (29, '李莫愁', '女', '反派', 6);
INSERT INTO `characters` VALUES (30, '张无忌', '男', '主角', 7);
INSERT INTO `characters` VALUES (31, '赵敏', '女', '主角', 7);
INSERT INTO `characters` VALUES (32, '周芷若', '女', '主要角色', 7);
INSERT INTO `characters` VALUES (33, '张三丰', '男', '武学宗师', 7);
INSERT INTO `characters` VALUES (34, '小昭', '女', '配角', 7);
INSERT INTO `characters` VALUES (35, '乔峰', '男', '主角', 8);
INSERT INTO `characters` VALUES (36, '段誉', '男', '主角', 8);
INSERT INTO `characters` VALUES (37, '虚竹', '男', '主角', 8);
INSERT INTO `characters` VALUES (38, '王语嫣', '女', '主要角色', 8);
INSERT INTO `characters` VALUES (39, '阿朱', '女', '配角', 8);
INSERT INTO `characters` VALUES (40, '令狐冲', '男', '主角', 9);
INSERT INTO `characters` VALUES (41, '任盈盈', '女', '主角', 9);
INSERT INTO `characters` VALUES (42, '岳不群', '男', '伪君子', 9);
INSERT INTO `characters` VALUES (43, '东方不败', '待定', '大反派', 9);
INSERT INTO `characters` VALUES (44, '韦小宝', '男', '主角', 10);
INSERT INTO `characters` VALUES (45, '康熙', '男', '皇帝', 10);
INSERT INTO `characters` VALUES (46, '陈近南', '男', '天地会总舵主', 10);
INSERT INTO `characters` VALUES (47, '双儿', '女', '主要伴侣', 10);
INSERT INTO `characters` VALUES (48, '陈家洛', '男', '主角', 11);
INSERT INTO `characters` VALUES (49, '霍青桐', '女', '主要角色', 11);
INSERT INTO `characters` VALUES (50, '石破天', '男', '主角', 12);
INSERT INTO `characters` VALUES (51, '丁当', '女', '主要角色', 12);
INSERT INTO `characters` VALUES (52, '狄云', '男', '主角', 13);
INSERT INTO `characters` VALUES (53, '戚芳', '女', '主要角色', 13);
INSERT INTO `characters` VALUES (54, '胡斐', '男', '主角', 14);
INSERT INTO `characters` VALUES (55, '苗若兰', '女', '主要角色', 14);
INSERT INTO `characters` VALUES (56, '袁紫衣', '女', '主要角色', 15);
INSERT INTO `characters` VALUES (57, '程灵素', '女', '主要角色', 15);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_users_phone`(`phone` ASC) USING BTREE,
  INDEX `ix_users_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '13812345678', 'testuser');

SET FOREIGN_KEY_CHECKS = 1;
