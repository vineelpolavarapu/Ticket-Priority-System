CREATE TABLE tickets (

id INT AUTO_INCREMENT PRIMARY KEY,

issue_type VARCHAR(20) NOT NULL,

impact INT NOT NULL,

customer_type VARCHAR(20) NOT NULL,

create_time DATETIME NOT NULL,

priority_score INT,

priority_level VARCHAR(5)

);

CREATE INDEX idx_priority ON tickets(priority_level)