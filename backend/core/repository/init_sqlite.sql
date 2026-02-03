CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_type TEXT NOT NULL,
    impact INTEGER NOT NULL,
    customer_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    priority_score INTEGER NOT NULL, 
    priority_level TEXT NOT NULL
);
