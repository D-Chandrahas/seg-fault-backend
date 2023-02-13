DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

PRAGMA foreign_keys = ON;

.read 'ddl.sql'
.read 'insert_users.sql'
.read 'insert_posts.sql'
.read 'insert_replies.sql'