--Setup script for Ticket Priority System Database
-- Run this in MySQL to initialize the schema

USE ticket_priority_system;

--USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- TICKETS TABLE
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_type VARCHAR(50) NOT NULL,
    impact INT NOT NULL,
    customer_type VARCHAR(50) NOT NULL,
    priority_score INT,
    priority_level VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_priority_level (priority_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===== OPTIONAL TEST DATA =====
-- I've included a test user account for development and testing.
-- Username: vineel
-- Password: password (stored as bcrypt hash with security level 12)
-- The password is already hashed when you insert it. If you need to create a new test user,
-- you can generate a bcrypt hash using Python:
--   python -c "import bcrypt; print(bcrypt.hashpw(b'your_password', bcrypt.gensalt()).decode())"

INSERT IGNORE INTO users (username, password_hash, created_at) VALUES 
('vineel', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm2', NOW());

-- Verify
SELECT * FROM users;
SELECT * FROM tickets;
