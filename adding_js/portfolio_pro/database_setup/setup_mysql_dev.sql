-- This script creates a new uset in a database

-- Creating a database if not exist
CREATE DATABASE IF NOT EXISTS online_store_db;
-- Creating a new user
CREATE USER IF NOT EXISTS 'online_store'@'localhost' IDENTIFIED BY 'online_store_pwd';
-- Granting all privileges on the database
GRANT ALL PRIVILEGES ON online_store_db.* TO 'online_store'@'localhost';
-- Granting SELECT privileges on the database
GRANT SELECT ON performance_schema.* TO 'online_store'@'localhost';
