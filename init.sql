-- MySQL initialization script for RangBot
-- Create database and set character set

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS rangbot_db;
USE rangbot_db;

-- Set character set to utf8mb4 for proper Unicode support
ALTER DATABASE rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify database creation
SHOW DATABASES;
SHOW CREATE DATABASE rangbot_db;

-- Create a test table (optional)
-- CREATE TABLE IF NOT EXISTS test (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
