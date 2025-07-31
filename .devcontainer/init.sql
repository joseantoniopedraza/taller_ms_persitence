-- init.sql
DROP DATABASE IF EXISTS persistence_db;
DROP USER IF EXISTS persistence_user;

CREATE USER persistence_user WITH PASSWORD 'A123456';
CREATE DATABASE persistence_db OWNER persistence_user;

GRANT ALL PRIVILEGES ON DATABASE persistence_db TO persistence_user;