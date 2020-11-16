# -*- coding: UTF-8 -*-

"""Insertion templates for all database tables
"""

###############################################################################

# template for inserting thread insertion dict into MySQL database
ADD_THREAD = (
  "INSERT INTO threads "
  "(thread_url, thread_id, thread_title, last_page, creator_username, creator_user_id, thread_timestamp) "
  "VALUES (%(thread_url)s, %(thread_id)s, %(thread_title)s, %(last_page)s, %(creator_username)s, %(creator_user_id)s, %(thread_timestamp)s)")

# template for inserting post insertion dict into MySQL database
ADD_POST = (
  "INSERT INTO posts "
  "(thread_id, post_id, author_username, author_user_id, post_timestamp, post_text) "
  "VALUES (%(thread_id)s, %(post_id)s, %(author_username)s, %(author_user_id)s, %(post_timestamp)s, %(post_text)s)")

# template for inserting blockquote insertion dict into MySQL database
ADD_BLOCKQUOTE = (
  "INSERT INTO blockquotes "
  "(thread_id, post_id, post_url, author_user_id, blockquote_text, blockquote_source) "
  "VALUES (%(thread_id)s, %(post_id)s, %(post_url)s, %(author_user_id)s, %(blockquote_text)s, %(blockquote_source)s)")

# template for inserting link insertion dict into MySQL database
ADD_LINK = (
  "INSERT INTO links "
  "(thread_id, post_id, author_user_id, link_source, link_text) "
  "VALUES (%(thread_id)s, %(post_id)s, %(author_user_id)s, %(link_source)s, %(link_text)s)")

# template for inserting image insertion dict into MySQL database
ADD_IMAGE = (
  "INSERT INTO images "
  "(thread_id, post_id, author_user_id, image_source) "
  "VALUES (%(thread_id)s, %(post_id)s, %(author_user_id)s, %(image_source)s)")

# template for inserting reaction insertion dict into MySQL database
ADD_REACTION = (
  "INSERT INTO reactions "
  "(post_id, author_username, author_user_id, reaction_id, reaction_name, reaction_timestamp) "
  "VALUES (%(post_id)s, %(author_username)s, %(author_user_id)s, %(reaction_id)s, %(reaction_name)s, %(reaction_timestamp)s)")

# template for inserting user insertion dict into MySQL database
ADD_USER = (
  "INSERT INTO users "
  "(user_username, user_id, user_image, user_messages, user_reaction_score, user_points, user_joined, user_last_seen) "
  "VALUES (%(user_username)s, %(user_id)s, %(user_image)s, %(user_messages)s, %(user_reaction_score)s,%(user_points)s, %(user_joined)s, %(user_last_seen)s  )")

###############################################################################

# dict of database tables with associated columns and types
TABLES = {
  'threads' : (
    "CREATE TABLE `threads` ("
    "  `thread_url` varchar(1024) NOT NULL,"
    "  `thread_id` int NOT NULL,"
    "  `thread_title` varchar(1024) NOT NULL,"
    "  `last_page` smallint NOT NULL,"
    "  `creator_username` varchar(128),"
    "  `creator_user_id` mediumint,"
    "  `thread_timestamp` int NOT NULL"
    ") ENGINE=InnoDB"),
  'posts' : (
    "CREATE TABLE `posts` ("
    "  `thread_id` int NOT NULL,"
    "  `post_id` int NOT NULL,"
    "  `post_url` varchar(1024) NOT NULL,"
    "  `author_username` varchar(128),"
    "  `author_user_id` mediumint,"
    "  `post_timestamp` int NOT NULL,"
    "  `post_text` mediumtext"
    ") ENGINE=InnoDB"),
  'blockquotes' : (
    "CREATE TABLE `blockquotes` ("
    "  `thread_id` int NOT NULL,"
    "  `post_id` int NOT NULL,"
    "  `author_user_id` mediumint,"
    "  `blockquote_text` mediumtext NOT NULL,"
    "  `blockquote_source` varchar(1024)"
    ") ENGINE=InnoDB"),
  'links' : (
    "CREATE TABLE `links` ("
    "  `thread_id` int NOT NULL,"
    "  `post_id` int NOT NULL,"
    "  `author_user_id` mediumint,"
    "  `link_source` varchar(2048) NOT NULL"
    "  `link_text` mediumtext"
    ") ENGINE=InnoDB"),
  'images' : (
    "CREATE TABLE `images` ("
    "  `thread_id` int NOT NULL,"
    "  `post_id` int NOT NULL,"
    "  `author_user_id` mediumint,"
    "  `image_source` varchar(2048) NOT NULL"
    ") ENGINE=InnoDB"),
  'reactions' : (
    "CREATE TABLE `reactions` ("
    "  `post_id` int NOT NULL,"
    "  `author_username` varchar(128),"
    "  `author_user_id` mediumint,"
    "  `reaction_id` tinyint"
    "  `reaction_name` varchar(16) NOT NULL"
    "  `reaction_timestamp` int NOT NULL,"
    ") ENGINE=InnoDB"),
  'users' : (
    "CREATE TABLE `users` ("
    "  `user_username` varchar(128) NOT NULL,"
    "  `user_id` mediumint NOT NULL,"
    "  `user_image` varchar(2048),"
    "  `user_messages` mediumint NOT NULL,"
    "  `user_reaction_score` mediumint NOT NULL,"
    "  `user_points` mediumint NOT NULL,"
    "  `user_joined` int NOT NULL,"
    "  `user_last_seen` int,"
    ") ENGINE=InnoDB") }

###############################################################################