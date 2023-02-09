DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

PRAGMA foreign_keys = ON;

.read 'database management/ddl.sql'
.read 'database management/insert_users.sql'
.read 'database management/insert_posts.sql'
.read 'database management/insert_replies.sql'