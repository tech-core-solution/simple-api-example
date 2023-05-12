CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(15) NOT NULL,
    last_name VARCHAR(15) NOT NULL,
    email VARCHAR(75) NOT NULL UNIQUE,
    hash_password VARCHAR(75) NOT NULL,
    access_token VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    title VARCHAR(15) NOT NULL,
    todo_description VARCHAR(200) NOT NULL,
    FOREIGN KEY (userId) REFERENCES user (id)
);
