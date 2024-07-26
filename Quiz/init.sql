CREATE DATABASE task3;
\connect task3


-- Create users table
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255)
);

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    question_text TEXT,
    correct_answer TEXT,
    answer TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
);

-- Create leaderboard table
CREATE TABLE IF NOT EXISTS leaderboard (
    username VARCHAR(50) PRIMARY KEY,
    points INTEGER DEFAULT 0,
    FOREIGN KEY (username) REFERENCES users(username)
);
