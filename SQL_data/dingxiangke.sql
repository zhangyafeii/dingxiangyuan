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

 Date: 02/01/2020 10:29:42
*/


-- ----------------------------
-- Table structure for dingxiangke
-- ----------------------------
DROP TABLE IF EXISTS "public"."dingxiangke";
CREATE TABLE "public"."dingxiangke" (
  "user_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "user_name" varchar(255) COLLATE "pg_catalog"."default",
  "posts" int4,
  "distilled" int4,
  "score" int4,
  "posts_voted" int4,
  "following" int4,
  "follower" int4,
  "dingdang" int4,
  "user_level" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "user_identify" varchar(255) COLLATE "pg_catalog"."default",
  "user_city" varchar(255) COLLATE "pg_catalog"."default",
  "posts_browsered" int4,
  "posts_faved" int4,
  "online_time" int4,
  "user_url_unquote" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Indexes structure for table dingxiangke
-- ----------------------------
CREATE INDEX "url解码" ON "public"."dingxiangke" USING btree (
  "user_url_unquote" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "用户url" ON "public"."dingxiangke" USING btree (
  "user_url" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dingxiangke
-- ----------------------------
ALTER TABLE "public"."dingxiangke" ADD CONSTRAINT "dingxiangke_pkey" PRIMARY KEY ("user_url", "user_url_unquote");
