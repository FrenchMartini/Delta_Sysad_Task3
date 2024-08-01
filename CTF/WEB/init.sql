-- Create the database
CREATE DATABASE ctf_db;

-- Use the database
USE ctf_db;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    flag VARCHAR(100)
);

-- Insert a sample user and a hidden flag
INSERT INTO users (username, password, flag) VALUES
('admin', 'password', 'CTF{hidden_flag}');
