-- creates the table users

CREATE TABLE IF NOT EXISTS users (
    id NOT NULL PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
