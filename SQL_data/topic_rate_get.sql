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

 Date: 02/01/2020 10:29:27
*/


-- ----------------------------
-- Table structure for topic_rate_get
-- ----------------------------
DROP TABLE IF EXISTS "public"."topic_rate_get";
CREATE TABLE "public"."topic_rate_get" (
  "topic_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "rate_get" int4,
  "topic_type" varchar(255) COLLATE "pg_catalog"."default",
  "board_name" varchar(255) COLLATE "pg_catalog"."default",
  "title_topic_type" varchar(255) COLLATE "pg_catalog"."default",
  "title_readility" numeric(20,6),
  "content_readility" numeric(20,6)
)
;

-- ----------------------------
-- Primary Key structure for table topic_rate_get
-- ----------------------------
ALTER TABLE "public"."topic_rate_get" ADD CONSTRAINT "topic_rate_get_pkey" PRIMARY KEY ("topic_url");
