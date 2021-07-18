CREATE ROLE useradmin WITH LOGIN;
CREATE DATABASE users OWNER useradmin;
CREATE TABLE users.users (username STRING PRIMARY KEY, password STRING NOT NULL) OWNER useradmin;
INSERT INTO users.users VALUES ('user1','$argon2id$v=19$m=102400,t=2,p=8$HgNACAGA8F7LGQPgXKu1lg$A6+Cgwfax9j8JJc/dc/yFA');
