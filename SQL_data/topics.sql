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

 Date: 02/01/2020 10:29:35
*/


-- ----------------------------
-- Table structure for topics
-- ----------------------------
DROP TABLE IF EXISTS "public"."topics";
CREATE TABLE "public"."topics" (
  "topic_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "topic_title" varchar(1000) COLLATE "pg_catalog"."default",
  "board_id" int4,
  "board_name" varchar(255) COLLATE "pg_catalog"."default",
  "author_name" varchar(255) COLLATE "pg_catalog"."default",
  "author_url" varchar(255) COLLATE "pg_catalog"."default",
  "post_time" date,
  "reply_num" int4,
  "click_num" int4,
  "last_reply_time" timestamp(6),
  "good_topic" int4,
  "recommend_topic" int4,
  "award_topic" int4,
  "case_topic" int4
)
;

-- ----------------------------
-- Primary Key structure for table topics
-- ----------------------------
ALTER TABLE "public"."topics" ADD CONSTRAINT "topics_pkey" PRIMARY KEY ("topic_url");
