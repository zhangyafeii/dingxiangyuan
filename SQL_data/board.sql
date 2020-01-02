/*
 Navicat Premium Data Transfer

 Source Server         : postgressql
 Source Server Type    : PostgreSQL
 Source Server Version : 120001
 Source Host           : localhost:5432
 Source Catalog        : dingxiangyuan
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120001
 File Encoding         : 65001

 Date: 02/01/2020 10:30:55
*/


-- ----------------------------
-- Table structure for board
-- ----------------------------
DROP TABLE IF EXISTS "public"."board";
CREATE TABLE "public"."board" (
  "board_id" int4 NOT NULL,
  "board_name" varchar COLLATE "pg_catalog"."default",
  "board_url" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "topic_num" int4,
  "moderator_url_list" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Primary Key structure for table board
-- ----------------------------
ALTER TABLE "public"."board" ADD CONSTRAINT "team_pkey" PRIMARY KEY ("board_id", "board_url");
