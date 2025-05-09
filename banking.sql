CREATE DATABASE IF NOT EXISTS banking;
USE banking;

CREATE TABLE IF NOT EXISTS users (
    acc_no VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    pin VARCHAR(10),
    balance FLOAT DEFAULT 0
);

INSERT INTO users (acc_no, name, pin, balance) VALUES
('1001', 'Snigdha Sharma', '1234', 5000),
('1002', 'Amit Kumar', '5678', 10000)
ON DUPLICATE KEY UPDATE name=VALUES(name), pin=VALUES(pin), balance=VALUES(balance);
