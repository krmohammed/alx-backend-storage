-- creates the table users

CREATE TABLE IF NOT EXISTS users (
    id INT AUTOINCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
