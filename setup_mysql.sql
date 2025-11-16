-- Script untuk membuat database MySQL untuk RangBot Web
-- Jalankan di MySQL (phpMyAdmin atau MySQL Command Line)

-- Buat database
CREATE DATABASE IF NOT EXISTS rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Buat user (opsional, bisa menggunakan root)
-- CREATE USER IF NOT EXISTS 'rangbot_user'@'localhost' IDENTIFIED BY 'rangbot_password';
-- GRANT ALL PRIVILEGES ON rangbot_db.* TO 'rangbot_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Gunakan database
USE rangbot_db;

-- Tampilkan informasi
SELECT 'Database rangbot_db berhasil dibuat!' AS Status;

