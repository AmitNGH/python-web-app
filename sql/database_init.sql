use db;

CREATE TABLE users (
    user_id INT NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    creation_date DateTime NOT NULL,
    primary key(user_id)
);

CREATE TABLE config (
    endpoint_name VARCHAR(50) NOT NULL,
    endpoint_url VARCHAR(50) NOT NULL,
    endpoint_port VARCHAR(50) NOT NULL,
    endpoint_api VARCHAR(50) NOT NULL,
    browser VARCHAR(50) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    primary key(endpoint_name)
);

INSERT INTO config (endpoint_name, endpoint_url, endpoint_port, endpoint_api, browser, user_name)
VALUES ("frontend", "localhost", "5001", "/users/get_user_data", "Chrome", "Amit");

INSERT INTO config (endpoint_name, endpoint_url, endpoint_port, endpoint_api, browser, user_name)
VALUES ("backend", "localhost", "5000", "/users", "Chrome", "Amit");
