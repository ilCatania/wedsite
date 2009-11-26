BEGIN;
CREATE TABLE "confirm_partyconfirmation" (
    "id" integer NOT NULL PRIMARY KEY,
    "date_confirmed" datetime NOT NULL,
    "hash_code" integer unsigned NOT NULL,
    "name" varchar(50) NOT NULL,
    "adults" integer unsigned NOT NULL,
    "children" integer unsigned NULL
)
;
CREATE TABLE "ipsecurity_loggedaction" (
    "ip_addr" varchar(20) NOT NULL PRIMARY KEY,
    "last_action" datetime NOT NULL,
    "action_count" integer unsigned NOT NULL,
    "banned" bool NOT NULL
)
;
CREATE TABLE "nav_section_translation" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "language_id" integer NOT NULL,
    "master_id" integer NOT NULL,
    UNIQUE ("language_id", "master_id")
)
;
CREATE TABLE "nav_section" (
    "id" integer NOT NULL PRIMARY KEY,
    "slug" varchar(12) NOT NULL,
    "order" integer NOT NULL,
    "parent_id" integer NULL
)
;
CREATE INDEX "nav_section_translation_language_id" ON "nav_section_translation" ("language_id");
CREATE INDEX "nav_section_translation_master_id" ON "nav_section_translation" ("master_id");
CREATE INDEX "nav_section_slug" ON "nav_section" ("slug");
CREATE INDEX "nav_section_parent_id" ON "nav_section" ("parent_id");
CREATE TABLE "news_news_translation" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "text" text NOT NULL,
    "language_id" integer NOT NULL,
    "master_id" integer NOT NULL,
    UNIQUE ("language_id", "master_id")
)
;
CREATE TABLE "news_news" (
    "id" integer NOT NULL PRIMARY KEY,
    "slug" varchar(24) NOT NULL,
    "pub_date" datetime NOT NULL,
    "author_id" integer NOT NULL REFERENCES "auth_user" ("id")
)
;
CREATE INDEX "news_news_translation_language_id" ON "news_news_translation" ("language_id");
CREATE INDEX "news_news_translation_master_id" ON "news_news_translation" ("master_id");
CREATE INDEX "news_news_slug" ON "news_news" ("slug");
CREATE INDEX "news_news_author_id" ON "news_news" ("author_id");
CREATE TABLE "polls_poll" (
    "id" integer NOT NULL PRIMARY KEY,
    "slug" varchar(12) NOT NULL,
    "pub_date" datetime NOT NULL,
    "votedByG" integer unsigned NULL,
    "votedByC" integer unsigned NULL
)
;
CREATE TABLE "polls_singlechoicepoll_translation" (
    "id" integer NOT NULL PRIMARY KEY,
    "question" varchar(200) NOT NULL,
    "language_id" integer NOT NULL,
    "master_id" integer NOT NULL,
    UNIQUE ("language_id", "master_id")
)
;
CREATE TABLE "polls_singlechoicepoll" (
    "poll_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "polls_poll" ("id")
)
;
CREATE TABLE "polls_percentagepoll_translation" (
    "id" integer NOT NULL PRIMARY KEY,
    "question" varchar(200) NOT NULL,
    "min" varchar(200) NOT NULL,
    "low" varchar(200) NOT NULL,
    "avg" varchar(200) NOT NULL,
    "high" varchar(200) NOT NULL,
    "max" varchar(200) NOT NULL,
    "language_id" integer NOT NULL,
    "master_id" integer NOT NULL,
    UNIQUE ("language_id", "master_id")
)
;
CREATE TABLE "polls_percentagepoll" (
    "poll_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "polls_poll" ("id")
)
;
CREATE TABLE "polls_choice_translation" (
    "id" integer NOT NULL PRIMARY KEY,
    "choice" varchar(200) NOT NULL,
    "language_id" integer NOT NULL,
    "master_id" integer NOT NULL,
    UNIQUE ("language_id", "master_id")
)
;
CREATE TABLE "polls_choice" (
    "id" integer NOT NULL PRIMARY KEY,
    "votes" integer unsigned NOT NULL,
    "poll_id" integer NOT NULL REFERENCES "polls_singlechoicepoll" ("poll_ptr_id"),
    "order" integer unsigned NOT NULL
)
;
CREATE TABLE "polls_percentage" (
    "id" integer NOT NULL PRIMARY KEY,
    "votes" integer unsigned NOT NULL,
    "poll_id" integer NOT NULL REFERENCES "polls_percentagepoll" ("poll_ptr_id"),
    "perc" integer unsigned NOT NULL
)
;
CREATE INDEX "polls_poll_slug" ON "polls_poll" ("slug");
CREATE INDEX "polls_singlechoicepoll_translation_language_id" ON "polls_singlechoicepoll_translation" ("language_id");
CREATE INDEX "polls_singlechoicepoll_translation_master_id" ON "polls_singlechoicepoll_translation" ("master_id");
CREATE INDEX "polls_percentagepoll_translation_language_id" ON "polls_percentagepoll_translation" ("language_id");
CREATE INDEX "polls_percentagepoll_translation_master_id" ON "polls_percentagepoll_translation" ("master_id");
CREATE INDEX "polls_choice_translation_language_id" ON "polls_choice_translation" ("language_id");
CREATE INDEX "polls_choice_translation_master_id" ON "polls_choice_translation" ("master_id");
CREATE INDEX "polls_choice_poll_id" ON "polls_choice" ("poll_id");
CREATE INDEX "polls_percentage_poll_id" ON "polls_percentage" ("poll_id");
COMMIT;
