CREATE DATABASE reddit;
CREATE USER 'tmp_user'@'%' IDENTIFIED BY 'easy';
GRANT ALL PRIVILEGES ON reddit.* TO 'tmp_user'@'%';
FLUSH PRIVILEGES;

