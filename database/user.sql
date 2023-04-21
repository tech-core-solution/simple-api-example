CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(15) NOT NULL,
    last_name VARCHAR(15) NOT NULL,
    email VARCHAR(75) NOT NULL UNIQUE,
    hash_password VARCHAR(75) NOT NULL,
    user_type VARCHAR(10) NOT NULL,
    account_state BOOLEAN NOT NULL
);
