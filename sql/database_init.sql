use db;

CREATE TABLE users (
    user_id INT NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    creation_date DateTime NOT NULL,
    primary key(user_id)
);
