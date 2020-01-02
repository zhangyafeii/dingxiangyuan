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

 Date: 02/01/2020 10:29:16
*/


-- ----------------------------
-- Table structure for posts_replies
-- ----------------------------
DROP TABLE IF EXISTS "public"."posts_replies";
CREATE TABLE "public"."posts_replies" (
  "floor" int4 NOT NULL,
  "topic_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "topic_title" varchar(255) COLLATE "pg_catalog"."default",
  "content" text COLLATE "pg_catalog"."default",
  "topic_type" varchar(255) COLLATE "pg_catalog"."default",
  "board_name" varchar(255) COLLATE "pg_catalog"."default",
  "author_name" varchar(255) COLLATE "pg_catalog"."default",
  "author_url" varchar(255) COLLATE "pg_catalog"."default",
  "post_time" timestamp(0),
  "reference_bool" int4,
  "author_level" varchar(255) COLLATE "pg_catalog"."default",
  "author_scores" int4,
  "author_votes" int4,
  "author_dingdang" int4,
  "browser_num" int4,
  "reply_num" int4,
  "vote_num" int4,
  "fav_num" int4,
  "reward_num" int4,
  "istopic" int4,
  "isgood" int4,
  "author_identify" varchar(255) COLLATE "pg_catalog"."default",
  "hot" int4,
  "author_identify_depart" varchar(255) COLLATE "pg_catalog"."default",
  "rate_get" int4
)
;

-- ----------------------------
-- Indexes structure for table posts_replies
-- ----------------------------
CREATE INDEX "主题帖url" ON "public"."posts_replies" USING btree (
  "topic_url" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "主题帖类型" ON "public"."posts_replies" USING btree (
  "topic_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "作者url" ON "public"."posts_replies" USING btree (
  "author_url" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "发布时间" ON "public"."posts_replies" USING btree (
  "post_time" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "所属板块" ON "public"."posts_replies" USING btree (
  "board_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table posts_replies
-- ----------------------------
ALTER TABLE "public"."posts_replies" ADD CONSTRAINT "posts_replies_pkey" PRIMARY KEY ("floor", "topic_url");
