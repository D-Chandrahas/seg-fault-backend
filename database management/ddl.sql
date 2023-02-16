CREATE TABLE users (
	user_id INTEGER PRIMARY KEY,
	username VARCHAR(255) UNIQUE NOT NULL,
	password VARCHAR(255) DEFAULT 'password' NOT NULL
);

CREATE TABLE posts (
	post_id INTEGER PRIMARY KEY,
	user_id INTEGER ,
	title VARCHAR(512),
	tags VARCHAR(512),
	body TEXT,
	upvotes INTEGER DEFAULT 0,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE replies (
	reply_id INTEGER PRIMARY KEY,
	post_id INTEGER,
	user_id INTEGER,
	body TEXT,
	upvotes INTEGER DEFAULT 0,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (post_id) REFERENCES posts(post_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE post_votes (
	post_id INTEGER,
	user_id INTEGER,
	vote CHAR(1) CHECK (vote IN ('u', 'd')),
	PRIMARY KEY (post_id, user_id),
	FOREIGN KEY (post_id) REFERENCES posts(post_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE reply_votes (
	reply_id INTEGER,
	user_id INTEGER,
	vote CHAR(1) CHECK (vote IN ('u', 'd')),
	PRIMARY KEY (reply_id, user_id),
	FOREIGN KEY (reply_id) REFERENCES replies(reply_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);